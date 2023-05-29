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

from client_sockets import Client, ChatSocketThread


class MainWindow(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

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
        self.socket = ChatSocketThread(self, "roulette")
        self.socket.responseRecieved.connect(self.get_answer)
        self.socket.send_message(self._login_line_edit.text, self._password_line_edit.text)

        #self.client.register(
        #    self._login_line_edit.text, self._password_line_edit.text, responseReceived_slot=self.get_answer
        #)
        # self.client = AccountInitialSocketThread(self)
        # self.client.responseRecieved.connect(self.get_answer)
        # self.client.register(self._login_line_edit.text, self._password_line_edit.text)

    def sign_in(self) -> None:
        self._answer_label.text = ""
        self._sign_up_button.enabled = False
        self._sign_in_button.enabled = False
        self.client.auth(
            self._login_line_edit.text, self._password_line_edit.text, responseReceived_slot=self.get_answer
        )
        # self.socket = AccountInitialSocketThread(self)
        # self.socket.answerRecieved.connect(self.get_answer)
        # self.socket.auth(self._login_line_edit.text, self._password_line_edit.text)
        # self.client = AccountInfoSocketThread(self)
        # self.client.responseRecieved.connect(self.get_answer)
        # self.client.get_account_info(self._login_line_edit.text)

    def get_answer(self, nickname: str, message: str) -> None:
        #self._answer_label.text = answer
        self._answer_label.text = f"{nickname}: {message}"


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(window.exec())
