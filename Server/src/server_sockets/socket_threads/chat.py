import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtNetwork import QTcpSocket
from PySide6.QtCore import Signal, QMutexLocker, QObject

from Shared.sockets.enums import SocketThreadType

from .ABC import ServerSocketThreadABC


class ChatSocketThread(ServerSocketThreadABC):
    messageRecieved = Signal(str, str)

    socket_type = SocketThreadType.CHAT

    def __init__(self, parent: QObject | None = None):
        super().__init__(parent)
        self.need_to_send = False
        self.nickname: str
        self.message: str

    def thread_workflow(self, socket: QTcpSocket) -> None:
        self.send_data_package(socket, True)
        slot = self.slot_storage.create_and_store_slot("recieve_message", self.recieve_message, socket)
        socket.readyRead.connect(slot)
        while self.is_working:
            self.try_to_send(socket)

    def recieve_message(self, socket: QTcpSocket) -> None:
        data: tuple[str, str] | None = self.recieve_data_package(socket, str, str)
        if data is None:
            return

        (nickname, message) = data

        self.messageRecieved.emit(nickname, message)

    def send_message(self, nickname: str, message: str) -> None:
        with QMutexLocker(self.mutex):
            self.nickname = nickname
            self.message = message
            self.need_to_send = True

    def try_to_send(self, socket: QTcpSocket) -> None:
        with QMutexLocker(self.mutex):
            if not self.need_to_send:
                return
            message = self.message
            nickname = self.nickname
            self.need_to_send = False

        self.send_data_package(socket, nickname, message)