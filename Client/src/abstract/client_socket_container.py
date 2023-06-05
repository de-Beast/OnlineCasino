import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtCore import QByteArray, QDataStream

from Shared.abstract import SocketContainerBase
from Shared.sockets import SocketType


class ClientSocketContainer(SocketContainerBase):
    socket_type = SocketType.NONE

    def on_start(self, *args, **kwargs) -> None:
        self.send_container_request(SocketContainerBase.ContainerRequest.CONNECT)

    def send_container_request(self, request: SocketContainerBase.ContainerRequest) -> None:
        block = QByteArray()
        send_stream = QDataStream(block, QDataStream.OpenModeFlag.WriteOnly)
        send_stream.writeQVariant(request)
        send_stream.writeQVariant(self.socket_type)
        self.socket.write(block)
        self.socket.wait_for_bytes_written(self.wait_timeout)

    def on_exit(self) -> None:
        self.send_container_request(SocketContainerBase.ContainerRequest.DISCONNECT)
