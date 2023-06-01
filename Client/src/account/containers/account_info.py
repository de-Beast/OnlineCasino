import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import Signal

from Shared.abstract import SocketContainerBase
from Shared.account import AccountInfo
from Shared.sockets import SocketThreadType


class AccountInfoSocketContainer(SocketContainerBase):
    socket_type = SocketThreadType.ACCOUNT_INFO

    responseRecieved = Signal(AccountInfo)

    _requestInfo = Signal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        slot = self.slot_storage.create_slot(self.make_request)
        self._requestInfo.connect(slot)

    def run(self, login: str) -> None:
        self._requestInfo.emit(login)

    def exit(self) -> None:
        super().exit()
        self.socket.readyRead.disconnect(self.slot_storage.pop("get_response"))

    def make_request(self, login: str) -> None:
        slot = self.slot_storage.create_and_store_slot("get_response", self.get_response)
        self.socket.readyRead.connect(slot)

        self.send_data_package(login)

    def get_response(self) -> None:
        data: tuple[AccountInfo] | None = self.recieve_data_package(dict)
        if data is None:
            return

        (info,) = data

        self.responseRecieved.emit(info)

    def get_account_info(self, login: str) -> None:
        self._requestInfo.emit(login)
