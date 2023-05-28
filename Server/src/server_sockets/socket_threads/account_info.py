import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from database import AccountsDB
from PySide6.QtNetwork import QTcpSocket

from Shared.sockets.enums import SocketThreadType

from .ABC import ServerSocketThread


class AccountInfoSocketThread(ServerSocketThread):
    socket_type = SocketThreadType.ACCOUNT_INFO

    def thread_workflow(self, socket: QTcpSocket) -> None:
        slot = self.slot_storage.create_and_store_slot("recieve_request", self.recieve_request, socket)
        socket.readyRead.connect(slot)
        self.wait_for_readyRead(socket)

    def recieve_request(self, socket: QTcpSocket) -> None:
        data: tuple[str] | None = self.recieve_data_package(socket, str)
        if data is None:
            return

        (login,) = data

        info = AccountsDB().get_account_info(login)
        self.send_data_package(socket, info)
