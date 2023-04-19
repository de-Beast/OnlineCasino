import PySide6  # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtNetwork import QTcpServer
from PySide6.QtWidgets import QApplication

from server_sockets import (
    ServerSocketThread,
    AuthorizationSocketThread,
    AccountSocketThread,
    ServerSocketThreadFactory,
)
from Shared.sockets import SocketThreadType


class Server(QTcpServer):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._sockets: list[ServerSocketThread] = []

        self._socket_thread_factory = ServerSocketThreadFactory()
        self._socket_thread_factory.socketIdentified.connect(self.create_socket_thread)

        if not self.listen(port=8888):
            print(self.error_string())
            sys.exit(self.error_string())

    def incoming_connection(self, handle: int) -> None:
        self._socket_thread_factory.identify_socket(handle)

    def create_socket_thread(self, socket_thread_type: SocketThreadType, socket_descriptor: int) -> None:
        socket_thread: ServerSocketThread
        match socket_thread_type:
            case SocketThreadType.AUTHORIZATION:
                socket_thread = AuthorizationSocketThread(socket_descriptor)
            case SocketThreadType.ACCOUNT:
                socket_thread = AccountSocketThread(socket_descriptor)

        socket_thread.start()
        self._sockets.append(socket_thread)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    server = Server()
    sys.exit(app.exec())
