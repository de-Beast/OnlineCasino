from enum import Enum

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_properties  # type: ignore # noqa: F401
from PySide6.QtCore import QDataStream, QMutexLocker, QObject, Signal
from PySide6.QtNetwork import QTcpSocket

from .ABC import ServerSocketThreadABC, ThreadABC
from .database_socket_threads import AccountSocketThread, AuthenticationSocketThread


class SocketThreadType(Enum):
    AUTHENTIFICATION: int = 0
    ACCOUNT: int = 1


class SocketThreadFactory(ThreadABC):
    result = Signal(ServerSocketThreadABC)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.start()

    def run(self) -> None:
        """
        Эта функция запускает цикл, который ожидает дескриптор сокета, создает из него `QTcpSocket` и
        подключает его к сигналу `readyRead`
        """

        while True:
            with QMutexLocker(self.mutex):
                # self.mutex.lock()
                self.cond.wait(self.mutex)
                socket_descriptor = self._socket_descriptor
            # self.mutex.unlock()
            print(f"run: {socket_descriptor}")
            if socket_descriptor is None:
                self.error.emit("Socket descriptor is None")
                continue

            socket = QTcpSocket()
            if not socket.set_socket_descriptor(socket_descriptor):
                self.error.emit("Socket is already created")
                continue

            socket.readyRead.connect(lambda: self.on_readyRead(socket))
            while socket.wait_for_ready_read(self.wait_timeout):
                pass
            del socket

    def define_socket_thread(self, socket_descriptor: int) -> None:
        """
        Устанавливает дескриптор сокета и пробуждает ожидающий поток

        ### Параметры
        - `socket_descriptor: int`

        Дескриптор передается в качестве параметра
        и сохраняется в атрибуте `_socket_descriptor` объекта
        """

        print(f"define_socket_thread: {socket_descriptor}")
        self._socket_descriptor = socket_descriptor
        self.cond.wake_one()

    def on_readyRead(self, socket: QTcpSocket) -> None:
        """
        Вызывается, когда данные готовы для чтения из `QTcpSocket`
        (сокет активирует сигнал `readyRead`). Определяет, какой тип потока сокета следует использовать
        для обработки данных

        ### Параметры
        - `socket: QTcpSocket`

        Сокет, в котором есть данные, готовые для чтения.
        """

        recieve_stream = QDataStream(socket)
        recieve_stream.start_transaction()
        socket_thread_type_value = recieve_stream.read_int32()
        if not recieve_stream.commit_transaction():
            return

        try:
            socket_thread_type = SocketThreadType(socket_thread_type_value)
        except ValueError:
            self.error.emit("Invalid socket thread type")
            return
        else:
            self.create_socket_thread(socket_thread_type, socket.socket_descriptor())

    def create_socket_thread(self, socket_thread_type: SocketThreadType, socket_descriptor: int) -> None:
        """
        Создает поток сокета и активирует сигнал `result`, передавая в него созданный поток

        ### Параметры
        - `socket_thread_type: SocketThreadType`

        `SocketThreadType` является перечислением, который определяет различные
        типы потоков сокетов

        - `socket_descriptor: int`

        Дескриптор для создания сокета
        """

        socket_thread: ServerSocketThreadABC
        match socket_thread_type:
            case SocketThreadType.AUTHENTIFICATION:
                socket_thread = AuthenticationSocketThread(socket_descriptor)
            case SocketThreadType.ACCOUNT:
                socket_thread = AccountSocketThread(socket_descriptor)

        self.result.emit(socket_thread)
