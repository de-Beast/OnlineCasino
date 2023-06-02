import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401

from Shared.abstract import SocketContainerBase
from Shared.games.roulette import RouletteBet, RouletteColor, RouletteState
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
        self.roulette.betResponse.connect(self.send_bet_response)
        self.roulette.stateChanged.connect(self.send_roulette_state)

        self.socket.readyRead.connect(self.slot_storage.create_and_store_slot("recieve_bet", self.recieve_bet))
        self.recieve_data_package()
        self.send_roulette_state(self.roulette.state)

    def exit(self) -> None:
        super().exit()
        self.socket.readyRead.disconnect(self.slot_storage.pop("recieve_bet"))

    def recieve_bet(self) -> None:
        data: tuple[str, RouletteBet] | None = self.recieve_data_package(str, RouletteBet)
        if data is None:
            return

        login, bet = data
        self.roulette.makeBet.emit(login, bet)

    def send_bet_response(self, response) -> None:
        self.send_data_package(response)

    def send_new_bet(self, login: str, bet: RouletteBet) -> None:
        self.send_data_package(login, bet)

    def send_result(self, result: RouletteColor, sector: int) -> None:
        self.send_data_package(result, sector)
    
    def send_roulette_state(self, state: RouletteState) -> None:
        self.send_data_package(state)
