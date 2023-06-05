import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import QMutex, QMutexLocker, Signal

from abstract import ServerSocketContainer
from Shared.games.roulette import (
    RouletteBet,
    RouletteBetResponse,
    RouletteColor,
    RouletteState,
)
from Shared.sockets import SocketType

from ..roulette import Roulette


class RouletteSocketContainer(ServerSocketContainer):
    socket_type = SocketType.ROULETTE

    betResponse = Signal(RouletteBetResponse)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.roulette = Roulette()
        self.mutex = QMutex()

    def on_start(self) -> None:
        self.send_current_roulette_info()

        self.readyRead.connect(self.receive_bet)
        self.betResponse.connect(self.send_bet_response)

        self.roulette.result.connect(self.send_result)
        self.roulette.betMade.connect(self.send_new_bet)
        self.roulette.stateChanged.connect(self.send_roulette_state)

    def on_exit(self) -> None:
        self.roulette.result.disconnect(self.send_result)
        self.roulette.betMade.disconnect(self.send_new_bet)
        self.roulette.stateChanged.disconnect(self.send_roulette_state)

    def send_current_roulette_info(self) -> None:
        with QMutexLocker(self.mutex):
            state = self.roulette.state
            bets = self.roulette.bets
            last_results = self.roulette.last_results

        self.send_roulette_state(state)
        for login, bet in bets.items():
            self.send_new_bet(login, bet)
        for result in last_results:
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
