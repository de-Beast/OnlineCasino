import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import QMutexLocker, QObject, Signal, QThread
from PySide6.QtNetwork import QTcpSocket

from Shared.sockets.enums import SocketThreadType

from .ABC import ClientSocketThreadABC
from .Client import Client

class ChatSocketThread (ClientSocketThreadABC):

    responseRecieved = Signal(str, str)

    socket_type = SocketThreadType.CHAT

    def __init__(self, parent: QObject | None = None, chat_room: str = "roulette") -> None:
        super().__init__(parent)

        self.message: str
        self.nickname: str
        self.chat_room = chat_room
        self.need_to_send = False
        self.start()

    def thread_workflow(self, socket: QTcpSocket) -> None:
        with QMutexLocker(self.mutex):
            chat_room = self.chat_room

        self.send_data_package(socket, chat_room)

        slot = self.slot_storage.create_slot(self.get_connection_status, socket)
        socket.readyRead.connect(slot)
        self.wait_for_readyRead(socket)
        socket.readyRead.disconnect(slot)

        slot = self.slot_storage.create_and_store_slot("recieve_message", self.recieve_message, socket)
        socket.readyRead.connect(slot)
        while self.is_working:
            self.try_to_send(socket)

    def get_connection_status(self, socket: QTcpSocket) -> None:
        data: tuple[bool] | None = self.recieve_data_package(socket, bool)
        if data is None:
            return

        (connection_status,) = data

        if not connection_status:
            self.stop_work()

    def recieve_message(self, socket: QTcpSocket) -> None:
        data: tuple[str, str] | None = self.recieve_data_package(socket, str, str)
        if data is None:
            return

        (nickname, message) = data

        self.responseRecieved.emit(nickname, message)

    def send_message(self, nickname: str, message: str) -> None:
        with QMutexLocker(self.mutex):
            self.nickname = nickname
            self.message = message
        self.need_to_send = True
        print(self.need_to_send)

    def try_to_send(self, socket: QTcpSocket) -> None:
        if not self.need_to_send:
            return
        with QMutexLocker(self.mutex):
            message = self.message
            nickname = self.nickname
        self.need_to_send = False

        self.send_data_package(socket, nickname, message)

