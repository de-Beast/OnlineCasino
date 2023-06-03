import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import Signal

from Shared.abstract import SocketContainerBase
from Shared.games.roulette import (
    RouletteBet,
    RouletteBetResponse,
    RouletteColor,
    RouletteState,
)
from Shared.sockets import SocketType

from ..roulette import Roulette


class RouletteSocketContainer(SocketContainerBase):
    socket_type = SocketType.ROULETTE

    betResponse = Signal(RouletteBetResponse)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.roulette = Roulette()

    def run(self) -> None:
        self.socket.readyRead.connect(self.connect_to_game)
        self.connect_to_game()

    def exit(self) -> None:
        self.socket.readyRead.disconnect(self.slot_storage.pop("receive_bet"))
        super().exit()

    def connect_to_game(self) -> None:
        data: tuple[SocketContainerBase.ContainerRequest] | None = self.receive_data_package(
            SocketContainerBase.ContainerRequest
        )
        if data is None:
            return
        self.socket.readyRead.disconnect(self.connect_to_game)

        (request,) = data
        if request is not SocketContainerBase.ContainerRequest.CONNECT:
            return
        
        self.betResponse.connect(self.send_bet_response)
        self.roulette.result.connect(self.send_result)
        self.roulette.betMade.connect(self.send_new_bet)
        self.roulette.stateChanged.connect(self.send_roulette_state)
        self.socket.readyRead.connect(self.slot_storage.create_and_store_slot("receive_bet", self.receive_bet))

        self.send_roulette_state(self.roulette.state)
        for login, bet in self.roulette.bets.items():
            self.send_new_bet(login, bet)
        for result in self.roulette.last_results:
            self.send_result(result, -1)

    def receive_bet(self) -> None:
        data: tuple[str, RouletteBet] | None = self.receive_data_package(str, RouletteBet)
        if data is None:
            return

        login, bet = data
        self.roulette.makeBet.emit(self, login, bet)

    def send_bet_response(self, response) -> None:
        self.send_data_package(response)

    def send_new_bet(self, login: str, bet: RouletteBet) -> None:
        self.send_data_package(login, bet)

    def send_result(self, result: RouletteColor, sector: int) -> None:
        self.send_data_package(result, sector)

    def send_roulette_state(self, state: RouletteState) -> None:
        self.send_data_package(state)
