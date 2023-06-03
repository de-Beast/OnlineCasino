import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401

from database import AccountsDB
from Shared.abstract import SocketContainerBase
from Shared.sockets import SocketType


class AccountInfoSocketContainer(SocketContainerBase):
    socket_type = SocketType.ACCOUNT_INFO

    def run(self) -> None:
        self.receive_request()

        slot = self.slot_storage.create_and_store_slot("receive_request", self.receive_request)
        self.socket.readyRead.connect(slot)

    def exit(self) -> None:
        self.socket.readyRead.disconnect(self.slot_storage.pop("receive_request"))
        super().exit()

    def receive_request(self) -> None:
        data: tuple[str] | None = self.receive_data_package(str)
        if data is None:
            return

        (login,) = data

        info = AccountsDB().get_account_info(login)
        self.send_data_package(info)
