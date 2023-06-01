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

from account import AccountAPI
from chat import ChatAPI


class MainWindow(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._login_line_edit = QLineEdit()
        self._password_line_edit = QLineEdit()

        self._sign_in_button = QPushButton("Sign in")
        self._connect_button = QPushButton("Connect")
        self._send_button = QPushButton("Send")
        quit_button = QPushButton("Disconnect")

        self._sign_in_button.clicked.connect(self.sign_in)
        self._connect_button.clicked.connect(self.connect_to_chat_room)
        self._send_button.clicked.connect(self.send)
        quit_button.clicked.connect(self.disconnect_from_chat_room)

        button_box = QDialogButtonBox()
        button_box.add_button(self._sign_in_button, QDialogButtonBox.ButtonRole.ActionRole)
        button_box.add_button(self._connect_button, QDialogButtonBox.ButtonRole.ActionRole)
        button_box.add_button(self._send_button, QDialogButtonBox.ButtonRole.ActionRole)
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

    def sign_in(self) -> None:
        self._answer_label.text = ""

        api = AccountAPI()
        api.responseAccountInitial.connect(self.get_answer)
        api.auth(self._login_line_edit.text, self._password_line_edit.text)

    def connect_to_chat_room(self) -> None:
        self._answer_label.text = ""

        api = ChatAPI()
        api.recievedMessage.connect(self.get_answer)
        api.connect_to_chat_room("roulette")

    def send(self) -> None:
        self._answer_label.text = ""

        api = ChatAPI()
        api.send_message(self._login_line_edit.text, self._password_line_edit.text)

    def disconnect_from_chat_room(self) -> None:
        self._answer_label.text = ""

        api = ChatAPI()
        api.disconnect_from_chat_room()
        api.recievedMessage.disconnect(self.get_answer)

    def get_answer(self, info: str, bonus_info: str | None = None) -> None:
        # if isinstance(info, str):
        #     self._answer_label.text = f"{info}"
        # elif isinstance(info, dict):
        #     self._answer_label.text = f"{info['nickname']}: {info['balance']}"
        if bonus_info is not None:
            self._answer_label.text = f"{info}: {bonus_info}"
        else:
            self._answer_label.text = f"{info}"


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(window.exec())
