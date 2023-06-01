import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import Signal

from abstract import APIBase
from Shared.account import AccountInfo, AccountInitialRequest, AccountInitialResponse
from Shared.sockets import SocketThreadType

from .containers import AccountInfoSocketContainer, AccountInitialSocketContainer


class AccountAPI(APIBase):
    responseAccountInitial = Signal(AccountInitialResponse)
    responseAccountInfo = Signal(AccountInfo)

    def on_container_added(self, socket_type: SocketThreadType, *args) -> None:
        container = self.socket_thread.containers[socket_type]
        if isinstance(container, AccountInitialSocketContainer):
            container.responseRecieved.connect(self.responseAccountInitial.emit)
        elif isinstance(container, AccountInfoSocketContainer):
            container.responseRecieved.connect(self.responseAccountInfo.emit)
        else:
            return

        self.socket_thread.containerAdded.disconnect(self.slot_storage.pop("on_container_added"))
        container.run(*args)

    def auth(self, login: str, password: str) -> None:
        if container := self.socket_thread.containers.get(AccountInitialSocketContainer.socket_type, None):
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

    def register(self, login: str) -> None:
        if container := self.socket_thread.containers.get(AccountInitialSocketContainer.socket_type, None):
            container.quit()

        slot = self.slot_storage.create_and_store_slot(
            "on_container_added",
            self.on_container_added,
            None,
            AccountInitialSocketContainer.socket_type,
            login,
            AccountInitialRequest.REGISTER,
        )
        self.socket_thread.containerAdded.connect(slot)
        self.socket_thread.add_container(AccountInitialSocketContainer.socket_type)

    def get_account_info(self, login: str) -> None:
        if container := self.socket_thread.containers.get(AccountInfoSocketContainer.socket_type, None):
            container.quit()

        slot = self.slot_storage.create_and_store_slot(
            "on_container_added",
            self.on_container_added,
            None,
            AccountInfoSocketContainer.socket_type,
            login,
        )
        self.socket_thread.containerAdded.connect(slot)
        self.socket_thread.add_container(AccountInfoSocketContainer.socket_type)
