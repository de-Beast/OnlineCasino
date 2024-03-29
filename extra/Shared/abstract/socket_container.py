__all__ = [
    "SocketContainerBase",
]

from abc import abstractmethod
from typing import ClassVar, Type, TypeVar

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import QByteArray, QDataStream, QObject, Signal
from PySide6.QtNetwork import QTcpSocket

from Shared.abstract import EnumBase, auto
from Shared.slot_storage import SlotStorage
from Shared.sockets import SocketType

from .ABC import QABC

T = TypeVar("T", bound=object)


class SocketContainerBase(QABC, QObject):
    __socket_type_bindings: dict[SocketType, Type["SocketContainerBase"]] = {}

    socket_type: ClassVar[SocketType]

    # Таймаут, используемый в `wait_` методах
    wait_timeout: int = 10_000  # milliseconds

    readyRead = Signal()
    start: ClassVar[Signal]
    exit = Signal()

    class ContainerRequest(EnumBase):
        CONNECT = auto()
        DISCONNECT = auto()

    @classmethod
    def __init_subclass__(cls, **kwards) -> None:
        super().__init_subclass__(**kwards)

        if not hasattr(cls, "socket_type") or not isinstance(cls.socket_type, SocketType):
            raise TypeError("socket_type must be a Class variable of SocketThreadType enum")

        if cls.socket_type is not SocketType.NONE and not (hasattr(cls, "start") and isinstance(cls.start, Signal)):
            raise TypeError("start must be a Class variable of Signal type")

        if SocketContainerBase.__socket_type_bindings.get(cls.socket_type, None) is not None:
            raise RuntimeError("Can not create subclass with the same socket type")

        if cls.socket_type is not SocketType.NONE:
            SocketContainerBase.__socket_type_bindings.update({cls.socket_type: cls})

    def __init__(self, socket: QTcpSocket, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._socket = socket
        self._slot_storage = SlotStorage()

        self.start.connect(self.on_start)
        self.exit.connect(self.on_exit)

    @property
    def socket(self) -> QTcpSocket:
        if self._socket is None:
            raise RuntimeError("Socket is None")

        return self._socket

    @property
    def slot_storage(self) -> SlotStorage:
        return self._slot_storage

    @staticmethod
    def create_container(
        socket: QTcpSocket, socket_type: SocketType, parent: QObject | None = None
    ) -> "SocketContainerBase":
        """
        Создает контейнер сокета указанного типа, считывая из сокета его тип

        ### Параметры
        - `socket: QTcpSocket`
        - `*args`
        - `*parent: QObject | None`

        ### Возвращает
        Потомка класса `SocketContainer`
        """

        return SocketContainerBase.__socket_type_bindings[socket_type](socket, parent)  # type: ignore

    def run(self, *args) -> None:
        self.start.emit(*args)

    @abstractmethod
    def on_start(self) -> None:
        raise NotImplementedError()

    def quit(self) -> None:
        self.exit.emit()

    def on_exit(self) -> None:
        pass

    def wait_for_readyRead(self, msecs: int | None = None) -> bool:
        """
        Ожидает прибытия полного пакета данных

        ### Параметры
        - `socket: QTcpSocket`

        ### Возвращает
        `True`, если весь пакет данных был принял без ошибок и не сработал таймаут, иначе `False`

        ### Пример

        В данном примере `self.wait_for_readyRead(socket)` прекратит работу,
        или когда из сокета будут будет получены `int32`, `bool` и `string`, именно в таком порядке,
        или когда случится ошибка, или когда сработает таймаут
        >>> def thread_workflow(self, *args, **kwargs):
        >>>     ...
        >>>     socket.readyRead.connect(self.on_readyRead)
        >>>     self.wait_for_readyRead(socket)
        >>>     ...
        >>>
        >>> def on_readyRead(self):
        >>>     socket = self.get_socket()
        >>>     receive_stream = QDataStream(socket)
        >>>     receive_stream.start_transaction()
        >>>     socket_thread_type_value = receive_stream.read_int32()
        >>>     socket_thread_type_value = receive_stream.read_bool()
        >>>     socket_thread_type_value = receive_stream.read_string()
        >>>     if not receive_stream.commit_transaction():
        >>>         return
        """

        while True:
            if not self.socket.wait_for_ready_read(self.wait_timeout if msecs is None else msecs):
                print(self.socket.error_string())
                return False
            if self.socket.bytes_available() == 0:
                return True

    def send_data_package(self, *args: T) -> None:
        """
        Эта функция отправляет пакет данных через QTcpSocket.

        ### Параметры
        - `socket: QTcpSocket`

        - `*args: T`

        Объекты, которые нужно передать одним пакетом данных
        """

        block = QByteArray()
        send_stream = QDataStream(block, QDataStream.OpenModeFlag.WriteOnly)
        send_stream.writeQVariant(self.socket_type)
        for data in args:
            send_stream.writeQVariant(data)

        self.socket.write(block)
        self.socket.wait_for_bytes_written(self.wait_timeout)

    def receive_data_package(self, *args: Type[T]) -> tuple[T] | None:
        """
        Получает пакет данных из `QTcpSocket` и возвращает его в виде кортежа.

        Для `static type checker`'ов:

        Чтобы при расспаковке переменные были соответствующего типа,
        следует предварительно сделать аннотацию для кортежа:
        #>>> data: tuple[int, int, str, float] | None = self.receive_data_package(socket, int, int, str, float)
        #>>> if data is None:
        #>>>     return
        #>>> num, index, string, delta = data
        Так перменные `num`, `index`, `string`, `delta` будут, соответственно, с аннотациями `int`, `int`, `str` и `float`

        ### Параметры
        - `socket: QTcpSocket`

        - `*args: Type[T]`

        Принимает типы объектов, которые нужно получить из пакета данных,
        от порядка аргументов зависит порядок принимаемых объектов,
        поэтому от разработчика зависит что и в каком порядке ожидается для получения.
        `Undefined behavior`, если порядок или типы не совпадают с теми, что находятся в поступающем пакете

        ### Возвращает
        Кортёж объектов тех типов, что были переданы, в том же порядке.
        `None`, если был получен неполный пакет данных

        """  # noqa: E501

        receive_stream = QDataStream(self.socket)
        receive_stream.start_transaction()
        socket_type = receive_stream.readQVariant()
        if not isinstance(socket_type, SocketType) or socket_type is not self.socket_type:
            receive_stream.rollback_transaction()
            return None

        data: list = []
        for type in args:
            data.append(receive_stream.readQVariant())

            if not isinstance(data[-1], type):
                receive_stream.rollback_transaction()
                return None

        if not receive_stream.commit_transaction():
            return None

        return_value: tuple[T] = tuple(data)  # type: ignore

        return return_value
