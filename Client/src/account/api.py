import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import Signal

from abstract import APIBase
from Shared.abstract import SocketContainerBase
from Shared.account import AccountInfo, AccountInitialRequest, AccountInitialResponse

from .containers import AccountInfoSocketContainer, AccountInitialSocketContainer


class AccountAPI(APIBase):
    responseAccountInitial = Signal(AccountInitialResponse)
    responseAccountInfo = Signal(AccountInfo)

    def save_login(self, container: SocketContainerBase, response: AccountInitialResponse) -> None:
        match response:
            case AccountInitialResponse.AUTH_SUCCESS | AccountInitialResponse.REGISTER_SUCCESS:
                pass
            case _:
                APIBase._login = None

        if isinstance(container, AccountInitialSocketContainer) or isinstance(container, AccountInfoSocketContainer):
            container.responseReceived.disconnect(self.slot_storage.pop("save_login"))

    @APIBase.on_container_added(slot_name="setup_AccountInitialSocketContainer")
    def setup_AccountInitialSocketContainer(self, container: AccountInitialSocketContainer) -> None:
        slot = self.slot_storage.create_and_store_slot("save_login", self.save_login, container)
        container.responseReceived.connect(slot)
        container.responseReceived.connect(self.responseAccountInitial.emit)

    @APIBase.on_container_added(slot_name="setup_AccountInfoSocketContainer")
    def setup_AccountInfoSocketContainer(self, container: AccountInitialSocketContainer) -> None:
        container.responseReceived.connect(self.responseAccountInfo.emit)

    def auth(self, login: str, password: str) -> None:
        if container := self.containers.get(AccountInitialSocketContainer.socket_type, None):
            container.quit()

        slot = self.slot_storage.create_and_store_slot(
            "setup_AccountInitialSocketContainer",
            self.setup_AccountInitialSocketContainer,
            None,
            AccountInitialSocketContainer,
            login,
            password,
            AccountInitialRequest.AUTH,
        )
        APIBase._login = login
        self.socket_thread.containerAdded.connect(slot)
        self.socket_thread.append_container(AccountInitialSocketContainer.socket_type)

    def register(self, login: str, password: str) -> None:
        if container := self.containers.get(AccountInitialSocketContainer.socket_type, None):
            container.quit()

        slot = self.slot_storage.create_and_store_slot(
            "setup_AccountInitialSocketContainer",
            self.setup_AccountInitialSocketContainer,
            None,
            AccountInitialSocketContainer,
            login,
            password,
            AccountInitialRequest.REGISTER,
        )
        APIBase._login = login
        self.socket_thread.containerAdded.connect(slot)
        self.socket_thread.append_container(AccountInitialSocketContainer.socket_type)

    def get_account_info(self) -> None:
        if container := self.containers.get(AccountInfoSocketContainer.socket_type, None):
            container.quit()

        slot = self.slot_storage.create_and_store_slot(
            "setup_AccountInfoSocketContainer",
            self.setup_AccountInfoSocketContainer,
            None,
            AccountInfoSocketContainer,
            self.login,
        )
        self.socket_thread.containerAdded.connect(slot)
        self.socket_thread.append_container(AccountInfoSocketContainer.socket_type)
