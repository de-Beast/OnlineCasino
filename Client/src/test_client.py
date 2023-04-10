import PySide6
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtCore import QByteArray, QDataStream, QMutex, QThread, Signal
from PySide6.QtNetwork import QHostAddress, QTcpSocket
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)


class SocketHandler(QThread):
    requestAnswer = Signal(str)

    def __init__(self, login_line_text: str, password_line_text: str, parent=None) -> None:
        super().__init__(parent)
        self.finished.connect(self.delete_later)

        self._login_line_text: str = login_line_text
        self._password_line_text: str = password_line_text

        self._mutex = QMutex()

    def run(self) -> None:
        socket = QTcpSocket()
        socket.connect_to_host(QHostAddress.SpecialAddress.LocalHost, 8888)
        if not socket.wait_for_connected(5000):
            return

        self._mutex.lock()
        login_line_text = self._login_line_text
        password_line_text = self._password_line_text
        self._mutex.unlock()

        block = QByteArray()
        send_stream = QDataStream(block, QDataStream.OpenModeFlag.WriteOnly)
        send_stream.set_version(QDataStream.Version.Qt_6_4)
        send_stream.write_string(login_line_text)
        send_stream.write_string(password_line_text)
        socket.write(block)

        socket.readyRead.connect(lambda: self.on_readyRead(socket))

        if not socket.wait_for_ready_read(3000):
            self.requestAnswer.emit("Cant get answer")

    def on_readyRead(self, socket: QTcpSocket) -> None:
        recieve_stream = QDataStream(socket)
        recieve_stream.set_version(QDataStream.Version.Qt_6_4)

        recieve_stream.start_transaction()
        answer = recieve_stream.read_string()
        if not recieve_stream.commit_transaction():
            return

        self.requestAnswer.emit(answer)
        self.quit()


class MainWindow(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._login_line_edit = QLineEdit()
        self._password_line_edit = QLineEdit()

        self._login_line_edit.textChanged.connect(self.set_enabled_sign_in_button)
        self._password_line_edit.textChanged.connect(self.set_enabled_sign_in_button)

        self._sign_in_button = QPushButton("Sign in")
        quit_button = QPushButton("Quit")

        self._sign_in_button.clicked.connect(self.sign_in)
        quit_button.clicked.connect(self.close)

        button_box = QDialogButtonBox()
        button_box.add_button(self._sign_in_button, QDialogButtonBox.ButtonRole.ActionRole)
        button_box.add_button(quit_button, QDialogButtonBox.ButtonRole.RejectRole)

        self._answer_label = QLabel()

        main_layout = QVBoxLayout()
        main_layout.add_widget(self._login_line_edit)
        main_layout.add_widget(self._password_line_edit)
        main_layout.add_widget(button_box)
        main_layout.add_widget(self._answer_label)
        self.set_layout(main_layout)

        self.window_title = "Client"
        self._login_line_edit.set_focus()

    def set_enabled_sign_in_button(self) -> None:
        self._sign_in_button.enabled = self._login_line_edit.text != "" and self._password_line_edit.text != ""

    def sign_in(self) -> None:
        self._answer_label.text = ""
        self._sign_in_button.enabled = False
        self.socket = SocketHandler(self._login_line_edit.text, self._password_line_edit.text)
        self.socket.requestAnswer.connect(self.get_answer)
        self.socket.start()

    def get_answer(self, answer: str) -> None:
        self._answer_label.text = answer


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(window.exec())
