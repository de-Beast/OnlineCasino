import PySide6  # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtWidgets import (
    QApplication,
    QDialog,
    QDialogButtonBox,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
)

from client_sockets import (
    AccountInfoSocketThread,
    AccountInitialSocketThread,
    ClientSocketThread,
)


class MainWindow(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)
        self.socket: ClientSocketThread

        self._login_line_edit = QLineEdit()
        self._password_line_edit = QLineEdit()

        self._login_line_edit.textChanged.connect(self.set_enabled_sign_buttons)
        self._password_line_edit.textChanged.connect(self.set_enabled_sign_buttons)

        self._sign_up_button = QPushButton("Sign up")
        self._sign_in_button = QPushButton("Sign in")
        quit_button = QPushButton("Quit")

        self._sign_up_button.clicked.connect(self.sign_up)
        self._sign_in_button.clicked.connect(self.sign_in)
        quit_button.clicked.connect(self.close)

        button_box = QDialogButtonBox()
        button_box.add_button(self._sign_up_button, QDialogButtonBox.ButtonRole.ActionRole)
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
        self._sign_up_button.enabled = False
        self._sign_in_button.enabled = False
        self._login_line_edit.set_focus()

    def set_enabled_sign_buttons(self) -> None:
        enabled = self._login_line_edit.text != "" and self._password_line_edit.text != ""
        self._sign_in_button.enabled = self._sign_up_button.enabled = enabled

    def sign_up(self) -> None:
        self._answer_label.text = ""
        self._sign_up_button.enabled = False
        self._sign_in_button.enabled = False
        self.socket = AccountInitialSocketThread(self)
        self.socket.responseRecieved.connect(self.get_answer)
        self.socket.register(self._login_line_edit.text, self._password_line_edit.text)

    def sign_in(self) -> None:
        self._answer_label.text = ""
        self._sign_up_button.enabled = False
        self._sign_in_button.enabled = False
        # self.socket = AccountInitialSocketThread(self)
        # self.socket.answerRecieved.connect(self.get_answer)
        # self.socket.auth(self._login_line_edit.text, self._password_line_edit.text)
        self.socket = AccountInfoSocketThread(self)
        self.socket.responseRecieved.connect(self.get_answer)
        self.socket.get_account_info(self._login_line_edit.text)

    def get_answer(self, answer: dict) -> None:
        self._answer_label.text = f"balance: {answer['balance']}, nickname: {answer['nickname']}"


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(window.exec())
