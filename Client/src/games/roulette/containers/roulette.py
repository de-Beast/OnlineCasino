import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import Signal

from Shared.abstract import SocketContainerBase
from Shared.games.roulette import (
    RouletteBet,
    RouletteBetResponse,
    RouletteColor,
    RouletteState,
)
from Shared.sockets import SocketType


class RouletteSocketContainer(SocketContainerBase):
    socket_type = SocketType.ROULETTE

    betResponse = Signal(RouletteBetResponse)
    resultReceived = Signal(RouletteColor, int)
    rouletteStateChanged = Signal(RouletteState)
    betReceived = Signal(str, RouletteBet)

    _sendBet = Signal(str, RouletteBet)
    _start = Signal()

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        slot = self.slot_storage.create_and_store_slot("_send_bet", self._send_bet)
        self._sendBet.connect(slot)
        self._start.connect(self.start)

    def run(self) -> None:
        self._start.emit()

    def start(self) -> None:
        slot = self.slot_storage.create_and_store_slot("receive_bet", self.receive_bet)
        self.socket.readyRead.connect(slot)

        slot = self.slot_storage.create_and_store_slot("receive_result", self.receive_result)
        self.socket.readyRead.connect(slot)

        slot = self.slot_storage.create_and_store_slot("receive_roulette_state", self.receive_roulette_state)
        self.socket.readyRead.connect(slot)
        self.connect_to_game()

    def exit(self) -> None:
        super().exit()
        self.socket.readyRead.disconnect(self.slot_storage.pop("receive_bet"))
        self.socket.readyRead.disconnect(self.slot_storage.pop("receive_result"))
        self.socket.readyRead.disconnect(self.receive_bet_response)

    def connect_to_game(self) -> None:
        self.send_data_package(SocketContainerBase.ContainerRequest.CONNECT)

    def send_bet(self, login: str, bet: RouletteBet) -> None:
        self._sendBet.emit(login, bet)

    def _send_bet(self, login: str, bet: RouletteBet) -> None:
        self.send_data_package(login, bet)
        self.socket.readyRead.connect(self.receive_bet_response)

    def receive_bet_response(self) -> None:
        data: tuple[RouletteBetResponse] | None = self.receive_data_package(RouletteBetResponse)
        if data is None:
            return
        self.socket.readyRead.disconnect(self.receive_bet_response)

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
        data: tuple[RouletteState] | None = self.receive_data_package(RouletteState)
        if data is None:
            return

        (state,) = data
        self.rouletteStateChanged.emit(state)
