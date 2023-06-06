import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtCore import QDataStream, Signal
from PySide6.QtNetwork import QTcpSocket

from Shared.abstract import SocketContainerBase
from Shared.sockets import SocketType


class ServerSocketContainer(SocketContainerBase):
    socket_type = SocketType.NONE
    
    start = Signal()

    @staticmethod
    def receive_container_request(
        socket: QTcpSocket,
    ) -> tuple[SocketContainerBase.ContainerRequest | None, SocketType | None]:
        receive_stream = QDataStream(socket)
        receive_stream.start_transaction()
        data = receive_stream.readQVariant()
        if isinstance(data, SocketContainerBase.ContainerRequest):
            container_request = data
            receive_stream.commit_transaction()

            receive_stream.start_transaction()
            data = receive_stream.readQVariant()
            if isinstance(data, SocketType):
                receive_stream.commit_transaction()
                return container_request, data
            else:
                receive_stream.rollback_transaction()
                return container_request, None
        receive_stream.rollback_transaction()
        return None, None
