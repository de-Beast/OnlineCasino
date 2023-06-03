import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import Signal

from Shared.abstract import SocketContainerBase
from Shared.account import AccountInfo
from Shared.sockets import SocketType


class AccountInfoSocketContainer(SocketContainerBase):
    socket_type = SocketType.ACCOUNT_INFO

    responseReceived = Signal(AccountInfo)

    _requestInfo = Signal(str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        slot = self.slot_storage.create_slot(self.make_request)
        self._requestInfo.connect(slot)

    def run(self, login: str) -> None:
        self._requestInfo.emit(login)

    def exit(self) -> None:
        self.socket.readyRead.disconnect(self.slot_storage.pop("get_response"))
        super().exit()

    def make_request(self, login: str) -> None:
        slot = self.slot_storage.create_and_store_slot("get_response", self.get_response)
        self.socket.readyRead.connect(slot)

        self.send_data_package(login)

    def get_response(self) -> None:
        data: tuple[AccountInfo] | None = self.receive_data_package(dict)
        if data is None:
            return

        (info,) = data

        self.responseReceived.emit(info)
        self.quit()
