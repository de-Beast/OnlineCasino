import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtCore import QByteArray, QDataStream, QMutexLocker, Signal
from PySide6.QtNetwork import QTcpSocket

# from .ABC import ServerSocketThreadABC
# from .socket_threads import AccountSocketThread, AuthenticationSocketThread
from Shared.sockets import SocketThreadABC, SocketThreadType


class ServerSocketThreadFactory(SocketThreadABC):
    """
    Специальный класс для определения необходимого для корректной
    связи с клиентом потока. Рабочий процесс заключен в цикл, постоянно обрабатывая
    поступающие серверу сокеты 
    """

    # Активируется, когда класс определил необходимый типа потока, передаёт типа потока и дескриптор сокета
    socketIdentified = Signal(SocketThreadType, int)

    def thread_workflow(self, *args) -> None:
        """
        Запускает цикл, в котором обрабатываются только что подключенные к хосту сокеты.
        Определяется, какого типа поток нужно будет создать

        ### Параметры
        - `*args`

        Пустой кортеж, не используется, существует для совместимости с базовым классом
        """

        with QMutexLocker(self.mutex):
            socket_descriptor = self._socket_descriptor

        while self.is_working:
            socket = self._create_socket(socket_descriptor)
            if socket is not None:
                socket.readyRead.connect(lambda: self._recieve_socket_thread_type(socket))
                self.wait_for_readyRead(socket)

            with QMutexLocker(self.mutex):
                self.cond.wait(self.mutex)
                socket_descriptor = self._socket_descriptor

    def identify_socket(self, socket_descriptor: int) -> None:
        """
        Сохраняется переданный дескриптор, затем поток запускается или пробуждается

        ### Параметры
        - `socket_descriptor: int`

        Дескриптор сохраняется в атрибуте `_socket_descriptor`
        """

        self._socket_descriptor = socket_descriptor
        if not self.is_running():
            self.start()
        else:
            self.cond.wake_one()

    def _create_socket(self, socket_descriptor: int) -> QTcpSocket | None:
        """
        Создает сокет с помощью переданного дескриптора

        ### Возвращает

        QTcpSocket или None, если не удалось присоединиться к хосту
        """

        socket = QTcpSocket()
        if not socket.set_socket_descriptor(socket_descriptor):
            self.error.emit("Socket is already created")
            return None

        return socket

    def _recieve_socket_thread_type(self, socket: QTcpSocket) -> None:
        """
        Вызывается, когда данные готовы для чтения из `QTcpSocket`
        (сокет активирует сигнал `readyRead`). Определяет, какой тип потока сокета следует использовать
        для обработки данных. Вызывает `socketIdentified` при успешной соединении

        ### Параметры
        - `socket: QTcpSocket`

        Сокет, в котором есть данные, готовые для чтения.
        """

        recieve_stream = QDataStream(socket)
        recieve_stream.start_transaction()
        socket_thread_type_value = recieve_stream.read_int32()
        if not recieve_stream.commit_transaction():
            return

        connection_status = True
        try:
            socket_thread_type = SocketThreadType(socket_thread_type_value)
        except ValueError:
            self.error.emit("Invalid socket thread type")
            connection_status = False

        self._send_socket_connection(socket, connection_status)
        if not connection_status:
            return

        self.socketIdentified.emit(socket_thread_type, socket.socket_descriptor())

    def _send_socket_connection(self, socket: QTcpSocket, connection_status: bool) -> None:
        block = QByteArray()
        send_stream = QDataStream(block, QDataStream.OpenModeFlag.WriteOnly)
        send_stream.write_bool(connection_status)
        socket.write(block)
        socket.wait_for_bytes_written(self.wait_timeout)
