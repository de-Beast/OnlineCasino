import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401

from database import AccountsDB
from Shared.abstract import SocketContainerBase
from Shared.sockets import SocketThreadType


class AccountInfoSocketContainer(SocketContainerBase):
    socket_type = SocketThreadType.ACCOUNT_INFO

    def run(self) -> None:
        slot = self.slot_storage.create_and_store_slot("recieve_request", self.recieve_request)
        self.socket.readyRead.connect(slot)
        self.recieve_request()

    def exit(self) -> None:
        super().exit()
        self.socket.readyRead.disconnect(self.slot_storage.pop("recieve_request"))

    def recieve_request(self) -> None:
        data: tuple[str] | None = self.recieve_data_package(str)
        if data is None:
            return

        (login,) = data

        info = AccountsDB().get_account_info(login)
        self.send_data_package(info)
        self.exit()
