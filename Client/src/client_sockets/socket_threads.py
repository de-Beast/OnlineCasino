import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import QByteArray, QDataStream, QMutexLocker, QObject, Signal
from PySide6.QtNetwork import QTcpSocket

from .ABC import ClientSocketThreadABC
from Shared.sockets import SocketThreadType


class AuthorizationSocketThread(ClientSocketThreadABC):
    """
    Поток для обработки запросов, связанных с авторизацией (регистрацией)
    """
    
    # Активируется после того, как сервер прислал ответ о попытке войти или зарегистрироваться.
    # Передаёт в сигнал ответ сервера в виде строки
    answerRecieved = Signal(str)
    
    # Переменная класса, определяющая тип потока, передаётся серверу.
    # Не может быть двух классов с одинаковым типом потока
    socket_type = SocketThreadType.AUTHORIZATION

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.login: str
        self.password: str
        self.sign_up: bool

    def auth(self, login: str, password: str, *, sign_up: bool = False) -> None:
        """
        Принимает и сохраняет логин, пароль и флаг `sign_up` для определения запроса в дальнейшем.
        Запускает поток.
        
        ### Параметры
        
        - `login: str`
        Строка, представляющая логин (имя пользователя) для аутентификации
        
        - `password: str`
        Строка, представляющая пароль пользователя
        
        - `sign_up: bool = False`
        Параметр `sign_up` представляет собой логический флаг, указывающий, выполняется ли
        регистрация нового пользователя (`True`) или вход в существующий аккаунт (`False`)
        """
        
        with QMutexLocker(self.mutex):
            self.login = login
            self.password = password
            self.sign_up = sign_up
            if not self.is_running():
                self.start()

    def thread_workflow(self, socket: QTcpSocket) -> None:
        with QMutexLocker(self.mutex):
            login = self.login
            password = self.password
            sign_up = self.sign_up

        block = QByteArray()
        send_stream = QDataStream(block, QDataStream.OpenModeFlag.WriteOnly)
        send_stream.write_string(login)
        send_stream.write_string(password)
        send_stream.write_bool(sign_up)
        socket.write(block)

        socket.readyRead.connect(lambda: self.on_readyRead(socket))
        self.wait_for_readyRead(socket)

    def on_readyRead(self, socket: QTcpSocket) -> None:
        recieve_stream = QDataStream(socket)
        recieve_stream.start_transaction()

        answer = recieve_stream.read_string()
        if not recieve_stream.commit_transaction():
            return

        self.answerRecieved.emit(answer)
