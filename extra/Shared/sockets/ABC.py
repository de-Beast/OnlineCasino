from abc import ABC, abstractmethod
from typing import Type, TypeVar

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import QByteArray, QDataStream, QObject
from PySide6.QtNetwork import QTcpSocket

from Shared import SlotStorage
from Shared.abstract import ThreadABC

T = TypeVar("T", bound=object)


class SocketThreadABC(ThreadABC, ABC):
    """
    Абстрактный базовый класс для потоков сокетов

    ### Абстрактные методы

    #>>> thread_workflow(self, socket: QTcpSocket) -> None
    #>>> _create_socket(self, *args, **kwargs) -> QTcpSocket | None
    """

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self._slot_storage: SlotStorage = SlotStorage()

    @property
    def slot_storage(self) -> SlotStorage:
        return self._slot_storage

    @abstractmethod
    def thread_workflow(self, socket: QTcpSocket) -> None:
        raise NotImplementedError

    @abstractmethod
    def _create_socket(self, *args, **kwargs) -> QTcpSocket | None:
        raise NotImplementedError

    def wait_for_readyRead(self, socket: QTcpSocket, msecs: int | None = None) -> bool:
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
        >>>     recieve_stream = QDataStream(socket)
        >>>     recieve_stream.start_transaction()
        >>>     socket_thread_type_value = recieve_stream.read_int32()
        >>>     socket_thread_type_value = recieve_stream.read_bool()
        >>>     socket_thread_type_value = recieve_stream.read_string()
        >>>     if not recieve_stream.commit_transaction():
        >>>         return
        """

        while True:
            if not socket.wait_for_ready_read(self.wait_timeout if msecs is None else msecs):
                print(socket.error_string())
                self.error.emit(socket.error_string())
                return False
            if socket.bytes_available() == 0:
                return True

    def send_data_package(self, socket: QTcpSocket, *args: T) -> None:
        """
        Эта функция отправляет пакет данных через QTcpSocket.

        ### Параметры
        - `socket: QTcpSocket`

        - `*args: T`

        Объекты, которые нужно передать одним пакетом данных
        """

        block = QByteArray()
        send_stream = QDataStream(block, QDataStream.OpenModeFlag.WriteOnly)
        for data in args:
            if isinstance(data, bool):
                send_stream.write_bool(data)
            elif isinstance(data, int):
                send_stream.write_int32(data)
            elif isinstance(data, float):
                send_stream.write_float(data)
            elif isinstance(data, str):
                send_stream.write_string(data)
            else:
                send_stream.writeQVariant(data)

        socket.write(block)
        socket.wait_for_bytes_written(self.wait_timeout)

    def recieve_data_package(self, socket: QTcpSocket, *args: Type[T]):
        """
        Получает пакет данных из `QTcpSocket` и возвращает его в виде кортежа.

        Для `static type checker`'ов:

        Чтобы при расспаковке переменные были соответствующего типа,
        следует предварительно сделать аннотацию для кортежа:
        #>>> data: tuple[int, int, str, float] | None = self.recieve_data_package(socket, int, int, str, float)
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

        recieve_stream = QDataStream(socket)
        data: list = []
        recieve_stream.start_transaction()
        for type in args:
            if type is bool:
                data.append(recieve_stream.read_bool())
            elif type is int:
                data.append(recieve_stream.read_int32())
            elif type is float:
                data.append(recieve_stream.read_float())
            elif type is str:
                data.append(recieve_stream.read_string())
            else:
                data.append(recieve_stream.readQVariant())

        if not recieve_stream.commit_transaction():
            return None

        # Для static type checker'ов
        return_value: tuple[T, ...] = tuple(data)

        return return_value

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
