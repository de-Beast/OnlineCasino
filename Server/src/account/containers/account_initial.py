import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401

from abstract import ServerSocketContainer
from database import AccountsDB, DB_CheckAccountResponse
from Shared.account import AccountInitialRequest, AccountInitialResponse
from Shared.sockets import SocketType


class AccountInitialSocketContainer(ServerSocketContainer):
    socket_type = SocketType.ACCOUNT_INITIAL

    def on_start(self) -> None:
        self.readyRead.connect(self.receive_request)

    def receive_request(self) -> None:
        data: tuple[str, str, AccountInitialRequest] | None = self.receive_data_package(str, str, AccountInitialRequest)
        if data is None:
            return

        login, password, method = data

        response = self.proccess_authorization(login, password, method)
        self.send_data_package(response)

    def proccess_authorization(
        self, login: str, password: str, method: AccountInitialRequest
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
