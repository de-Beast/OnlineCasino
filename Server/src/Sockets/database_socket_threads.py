import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_properties  # type: ignore # noqa: F401
from PySide6.QtCore import QByteArray, QDataStream
from PySide6.QtNetwork import QTcpSocket

from .ABC import ServerSocketThreadABC


class AuthenticationSocketThread(ServerSocketThreadABC):
    def run(self) -> None:
        if (socket := self.create_socket()) is None:
            return

        while True:
            if not socket.wait_for_ready_read(self.wait_timeout):
                break

    def on_readyRead(self, socket: QTcpSocket) -> None:
        recieve_stream = QDataStream(socket)
        recieve_stream.set_version(QDataStream.Version.Qt_6_4)
        recieve_stream.start_transaction()

        login = recieve_stream.read_string()
        password = recieve_stream.read_string()
        if not recieve_stream.commit_transaction():
            return

        self.send_answer(socket, login, password)

    def send_answer(self, socket: QTcpSocket, login: str, password: str) -> None:
        block = QByteArray()
        send_stream = QDataStream(block, QDataStream.OpenModeFlag.WriteOnly)
        message = "Говно твой логин и пароль"
        if login == "admin" and password == "123":
            message = "Вы успешно вошли"
        send_stream.write_string(message)
        socket.write(block)
        socket.disconnect_from_host()
        socket.wait_for_disconnected()


class AccountSocketThread(ServerSocketThreadABC):
    def on_readyRead(self, socket: QTcpSocket) -> None:
        pass
