import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import QMutexLocker, QObject, Signal
from PySide6.QtNetwork import QTcpSocket

from Shared.sockets.enums import SocketThreadType

from .ABC import ClientSocketThreadABC
from .Client import Client

class BetSocketThread(ClientSocketThreadABC):
    responseRecieved = Signal(bool, int, str, str)
    socket_type = SocketThreadType.BET

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self.bet: int
        self.login: str
        self.color: str

    def thread_workflow(self, socket: QTcpSocket) -> None:
        with QMutexLocker(self.mutex):
            bet = self.bet
            login = self.login
            color = self.color

        self.send_data_package(socket, bet, login, color)
        slot = self.slot_storage.create_and_store_slot("get_response", self.get_response, socket)
        socket.readyRead.connect(slot)
        self.wait_for_readyRead(socket)

    def get_response(self, socket: QTcpSocket) -> None:
        """Получение значения с сервера для заполения списков игроков, сделавштх ставки
        result - булевая переменная: True - если у игрока хватает денег на балансе,
        False - если не хватает. При False высвечивать сообщение об ошибке стваки!"""

        data: tuple[bool, int, str, str] | None = self.recieve_data_package(socket, bool, int, str, str)
        if data is None:
            return

        (result, bet, login, color) = data

        self.responseRecieved.emit(result, bet, login, color)

    def make_a_bet(self, bet: int, login: str, color: str) -> None:
        with QMutexLocker(self.mutex):
            if self.is_running():
                return
            self.bet = bet
            self.login = login
            self.color = color
            self.start()
