import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtCore import QByteArray, QDataStream, QMutexLocker, QObject, Signal
from PySide6.QtNetwork import QTcpSocket

from Shared import SlotStorage
from Shared.abstract import ThreadBase
from Shared.sockets import SocketThreadBase
from Shared.sockets.enums import SocketThreadType

from .socket_threads import ChatSocketThread, ServerSocketThread


class ChatManager(QObject):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.chat_rooms: dict[str, ChatRoomTest] = {"roulette": ChatRoomTest(self)}
        self.sockets: list[QTcpSocket] = []

    def connect_to_chat_room(self, socket_descriptor: int) -> None:
        socket = QTcpSocket()
        if not socket.set_socket_descriptor(socket_descriptor):
            return
        self.sockets.append(socket)
        slot = SlotStorage.create_slot(self.sockets.remove, socket)
        socket.disconnected.connect(slot)
        chat_room: str | None = None
        while socket.wait_for_ready_read():
            recieve_stream = QDataStream(socket)
            recieve_stream.start_transaction()
            chat_room = recieve_stream.read_string()
            if recieve_stream.commit_transaction():
                break

        if chat_room is not None:
            self.chat_rooms[chat_room].add_socket(socket_descriptor)


class ChatRoom(QObject):
    messageRecieved = Signal(str, str)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._slot_storage = SlotStorage()
        self.socket_threads: list[ChatSocketThread] = []
        self.messageRecieved.connect(self.message_recieved)

    @property
    def slot_storage(self) -> SlotStorage:
        return self._slot_storage

    def add_socket(self, socket_descriptor: int) -> None:
        socket_thread: ChatSocketThread = ServerSocketThread.from_socket_type(
            SocketThreadType.CHAT, socket_descriptor, self
        )  # type: ignore
        self.socket_threads.append(socket_thread)

        slot = self.slot_storage.create_slot(self.remove_thread, socket_thread)
        socket_thread.finished.connect(slot)

        slot = self.slot_storage.create_slot(self.message_recieved, socket_thread)
        socket_thread.messageRecieved.connect(slot)

        self.messageRecieved.connect(socket_thread.send_message)

        socket_thread.start()

    def remove_thread(self, socket_thread: ChatSocketThread) -> None:
        self.socket_threads.remove(socket_thread)

    def message_recieved(self, nickname: str, message: str) -> None:
        for socket_thread in self.socket_threads:
            socket_thread.send_message(nickname, message)


class ChatRoomTest(ThreadBase):
    socketAdded = Signal(int)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._slot_storage = SlotStorage()
        # self.sockets: list[QTcpSocket]
        self.start()

    @property
    def slot_storage(self) -> SlotStorage:
        return self._slot_storage

    def thread_workflow(self, *args) -> None:
        sockets: list[QTcpSocket] = []
        slot = self.slot_storage.create_slot(self._add_socket, None, sockets)
        self.socketAdded.connect(slot)
        self.exec()

    def add_socket(self, socket_descriptor: int) -> None:
       self.socketAdded.emit(socket_descriptor)

    def _add_socket(self, sockets: list[QTcpSocket], socket_descriptor: int) -> None:
        socket = QTcpSocket()
        if not socket.set_socket_descriptor(socket_descriptor):
            print(socket.error_string())
            return
        
        sockets.append(socket)

        slot = self.slot_storage.create_slot(self.remove, socket, sockets)
        socket.disconnected.connect(slot)
        
        slot = self.slot_storage.create_slot(self.message_recieved, socket, sockets)
        socket.readyRead.connect(slot)

    def remove(self, socket: QTcpSocket, sockets: list[QTcpSocket]) -> None:
        sockets.remove(socket)
    
    def message_recieved(self, sender_socket: QTcpSocket, sockets: list[QTcpSocket]) -> None:
        recieve_stream = QDataStream(sender_socket)

        recieve_stream.start_transaction()
        nickname = recieve_stream.read_string()
        message = recieve_stream.read_string()
        if not recieve_stream.commit_transaction():
            return

        for socket in sockets:
            descriptor = socket.socket_descriptor()

            block = QByteArray()
            send_stream = QDataStream(block, QDataStream.OpenModeFlag.WriteOnly)
            send_stream.write_string(nickname)
            send_stream.write_string(message)
            print(f"{descriptor}: {socket.state()}, {socket.is_readable()}, {socket.is_writable()}")
            # socket.open(QTcpSocket.OpenModeFlag.ReadWrite)
            # socket.set_socket_state(QTcpSocket.SocketState.ConnectedState)
            print(f"{descriptor}: {socket.state()}, {socket.is_readable()}, {socket.is_writable()}")
            res = socket.write(block)
            print(f"{descriptor}: {socket.state()}, {socket.is_readable()}, {socket.is_writable()}, {res}")
            # res = socket.wait_for_bytes_written(-1)
            print(
                f"{descriptor}: {socket.state()}, {socket.is_readable()}, {socket.is_writable()}, {res}, {socket.error_string()}: {socket.error()}"
            )
            print(f"{descriptor}: {socket.bytes_available()}, {socket.bytes_to_write()}")
