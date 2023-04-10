import PySide6
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtCore import QByteArray, QDataStream, QMutex, QThread, QWaitCondition
from PySide6.QtNetwork import QTcpServer, QTcpSocket
from PySide6.QtWidgets import QApplication


class SocketHandler(QThread):
    def __init__(self, socket_descriptor: int, parent=None) -> None:
        super().__init__(parent)
        self.finished.connect(self.delete_later)

        self._socket_descriptor: int = socket_descriptor
        self._cond = QWaitCondition()
        self._mutex = QMutex()

    def run(self) -> None:
        socket = QTcpSocket()
        if not socket.set_socket_descriptor(self._socket_descriptor):
            return
        socket.readyRead.connect(lambda: self.on_readyRead(socket))

        while True:
            if not socket.wait_for_ready_read(5000):
                break

    def on_readyRead(self, socket: QTcpSocket) -> None:
        recieve_stream = QDataStream(socket)
        recieve_stream.set_version(QDataStream.Version.Qt_6_4)
        recieve_stream.start_transaction()

        login = recieve_stream.read_string()
        password = recieve_stream.read_string()
        print(login, password)
        if not recieve_stream.commit_transaction():
            return

        self.send_answer(socket, login, password)

    def handle_login_request(self, socket: QTcpSocket) -> bool:
        recieve_stream = QDataStream(socket)
        recieve_stream.set_version(QDataStream.Version.Qt_6_4)
        recieve_stream.start_transaction()

        login = recieve_stream.read_string()
        password = recieve_stream.read_string()
        print(login, password)
        if not recieve_stream.commit_transaction():
            return False

        self.send_answer(socket, login, password)
        return True

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


class Server(QTcpServer):
    def __init__(self, parent=None) -> None:
        super().__init__(parent)

        self._sockets: list[SocketHandler] = []

        if not self.listen(port=8888):
            print(self.error_string())
            sys.exit(self.error_string())

    def incoming_connection(self, handle: int) -> None:
        thread = SocketHandler(handle, self)
        thread.start()
        self._sockets.append(thread)


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    server = Server()
    sys.exit(app.exec())
