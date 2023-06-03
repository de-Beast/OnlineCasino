import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401

from database import AccountsDB, DB_CheckAccountResponse
from Shared.abstract import SocketContainerBase
from Shared.account import AccountInitialRequest, AccountInitialResponse
from Shared.sockets import SocketType


class AccountInitialSocketContainer(SocketContainerBase):
    socket_type = SocketType.ACCOUNT_INITIAL

    def run(self) -> None:
        self.receive_request()
        
        slot = self.slot_storage.create_and_store_slot("receive_request", self.receive_request)
        self.socket.readyRead.connect(slot)

    def exit(self) -> None:
        self.socket.readyRead.disconnect(self.slot_storage.pop("receive_request"))
        super().exit()

    def receive_request(self) -> None:
        data: tuple[AccountInitialRequest, str, str] | None = self.receive_data_package(AccountInitialRequest, str, str)
        if data is None:
            return

        method, login, password = data

        response = self.proccess_authorization(method, login, password)
        self.send_data_package(response)

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
