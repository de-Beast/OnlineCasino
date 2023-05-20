import sys

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtNetwork import QTcpServer
from server_sockets import ServerSocketThread, ServerSocketThreadFactory

from Shared.slot_storage import SlotStorage
from Shared.sockets.enums import SocketThreadType
from server_sockets import ChatManager

class Server(QTcpServer):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._socket_threads: list[ServerSocketThread] = []

        self._socket_thread_factory = ServerSocketThreadFactory()
        self._socket_thread_factory.socketIdentified.connect(self.create_socket_thread)

        self.chat_manager = ChatManager()

        if not self.listen(port=8888):
            print(self.error_string())
            sys.exit(1)
        else:
            print("Server started")

    def incoming_connection(self, handle: int) -> None:
        self._socket_thread_factory.identify_socket(handle)

    def create_socket_thread(self, socket_thread_type: SocketThreadType, socket_descriptor: int) -> None:
        if socket_thread_type is SocketThreadType.CHAT:
            self.chat_manager.connect_to_chat_room(socket_descriptor)
            return
        socket_thread = ServerSocketThread.from_socket_type(socket_thread_type, socket_descriptor)
        socket_thread.finished.connect(SlotStorage.create_slot(self._socket_threads.remove, socket_thread))
        socket_thread.start()
        self._socket_threads.append(socket_thread)
