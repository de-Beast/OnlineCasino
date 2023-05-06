import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from database import AccountsDB, DB_CheckAccountResponse
from PySide6.QtNetwork import QTcpSocket

from Shared.sockets.enums import (
    AccountInitialRequest,
    AccountInitialResponse,
    SocketThreadType,
)

from .ABC import ServerSocketThreadABC


class AccountInitialSocketThread(ServerSocketThreadABC):
    socket_type = SocketThreadType.ACCOUNT_INITIAL

    def thread_workflow(self, socket: QTcpSocket) -> None:
        slot = self.slot_storage.create_and_store_slot("recieve_request", self.recieve_request, socket)
        socket.readyRead.connect(slot)
        self.wait_for_readyRead(socket)

    def recieve_request(self, socket: QTcpSocket) -> None:
        data: tuple[AccountInitialRequest, str, str] | None = self.recieve_data_package(
            socket, AccountInitialRequest, str, str
        )
        if data is None:
            return

        method, login, password = data

        response = self.proccess_authorization(method, login, password)
        self.send_data_package(socket, response)

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
