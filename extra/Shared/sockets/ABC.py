import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;

from abc import abstractmethod
from PySide6.QtNetwork import QTcpSocket
from Shared.abstract import ThreadABC


class SocketThreadABC(ThreadABC):
    """
    Абстрактный базовый класс для потоков сокетов

    ### Абстрактные методы

    >>> thread_workflow(self, socket: QTcpSocket) -> None
    >>> _create_socket(self, *args, **kwargs) -> QTcpSocket | None
    """

    @abstractmethod
    def thread_workflow(self, socket: QTcpSocket) -> None:
        raise NotImplementedError
    
    @abstractmethod
    def _create_socket(self, *args, **kwargs) -> QTcpSocket | None:
        raise NotImplementedError

    def wait_for_readyRead(self, socket: QTcpSocket) -> bool:
        """
        Ожидает прибытия полного пакета данных

        ### Параметры
        - `socket: QTcpSocket`

        ### Возвращает
        `True`, если весь пакет данных был принял без ошибок и не сработал таймаут, иначе `False`

        ### Пример

        В данном примере `self.wait_for_readyRead(socket)` прекратит работу,
        или когда из сокета будут будет получены `int32`, `bool` и `string` именно в таком порядке,
        или когда случится ошибка, или когда сработает таймаут
        >>> def thread_workflow(self, *args, **kwargs):
        >>>     ...
        >>>     socket.readyRead.connect(lambda: self.on_readyRead(socket))
        >>>     self.wait_for_readyRead(socket)
        >>>     ...
        >>>
        >>> def on_readyRead(self, socket):
        >>>     recieve_stream = QDataStream(socket)
        >>>     recieve_stream.start_transaction()
        >>>     socket_thread_type_value = recieve_stream.read_int32()
        >>>     socket_thread_type_value = recieve_stream.read_bool()
        >>>     socket_thread_type_value = recieve_stream.read_string()
        >>>     if not recieve_stream.commit_transaction():
        >>>         return
        """

        while True:
            if not socket.wait_for_ready_read(self.wait_timeout):
                print(socket.error_string())
                self.error.emit(socket.error_string())
                return False
            if socket.bytes_available() == 0:
                return True

    def _disconnect_socket(self, socket: QTcpSocket) -> None:
        """
        Отключает сокет от хоста, работает и на стороне клиента, и на стороне сервера.
        Ничего не делает, если сокет уже был отключён

        ### Параметры
        - `socket: QTcpSocket`
        """

        socket.disconnect_from_host()
        if socket.state() is not socket.SocketState.UnconnectedState:
            socket.wait_for_disconnected()
