import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import QMutexLocker, QObject, Signal
from PySide6.QtNetwork import QTcpSocket

from Shared.sockets.enums import SocketThreadType

from .ABC import ClientSocketThread


class ChatSocketThread(ClientSocketThread):
    responseRecieved = Signal(str, str)
    readyToSendMessage = Signal(str, str)

    socket_type = SocketThreadType.CHAT

    def __init__(self, chat_room: str = "roulette", parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.message: str
        self.nickname: str

        self.chat_room = chat_room
        self.need_to_send = False

    def thread_workflow(self, socket: QTcpSocket) -> None:
        with QMutexLocker(self.mutex):
            chat_room = self.chat_room

        slot = self.slot_storage.create_slot(self.get_connection_status, socket)
        socket.readyRead.connect(slot)
        self.send_data_package(socket, chat_room)

        self.wait_for_readyRead(socket)
        socket.readyRead.disconnect(slot)

        slot = self.slot_storage.create_and_store_slot("recieve_message", self.recieve_message, socket)
        socket.readyRead.connect(slot)

        # slot = self.slot_storage.create_and_store_slot("send_message", self._send_message, socket)
        # self.readyToSendMessage.connect(slot)

        # self.exec()

        while self.is_working:
            self.wait_for_readyRead(socket, 1000)
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

    # def _send_message(self, socket: QTcpSocket, nickname: str, message: str) -> None:
    #     self.send_data_package(socket, nickname, message)

    # def send_message(self, nickname: str, message: str) -> None:
    #     self.readyToSendMessage.emit(nickname, message)

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
