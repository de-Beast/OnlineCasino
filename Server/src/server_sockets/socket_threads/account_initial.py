import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from database import AccountsDB, DB_CheckAccountResponse
from PySide6.QtCore import QByteArray, QDataStream
from PySide6.QtNetwork import QTcpSocket

from Shared.sockets.enums import AccountInitialRequest, AccountInitialResponse

from .ABC import ServerSocketThreadABC


class AccountInitialSocketThread(ServerSocketThreadABC):
    def thread_workflow(self, socket: QTcpSocket) -> None:
        slot = self.slot_storage.create_and_store_slot("recieve_request", self.recieve_request, socket)
        socket.readyRead.connect(slot)
        self.wait_for_readyRead(socket)

    def recieve_request(self, socket: QTcpSocket) -> None:
        recieve_stream = QDataStream(socket)
        recieve_stream.set_version(QDataStream.Version.Qt_6_4)

        recieve_stream.start_transaction()
        method = recieve_stream.read_int32()
        login = recieve_stream.read_string()
        password = recieve_stream.read_string()
        if not recieve_stream.commit_transaction():
            return

        response = self.proccess_authorization(AccountInitialRequest(method), login, password)
        self.send_response(socket, response)

    def proccess_authorization(
        self, method: AccountInitialRequest, login: str, password: str
    ) -> AccountInitialResponse:
        db = AccountsDB()
        account = {"login": login, "password": password}
        match method:
            case AccountInitialRequest.REGISTER:
                if db.register_account(account):
                    response = AccountInitialResponse.REGISTER_SUCCESS
                else:
                    response = AccountInitialResponse.REGISTER_FAILURE
            case AccountInitialRequest.AUTH:
                match db.check_account(account):
                    case DB_CheckAccountResponse.OK:
                        response = AccountInitialResponse.AUTH_SUCCESS
                    case DB_CheckAccountResponse.WRONG_LOGIN:
                        response = AccountInitialResponse.AUTH_FAILURE_LOGIN
                    case DB_CheckAccountResponse.WRONG_PASSWORD:
                        response = AccountInitialResponse.AUTH_FAILURE_PASSWORD

        return response

    def send_response(self, socket: QTcpSocket, response: AccountInitialResponse) -> None:
        block = QByteArray()
        send_stream = QDataStream(block, QDataStream.OpenModeFlag.WriteOnly)
        send_stream.write_int32(response)
        socket.write(block)
        socket.wait_for_bytes_written(self.wait_timeout)
