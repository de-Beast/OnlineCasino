import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401

from abstract import ServerSocketContainer
from database import AccountsDB
from Shared.sockets import SocketType


class AccountInfoSocketContainer(ServerSocketContainer):
    socket_type = SocketType.ACCOUNT_INFO

    def on_start(self) -> None:
        self.readyRead.connect(self.receive_request)

    def receive_request(self) -> None:
        data = self.receive_data_package(str)
        if data is None:
            return

        (login,) = data

        info = AccountsDB().get_account_info(login)
        self.send_data_package(info)
