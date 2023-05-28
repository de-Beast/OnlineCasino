import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import QMutexLocker, QObject, Signal
from PySide6.QtNetwork import QTcpSocket

from Shared.sockets.enums import SocketThreadType

from .ABC import ClientSocketThread


class AccountInfoSocketThread(ClientSocketThread):
    responseRecieved = Signal(dict)

    socket_type = SocketThreadType.ACCOUNT_INFO

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.login: str

    def thread_workflow(self, socket: QTcpSocket) -> None:
        with QMutexLocker(self.mutex):
            login = self.login

        self.send_data_package(socket, login)

        slot = self.slot_storage.create_and_store_slot("get_response", self.get_response, socket)
        socket.readyRead.connect(slot)
        self.wait_for_readyRead(socket)

    def get_response(self, socket: QTcpSocket) -> None:
        data: tuple[dict] | None = self.recieve_data_package(socket, dict)
        if data is None:
            return

        (info,) = data

        self.responseRecieved.emit(info)

    def get_account_info(self, login: str) -> None:
        if self.is_running():
            return

        with QMutexLocker(self.mutex):
            self.login = login
            self.start()
