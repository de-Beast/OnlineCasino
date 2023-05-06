# from abc import abstractmethod
from typing import ClassVar

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import QMutexLocker, QObject, Signal
from PySide6.QtNetwork import QHostAddress, QTcpSocket

from Shared.sockets import SocketThreadABC
from Shared.sockets.enums import SocketThreadType

# TODO Класс для хранения и работы с лямбда-функциями, которые можно к объектам SignalInstance присоединять


class ClientSocketThreadABC(SocketThreadABC):
    """
    Базовый класс для клиентских сокетов.

    ### Абстрактные методы
    >>> def thread_workflow(self, socket: QTcpSocket) -> None: ...

    Главный метод, в котором происходят основные вычисления потока.
    Должен быть обязательно переопределён. Не имеет базовой реализации
    """

    __socket_types: set[SocketThreadType] = set()

    # В наследнике должен быть инициализирован, иначе выкинется исключение.
    # Значение не должно быть использовано другими наследниками
    socket_type: ClassVar[SocketThreadType]

    # В наследнике должен быть инициализирован, иначе выкинется исключение.
    # Принимаемый(-ые) типы у наследников могут быть разные
    responseRecieved: ClassVar[Signal]

    @classmethod
    def __init_subclass__(cls, **kwargs) -> None:
        super().__init_subclass__(**kwargs)

        if not hasattr(cls, "responseRecieved") or not isinstance(cls.responseRecieved, Signal):
            raise TypeError("responseRecieved must be a Class variable of Signal type")

        if not hasattr(cls, "socket_type") or not isinstance(cls.socket_type, SocketThreadType):
            raise TypeError("socket_type must be a Class variable of SocketThreadType enum")

        if cls.socket_type in ClientSocketThreadABC.__socket_types:
            raise RuntimeError("Can not create subclass with the same socket type")

        ClientSocketThreadABC.__socket_types.add(cls.socket_type)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.__is_connected: bool

    def run(self) -> None:
        import sys

        if sys.argv.count("debug_threads") > 0:
            import debugpy  # type: ignore

            debugpy.debug_this_thread()

        if (socket := self._create_socket()) is None:
            return

        self._send_socket_type(socket)
        if not self.wait_for_readyRead(socket):
            print("Can not get connection answer from host")
            return

        if not self.__is_connected:
            self._disconnect_socket(socket)
            return

        self._is_working = True
        self.thread_workflow(socket)
        self._is_working = False
        self._disconnect_socket(socket)

    def _create_socket(self) -> QTcpSocket | None:
        """
        Создает сокет и присодиняет его к хосту.
        Должен быть использован только в методе `run`.

        ### Возвращает

        QTcpSocket или None, если не удалось присоединиться к хосту
        """

        host = QHostAddress(QHostAddress.SpecialAddress.LocalHost)
        port = 8888

        socket = QTcpSocket()
        socket.connect_to_host(host, port)
        if not socket.wait_for_connected(self.wait_timeout):
            print("Can not connect to the host")
            self.error.emit("Can not connect to the host")
            return None

        return socket

    def _send_socket_type(self, socket: QTcpSocket) -> None:
        """
        Посылает на сервер типа сокета, по которому тот определит, какой поток
        в качестве обработчика нужно будет использовать

        ### Параметры
        - `socket: QTcpSocket`
        """

        with QMutexLocker(self.mutex):
            socket_type = self.socket_type

        self.send_data_package(socket, socket_type)
        slot = self.slot_storage.create_and_store_slot(
            "_recieve_server_socket_connection", self._recieve_server_socket_connection, socket
        )
        socket.readyRead.connect(slot)

    def _recieve_server_socket_connection(self, socket: QTcpSocket) -> None:
        """
        Получает ответ от сервера о том, успешно ли сокет был распознан хостом

        ### Параметры
        - `socket: QTcpSocket`
        """

        data: tuple[bool] | None = self.recieve_data_package(socket, bool)
        if data is None:
            return

        (is_connected,) = data

        self.__is_connected = is_connected
        socket.readyRead.disconnect(self.slot_storage.pop("_recieve_server_socket_connection"))
