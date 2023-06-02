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

from games import RouletteAPI
from Shared.games.roulette import RouletteBet, RouletteBetResponse, RouletteColor


class MainWindow(QDialog):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._login_line_edit = QLineEdit()
        self._bet_line_edit = QLineEdit()
        self._color_line_edit = QLineEdit()

        self._connect_to_game_button = QPushButton("Connect")
        self._bet_button = QPushButton("Bet")
        # self._send_button = QPushButton("Send")
        quit_button = QPushButton("Disconnect")

        self._connect_to_game_button.clicked.connect(self.connect_to_game)
        self._bet_button.clicked.connect(self.bet)
        # self._send_button.clicked.connect(self.send)
        quit_button.clicked.connect(self.disconnect_from_chat_room)

        button_box = QDialogButtonBox()
        button_box.add_button(self._connect_to_game_button, QDialogButtonBox.ButtonRole.ActionRole)
        button_box.add_button(self._bet_button, QDialogButtonBox.ButtonRole.ActionRole)
        # button_box.add_button(self._send_button, QDialogButtonBox.ButtonRole.ActionRole)
        button_box.add_button(quit_button, QDialogButtonBox.ButtonRole.RejectRole)

        self._bet_response_label = QLabel()
        self._result_label = QLabel()
        self._others_bets_label = QLabel()

        main_layout = QVBoxLayout()
        main_layout.add_widget(self._login_line_edit)
        main_layout.add_widget(self._bet_line_edit)
        main_layout.add_widget(self._color_line_edit)
        main_layout.add_widget(button_box)
        main_layout.add_widget(self._bet_response_label)
        main_layout.add_widget(self._result_label)
        main_layout.add_widget(self._others_bets_label)
        self.set_layout(main_layout)

        self.window_title = "Client"
        self._login_line_edit.set_focus()
        
        

    def connect_to_game(self) -> None:
        self._bet_response_label.text = ""
        api = RouletteAPI()
        api._login = self._login_line_edit.text
        api.betResponse.connect(self.bet_response)
        api.resultRecieved.connect(self.bet_result)
        api.betRecieved.connect(self.others_bets)
        api.connect_to_game()

    def bet(self) -> None:
        self._bet_response_label.text = ""

        api = RouletteAPI()
        bet = RouletteBet(int(self._bet_line_edit.text), RouletteColor(self._color_line_edit.text))
        api.bet(bet)

    def disconnect_from_chat_room(self) -> None:
        self._bet_response_label.text = ""

        api = RouletteAPI()
        api.disconnect_from_game()
        api.betResponse.disconnect(self.bet_response)
        api.resultRecieved.disconnect(self.bet_result)
        api.betRecieved.disconnect(self.others_bets)

    def bet_response(self, response: RouletteBetResponse) -> None:
        self._bet_response_label.text = f"Ответ {response.value}"

    def bet_result(self, result: RouletteColor) -> None:
        self._result_label.text = f"Выпало {result.value}"

    def others_bets(self, login: str, bet: RouletteBet) -> None:
        self._others_bets_label.text = f"Другая ставка {login}: {bet.total} - {bet.color}"


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(window.exec())
