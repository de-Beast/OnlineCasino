import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from database import AccountsDB
from PySide6.QtNetwork import QTcpSocket
from PySide6.QtCore import Signal, QMutexLocker, QObject

from roulette import Roulette
from Shared.sockets.enums import SocketThreadType, RouletteColor
from collections import namedtuple
from .ABC import ServerSocketThreadABC

BetAndColor = namedtuple("BetAndColor", ["bet", "color", "balance"])

class BetSocketThread(ServerSocketThreadABC):
    socket_type = SocketThreadType.BET

    def thread_workflow(self, socket: QTcpSocket) -> None:
        slot = self.slot_storage.create_and_store_slot("recieve_request", self.recieve_request, socket)
        socket.readyRead.connect(slot)
        self.wait_for_readyRead(socket)

    def recieve_request(self, socket: QTcpSocket) -> None:
        data: tuple[int, str, RouletteColor] | None = self.recieve_data_package(socket, int, str, RouletteColor)
        if data is None:
            return

        (bet, login, color) = data

        info = AccountsDB().get_account_info(login)

        balance = info["balance"]

        if balance < bet:
            self.send_data_package(socket, False, bet, login, color)
            return

        bet_n_color: BetAndColor[int, RouletteColor, int] = BetAndColor(bet, color, balance)
        bets_update = {login: bet_n_color}
        Roulette().bets.update(bets_update)

        self.send_data_package(socket, True, bet, login, color)

