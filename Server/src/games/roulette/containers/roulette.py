import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401

from Shared.abstract import SocketContainerBase
from Shared.games.roulette import RouletteBet, RouletteColor
from Shared.sockets import SocketType

from ..roulette import Roulette


class RouletteSocketContainer(SocketContainerBase):
    socket_type = SocketType.ROULETTE

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.roulette = Roulette()

    def run(self) -> None:
        self.roulette.result.connect(self.send_result)
        self.roulette.betMade.connect(self.send_new_bet)
        self.roulette.betResponse.connect(self.bet_response)

        self.socket.readyRead.connect(self.slot_storage.create_and_store_slot("recieve_bet", self.recieve_bet))
        self.recieve_bet()

    def exit(self) -> None:
        super().exit()
        self.socket.readyRead.disconnect(self.slot_storage.pop("recieve_bet"))

    def recieve_bet(self) -> None:
        data: tuple[str, RouletteBet] | None = self.recieve_data_package(str, RouletteBet)
        if data is None:
            return

        login, bet = data
        self.roulette.makeBet.emit(login, bet)

    def bet_response(self, response) -> None:
        self.send_data_package(response)

    def send_new_bet(self, login: str, bet: RouletteBet) -> None:
        self.send_data_package(login, bet)

    def send_result(self, result: RouletteColor) -> None:
        self.send_data_package(result)