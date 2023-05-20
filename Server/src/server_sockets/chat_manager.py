import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtCore import QObject, QDataStream, QMutexLocker
from PySide6.QtNetwork import QTcpSocket
from Shared.sockets import SocketThreadABC
from Shared.sockets.enums import SocketThreadType
from .socket_threads import ChatSocketThread, ServerSocketThread


class ChatManager(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self.chat_rooms: dict[str, ChatRoom] = {"roulette": ChatRoom()}

    def connect_to_chat_room(self, socket_descriptor: int) -> None:
        socket = QTcpSocket()
        if not socket.set_socket_descriptor(socket_descriptor):
            return
        while socket.wait_for_ready_read():
            recieve_stream = QDataStream(socket)
            recieve_stream.start_transaction()
            chat_room = recieve_stream.read_string()
            if recieve_stream.commit_transaction():
                break
        del socket
        self.chat_rooms[chat_room].add_socket(socket_descriptor)

class ChatRoom(SocketThreadABC):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._socket_descriptor: int
        self.to_add_socket = False
        self.start()

    def thread_workflow(self, *args) -> None:
        socket_threads: list[ChatSocketThread] = []

        while self.is_working:
            with QMutexLocker(self.mutex):
                if not self.to_add_socket:
                    continue
                socket_descriptor = self._socket_descriptor
                self.to_add_socket = False
            socket = self._create_socket(socket_descriptor)
            socket_threads.append(socket)
            slot = self.slot_storage.create_slot(self.message_recieved, None, socket_threads)
            socket.messageRecieved.connect(slot)

    def message_recieved(self, socket_threads: list[ChatSocketThread], nickname: str, message: str) -> None:
        for socket_thread in socket_threads:
            socket_thread.send_message(nickname, message)

    def add_socket(self, socket_descriptor: int) -> None:
        with QMutexLocker(self.mutex):
            self._socket_descriptor = socket_descriptor
            self.to_add_socket = True

    def _create_socket(self, socket_descriptor: int) -> ChatSocketThread:
        return ServerSocketThread.from_socket_type(SocketThreadType.CHAT, socket_descriptor)
