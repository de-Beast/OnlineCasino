import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import Signal

from abstract import ClientSocketContainer
from Shared.games.roulette import (
    RouletteBet,
    RouletteBetResponse,
    RouletteColor,
    RouletteState,
)
from Shared.sockets import SocketType


class RouletteSocketContainer(ClientSocketContainer):
    socket_type = SocketType.ROULETTE

    betResponse = Signal(RouletteBetResponse)
    resultReceived = Signal(RouletteColor, int)
    rouletteStateChanged = Signal(RouletteState)
    betReceived = Signal(str, RouletteBet)

    start = Signal()
    _sendBet = Signal(str, RouletteBet)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def on_start(self) -> None:
        super().on_start()
        self.start.disconnect(self.on_start)

        self._sendBet.connect(self._send_bet)
        self.readyRead.connect(self.receive_bet)
        self.readyRead.connect(self.receive_result)
        self.readyRead.connect(self.receive_roulette_state)

    def send_bet(self, login: str, bet: RouletteBet) -> None:
        self._sendBet.emit(login, bet)

    def _send_bet(self, login: str, bet: RouletteBet) -> None:
        self.readyRead.connect(self.receive_bet_response)
        self.send_data_package(login, bet)

    def receive_bet_response(self) -> None:
        data = self.receive_data_package(RouletteBetResponse)
        if data is None:
            return
        self.readyRead.disconnect(self.receive_bet_response)

        (bet_response,) = data
        self.betResponse.emit(bet_response)

    def receive_bet(self) -> None:
        data: tuple[str, RouletteBet] | None = self.receive_data_package(str, RouletteBet)
        if data is None:
            return

        login, bet = data
        self.betReceived.emit(login, bet)

    def receive_result(self) -> None:
        data: tuple[RouletteColor, int] | None = self.receive_data_package(RouletteColor, int)
        if data is None:
            return

        (result, sector) = data
        self.resultReceived.emit(result, sector)

    def receive_roulette_state(self) -> None:
        data = self.receive_data_package(RouletteState)
        if data is None:
            return

        (state,) = data
        self.rouletteStateChanged.emit(state)
