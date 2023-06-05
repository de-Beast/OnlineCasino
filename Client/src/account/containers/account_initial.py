import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import Signal

from abstract import ClientSocketContainer
from Shared.account import AccountInitialRequest, AccountInitialResponse
from Shared.sockets import SocketType


class AccountInitialSocketContainer(ClientSocketContainer):
    socket_type = SocketType.ACCOUNT_INITIAL

    responseReceived = Signal(AccountInitialResponse)

    start = Signal(str, str, AccountInitialRequest)

    def on_start(self, login: str, password: str, method: AccountInitialRequest) -> None:
        super().on_start()

        self.readyRead.connect(self.get_response)

        self.send_data_package(login, password, method)

    def get_response(self) -> None:
        data = self.receive_data_package(AccountInitialResponse)
        if data is None:
            return

        (response,) = data

        self.responseReceived.emit(response)
        self.quit()
