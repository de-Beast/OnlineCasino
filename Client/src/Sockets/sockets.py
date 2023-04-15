import PySide6
from PySide6.QtNetwork import QTcpSocket
from PySide6.QtCore import QThread, QMutex, QMutexLocker, QWaitCondition, QDataStream, QByteArray, Signal

class AuthentificationSocket(QThread):
    answerRecieved = Signal(str)

    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port
        self.login = None
        self.password = None

        self.mutex = QMutex()
        self.cond = QWaitCondition()

    def auth(self, login, password):
        with QMutexLocker(self.mutex):
            self.login = login
            self.password = password
            self.cond.wakeOne()


    def run(self) -> None:

        with QMutexLocker(self.mutex):
            host = self.host
            port = self.port
            self.cond.wait(self.mutex)
            login = self.login
            password = self.password

        socket = QTcpSocket()
        socket.connectToHost(host, port)
        if not socket.waitForConnected(10000):
            return

        self.send_socket_type(socket)
        with QMutexLocker(self.mutex):
            self.cond.wait(self.mutex)
        
        block = QByteArray()
        send_stream = QDataStream(block, QDataStream.OpenModeFlag.WriteOnly)
        send_stream.writeString(login)
        send_stream.writeString(password)
        socket.write(block)
        socket.readyRead.connect()
        

    def send_socket_type(self, socket: QTcpSocket) -> None:
        block = QByteArray()
        send_stream = QDataStream(block, QDataStream.OpenModeFlag.WriteOnly)
        send_stream.writeInt32(0)
        socket.write(block)
        socket.readyRead.connect(lambda: self.notify_connection(socket))

    def notify_connection(self, socket: QTcpSocket) -> None:
        recieve_stream = QDataStream(socket)
        recieve_stream.startTransaction()
        is_connected = recieve_stream.readBool()
        if not recieve_stream.commitTransaction():
            return
        if not is_connected:
            return
        socket.readyRead.disconnect(lambda: self.notify_connection(socket))
        self.cond.wakeOne()

    def recieve_answer(self, answer):
        self.answerRecieved.emit(answer)



