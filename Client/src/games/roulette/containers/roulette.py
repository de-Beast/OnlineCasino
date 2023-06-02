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
    resultRecieved = Signal(RouletteColor, int)
    rouletteStateChanged = Signal(RouletteState)
    betRecieved = Signal(str, RouletteBet)

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
        slot = self.slot_storage.create_and_store_slot("recieve_bet", self.recieve_bet)
        self.socket.readyRead.connect(slot)

        slot = self.slot_storage.create_and_store_slot("recieve_result", self.recieve_result)
        self.socket.readyRead.connect(slot)
        
        slot = self.slot_storage.create_and_store_slot("recieve_roulette_state", self.recieve_roulette_state)
        self.socket.readyRead.connect(slot)
        self.send_data_package()

    def exit(self) -> None:
        super().exit()
        self.socket.readyRead.disconnect(self.slot_storage.pop("recieve_bet"))
        self.socket.readyRead.disconnect(self.slot_storage.pop("recieve_result"))
        self.socket.readyRead.disconnect(self.recieve_bet_response)

    def send_bet(self, login: str, bet: RouletteBet) -> None:
        self._sendBet.emit(login, bet)

    def _send_bet(self, login: str, bet: RouletteBet) -> None:
        self.send_data_package(login, bet)
        self.socket.readyRead.connect(self.recieve_bet_response)

    def recieve_bet_response(self) -> None:
        data: tuple[RouletteBetResponse] | None = self.recieve_data_package(RouletteBetResponse)
        if data is None:
            return
        self.socket.readyRead.disconnect(self.recieve_bet_response)

        (bet_response,) = data
        self.betResponse.emit(bet_response)

    def recieve_bet(self) -> None:
        data: tuple[str, RouletteBet] | None = self.recieve_data_package(str, RouletteBet)
        if data is None:
            return

        login, bet = data
        self.betRecieved.emit(login, bet)

    def recieve_result(self) -> None:
        data: tuple[RouletteColor, int] | None = self.recieve_data_package(RouletteColor, int)
        if data is None:
            return

        (result, sector) = data
        self.resultRecieved.emit(result, sector)

    def recieve_roulette_state(self) -> None:
        data: tuple[RouletteState] | None = self.recieve_data_package(RouletteState)
        if data is None:
            return

        (state,) = data
        self.rouletteStateChanged.emit(state)