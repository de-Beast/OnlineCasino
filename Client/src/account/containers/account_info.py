import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import Signal

from abstract import ClientSocketContainer
from Shared.account import AccountInfo
from Shared.sockets import SocketType


class AccountInfoSocketContainer(ClientSocketContainer):
    socket_type = SocketType.ACCOUNT_INFO

    start = Signal(str)
    responseReceived = Signal(AccountInfo)

    def on_start(self, login: str) -> None:
        super().on_start()

        self.readyRead.connect(self.get_response)

        self.send_data_package(login)

    def get_response(self) -> None:
        data: tuple[AccountInfo] | None = self.receive_data_package(dict)
        if data is None:
            return
        (info,) = data

        self.responseReceived.emit(info)
        self.quit()
