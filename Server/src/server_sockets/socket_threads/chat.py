from typing import TYPE_CHECKING

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import QMutexLocker, QObject, Signal
from PySide6.QtNetwork import QTcpSocket

from Shared.sockets.enums import SocketThreadType

from .ABC import ServerSocketThread

if TYPE_CHECKING:
    from server_sockets.chat_manager import ChatRoom


class ChatSocketThread(ServerSocketThread):
    messageRecieved = Signal(str, str)

    socket_type = SocketThreadType.CHAT

    def __init__(self, socket_descriptor: int, chat_room: "ChatRoom", parent: QObject | None = None):
        super().__init__(socket_descriptor, parent)

        self.nickname: str
        self.message: str

        self.chat_room = chat_room
        self.need_to_send = False

        # slot = self.slot_storage.create_and_store_slot("remove_from_list", self.chat_room.socket_threads.remove, self)
        # self.finished.connect(slot)

    def thread_workflow(self, socket: QTcpSocket) -> None:
        self.send_data_package(socket, True)
        slot = self.slot_storage.create_and_store_slot("recieve_message", self.recieve_message, socket)
        socket.readyRead.connect(slot)

        # slot = self.slot_storage.create_and_store_slot("send_message", self.send_message, socket)
        # self.chat_room.messageRecieved.connect(slot)
        # self.exec()

        while self.is_working:
            self.wait_for_readyRead(socket, 1000)
            self.try_to_send(socket)

    def recieve_message(self, socket: QTcpSocket) -> None:
        data: tuple[str, str] | None = self.recieve_data_package(socket, str, str)
        if data is None:
            return

        (nickname, message) = data

        self.chat_room.messageRecieved.emit(nickname, message)

    # def send_message(self, socket: QTcpSocket, nickname: str, message: str) -> None:
    #     self.send_data_package(socket, nickname, message)

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
