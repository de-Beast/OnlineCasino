import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import QMutexLocker, QObject, Signal
from PySide6.QtNetwork import QTcpSocket

from Shared.sockets.enums import (
    AccountInitialRequest,
    AccountInitialResponse,
    SocketThreadType,
)

from .ABC import ClientSocketThreadABC
from .Client import Client


@Client.register_socket_thread_class
class AccountInitialSocketThread(ClientSocketThreadABC):
    """
    Поток для обработки запросов, связанных с авторизацией и регистрацией

    Вызовите метод `auth`, чтобы запустить поток, который выполнит вход в аккаунт пользователя

    Вызовите метод `register`, чтобы запустить поток, который зарегистрирует пользователя
    """

    # Активируется после того, как сервер прислал ответ о попытке войти или зарегистрироваться.
    # Передаёт в сигнал ответ сервера в виде строки
    responseRecieved = Signal(str)

    # Переменная класса, определяющая тип потока, передаётся серверу.
    # Не может быть двух классов с одинаковым типом потока
    socket_type = SocketThreadType.ACCOUNT_INITIAL

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

        self.login: str
        self.password: str
        self.request_method: AccountInitialRequest

    @Client.mark_socket_thread_method
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

    @Client.mark_socket_thread_method
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

        self.send_data_package(socket, request_method, login, password)

        slot = self.slot_storage.create_and_store_slot("get_response", self.get_response, socket, request_method)
        socket.readyRead.connect(slot)
        self.wait_for_readyRead(socket)

    def get_response(self, socket: QTcpSocket, method: AccountInitialRequest) -> None:
        data: tuple[AccountInitialResponse] | None = self.recieve_data_package(socket, AccountInitialResponse)
        if data is None:
            return

        (response,) = data

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

        self.responseRecieved.emit(message)

    def proccess_register_response(self, response: AccountInitialResponse) -> None:
        match response:
            case AccountInitialResponse.REGISTER_SUCCESS:
                message = "Вы успешно зарегистрировались"
            case AccountInitialResponse.REGISTER_FAILURE:
                message = "Имя пользователя занято"

        self.responseRecieved.emit(message)
