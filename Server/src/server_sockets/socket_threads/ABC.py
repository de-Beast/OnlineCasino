# from abc import abstractmethod
from abc import ABC
from typing import TYPE_CHECKING, ClassVar, Literal, Type, overload

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtCore import QMutexLocker, QObject
from PySide6.QtNetwork import QTcpSocket

from Shared.sockets import SocketThreadBase
from Shared.sockets.enums import SocketThreadType

if TYPE_CHECKING:
    from .account_info import AccountInfoSocketThread
    from .account_initial import AccountInitialSocketThread
    from .chat import ChatSocketThread


class ServerSocketThread(SocketThreadBase):
    """
    Базовый класс для серверных сокетов.

    ### Абстрактные методы
    >>> def thread_workflow(self, socket: QTcpSocket) -> None: ...

    Главный метод, в котором происходят основные вычисления потока.
    Должен быть обязательно переопределён. Не имеет базовой реализации
    """

    __socket_type_bindings: dict[SocketThreadType, Type["ServerSocketThread"]] = {}

    socket_type: ClassVar[SocketThreadType]

    @classmethod
    def __init_subclass__(cls, **kwards) -> None:
        super().__init_subclass__(**kwards)

        if not hasattr(cls, "socket_type") or not isinstance(cls.socket_type, SocketThreadType):
            raise TypeError("socket_type must be a Class variable of SocketThreadType enum")

        if ServerSocketThread.__socket_type_bindings.get(cls.socket_type, None) is not None:
            raise RuntimeError("Can not create subclass with the same socket type")

        ServerSocketThread.__socket_type_bindings.update({cls.socket_type: cls})

    def __init__(self, socket_descriptor: int, parent: QObject | None = None) -> None:
        super().__init__(parent)

        if socket_descriptor is None:
            self.error.emit("Socket descriptor can not be None")
            return

        self._socket_descriptor = socket_descriptor

    @staticmethod
    def from_socket_type(
        socket_type: SocketThreadType, socket_descriptor: int, *args, parent: QObject | None = None
    ) -> "ServerSocketThread":
        """
        Создает поток сокета указанного типа, используя заданный дескриптор.

        ### Параметры
        - `socket_thread_type: SocketThreadType`
        - `socket_descriptor: int`

        ### Возвращает
        Потомка класса `ServerSocketThreadABC`
        """

        return ServerSocketThread.__socket_type_bindings[socket_type](socket_descriptor, *args, parent)  # type: ignore

    def run(self) -> None:
        import sys

        if sys.argv.count("debug_threads") > 0:
            import debugpy  # type: ignore

            debugpy.debug_this_thread()

        if (socket := self._create_socket()) is None:
            return

        socket.disconnected.connect(self.stop_work)

        self._is_working = True
        self.thread_workflow(socket)
        self._is_working = False
        self._disconnect_socket(socket)

    def _create_socket(self, *args, **kwargs) -> QTcpSocket | None:
        """
        Создаёт сокет, используя сохранённый дескриптор.
        Должен быть использован только в методе `run`.

        ### Возвращает

        `QTcpSocket` или `None`, если произошла ошибка.
        """

        with QMutexLocker(self.mutex):
            socket_descriptor = self._socket_descriptor

        if socket_descriptor is None:
            self.error.emit("Socket descriptor can not be None")
            return None

        socket = QTcpSocket()
        if not socket.set_socket_descriptor(socket_descriptor):
            print(socket.error_string())
            self.error.emit("Socket is already created")
            return None

        return socket
