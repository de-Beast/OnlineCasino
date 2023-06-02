import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import Signal

from Shared.abstract import SocketContainerBase
from Shared.account import AccountInitialRequest, AccountInitialResponse
from Shared.sockets import SocketType


class AccountInitialSocketContainer(SocketContainerBase):
    socket_type = SocketType.ACCOUNT_INITIAL

    responseRecieved = Signal(AccountInitialResponse)

    _accountRequest = Signal(str, str, AccountInitialRequest)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        slot = self.slot_storage.create_slot(self.make_request)
        self._accountRequest.connect(slot)

    def run(self, login: str, password: str, method: AccountInitialRequest) -> None:
        self._accountRequest.emit(login, password, method)

    def exit(self) -> None:
        super().exit()
        self.socket.readyRead.disconnect(self.slot_storage.pop("get_response"))

    def make_request(self, login: str, password: str, method: AccountInitialRequest) -> None:
        slot = self.slot_storage.create_and_store_slot("get_response", self.get_response)
        self.socket.readyRead.connect(slot)

        self.send_data_package(method, login, password)

    def get_response(self) -> None:
        data: tuple[AccountInitialResponse] | None = self.recieve_data_package(AccountInitialResponse)
        if data is None:
            return

        (response,) = data

        self.responseRecieved.emit(response)
        self.quit()
