import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import QByteArray, QDataStream
from PySide6.QtNetwork import QTcpSocket

# from database import AccountsDB

from .ABC import ServerSocketThreadABC
from database import AccountsDB, CheckAccountResponse


class AuthorizationSocketThread(ServerSocketThreadABC):
    def thread_workflow(self, socket: QTcpSocket) -> None:
        socket.readyRead.connect(lambda: self.on_readyRead(socket))
        self.wait_for_readyRead(socket)

    def on_readyRead(self, socket: QTcpSocket) -> None:
        recieve_stream = QDataStream(socket)
        recieve_stream.set_version(QDataStream.Version.Qt_6_4)

        recieve_stream.start_transaction()
        login = recieve_stream.read_string()
        password = recieve_stream.read_string()
        sign_up = recieve_stream.read_bool()
        if not recieve_stream.commit_transaction():
            return

        self.send_answer(socket, login, password, sign_up)

    def send_answer(self, socket: QTcpSocket, login: str, password: str, sign_up: bool) -> None:
        db = AccountsDB()
        account = {"login": login, "password": password}
        if sign_up:
            if db.register_account(account):
                message = "Вы успешно зарегестрированы"
            else:
                message = "Данное имя пользователя уже занято"
        else:
            match db.check_account(account):
                case CheckAccountResponse.OK:
                    message = "Вы успешно вошли"
                case CheckAccountResponse.WRONG_LOGIN:
                    message = "Говно твой логин"
                case CheckAccountResponse.WRONG_PASSWORD:
                    message = "Говно твой пароль"

        block = QByteArray()
        send_stream = QDataStream(block, QDataStream.OpenModeFlag.WriteOnly)
        send_stream.write_string(message)
        socket.write(block)
        socket.wait_for_bytes_written(self.wait_timeout)


class AccountSocketThread(ServerSocketThreadABC):
    def thread_workflow(self, socket: QTcpSocket) -> None:
        pass
