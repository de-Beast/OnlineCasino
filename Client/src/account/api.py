import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import Signal

from abstract import APIBase
from Shared.abstract import SocketContainerBase
from Shared.account import AccountInfo, AccountInitialRequest, AccountInitialResponse
from Shared.sockets import SocketType

from .containers import AccountInfoSocketContainer, AccountInitialSocketContainer


class AccountAPI(APIBase):
    responseAccountInitial = Signal(AccountInitialResponse)
    responseAccountInfo = Signal(AccountInfo)

    def save_login(self, container: SocketContainerBase, login: str, response: AccountInitialResponse) -> None:
        match response:
            case AccountInitialResponse.AUTH_SUCCESS | AccountInitialResponse.REGISTER_SUCCESS:
                self._login = login

        if isinstance(container, AccountInitialSocketContainer) or isinstance(container, AccountInfoSocketContainer):
            container.responseRecieved.disconnect(self.slot_storage.pop("save_login"))

    def on_container_added(self, socket_type: SocketType, *args) -> None:
        container = self.containers[socket_type]
        if isinstance(container, AccountInitialSocketContainer):
            container.responseRecieved.connect(self.responseAccountInitial.emit)
            slot = self.slot_storage.create_and_store_slot("save_login", self.save_login, container, args[0])
            container.responseRecieved.connect(slot)
        elif isinstance(container, AccountInfoSocketContainer):
            container.responseRecieved.connect(self.responseAccountInfo.emit)
        else:
            return

        self.socket_thread.containerAdded.disconnect(self.slot_storage.pop("on_container_added"))
        container.run(*args)

    def auth(self, login: str, password: str) -> None:
        if container := self.containers.get(AccountInitialSocketContainer.socket_type, None):
            container.quit()

        slot = self.slot_storage.create_and_store_slot(
            "on_container_added",
            self.on_container_added,
            None,
            AccountInitialSocketContainer.socket_type,
            login,
            password,
            AccountInitialRequest.AUTH,
        )
        self.socket_thread.containerAdded.connect(slot)
        self.socket_thread.add_container(AccountInitialSocketContainer.socket_type)

    def register(self, login: str, password: str) -> None:
        if container := self.containers.get(AccountInitialSocketContainer.socket_type, None):
            container.quit()

        slot = self.slot_storage.create_and_store_slot(
            "on_container_added",
            self.on_container_added,
            None,
            AccountInitialSocketContainer.socket_type,
            login,
            password,
            AccountInitialRequest.REGISTER,
        )
        self.socket_thread.containerAdded.connect(slot)
        self.socket_thread.add_container(AccountInitialSocketContainer.socket_type)

    def get_account_info(self) -> None:
        if container := self.containers.get(AccountInfoSocketContainer.socket_type, None):
            container.quit()

        slot = self.slot_storage.create_and_store_slot(
            "on_container_added",
            self.on_container_added,
            None,
            AccountInfoSocketContainer.socket_type,
            self.login,
        )
        self.socket_thread.containerAdded.connect(slot)
        self.socket_thread.add_container(AccountInfoSocketContainer.socket_type)
