import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import QByteArray, QDataStream, QMutexLocker, QObject, Signal
from PySide6.QtNetwork import QTcpSocket

from Shared.sockets.enums import AccountInitialRequest, AccountInitialResponse, SocketThreadType

from .ABC import ClientSocketThreadABC


class AccountInitialSocketThread(ClientSocketThreadABC):
    """
    Поток для обработки запросов, связанных с авторизацией и регистрацией

    Вызовите метод `auth`, чтобы запустить поток, который выполнит вход в аккаунт пользователя

    Вызовите метод `register`, чтобы запустить поток, который зарегистрирует пользователя
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
        self.request_method: AccountInitialRequest

    def auth(self, login: str, password: str) -> None:
        """
        Принимает и сохраняет логин и пароль для последующего входа в систему. Запускает поток.
        Не может быть запущен больше одного раза и, если был вызван метод `register`

        ### Параметры

        - `login: str`
        Строка, представляющая логин (имя пользователя) для аутентификации

        - `password: str`
        Строка, представляющая пароль пользователя
        """

        with QMutexLocker(self.mutex):
            if self.is_running():
                return

            self.login = login
            self.password = password
            self.request_method = AccountInitialRequest.AUTH
            self.start()

    def register(self, login: str, password: str) -> None:
        """
        Принимает и сохраняет логин и пароль для последующей регистрации пользователя в системе. Запускает поток.
        Не может быть запущен больше одного раза и, если был вызван метод `auth`

        ### Параметры

        - `login: str`
        Строка, представляющая логин (имя пользователя) для аутентификации

        - `password: str`
        Строка, представляющая пароль пользователя
        """

        with QMutexLocker(self.mutex):
            if self.is_running():
                return

            self.login = login
            self.password = password
            self.request_method = AccountInitialRequest.REGISTER
            self.start()

    def thread_workflow(self, socket: QTcpSocket) -> None:
        with QMutexLocker(self.mutex):
            login = self.login
            password = self.password
            request_method = self.request_method

        block = QByteArray()
        send_stream = QDataStream(block, QDataStream.OpenModeFlag.WriteOnly)
        send_stream.write_int32(request_method)
        send_stream.write_string(login)
        send_stream.write_string(password)
        socket.write(block)

        slot = self.slot_storage.create_and_store_slot("get_response", self.get_response, socket, request_method)
        socket.readyRead.connect(slot)
        self.wait_for_readyRead(socket)

    def get_response(self, socket: QTcpSocket, method: AccountInitialRequest) -> None:
        recieve_stream = QDataStream(socket)
        recieve_stream.start_transaction()

        raw_response = recieve_stream.read_int32()
        if not recieve_stream.commit_transaction():
            return

        response = AccountInitialResponse(raw_response)
        match method:
            case AccountInitialRequest.AUTH:
                self.proccess_auth_response(response)
            case AccountInitialRequest.REGISTER:
                self.proccess_register_response(response)
        
    def proccess_auth_response(self, response: AccountInitialResponse) -> None:
        match response:
            case AccountInitialResponse.AUTH_SUCCESS:
                message = "Вы успешно вошли"
            case AccountInitialResponse.AUTH_FAILURE_LOGIN:
                message = "Говно твой логин"
            case AccountInitialResponse.AUTH_FAILURE_PASSWORD:
                message = "Говно твой пароль"
        
        self.answerRecieved.emit(message)
    
    def proccess_register_response(self, response: AccountInitialResponse) -> None:
        match response:
            case AccountInitialResponse.REGISTER_SUCCESS:
                message = "Вы успешно зарегистрировались"
            case AccountInitialResponse.REGISTER_FAILURE:
                message = "Имя пользователя занято"
        
        self.answerRecieved.emit(message)
