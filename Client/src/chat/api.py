import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import Signal

from abstract import APIBase
from Shared.games import GameType

from .containers import ChatSocketContainer


class ChatAPI(APIBase):
    messageReceived = Signal(str, str)

    @APIBase.on_container_added(slot_name="setup_ChatSocketContainer")
    def setup_ChatSocketContainer(self, container: ChatSocketContainer) -> None:
        container.messageReceived.connect(self.messageReceived.emit)

    def connect_to_chat_room(self, game_room: GameType) -> None:
        if ChatSocketContainer.socket_type in self.containers.keys():
            return

        slot = self.slot_storage.create_and_store_slot(
            "setup_ChatSocketContainer",
            self.setup_ChatSocketContainer,
            None,
            ChatSocketContainer,
            game_room,
        )
        self.socket_thread.containerAdded.connect(slot)
        self.socket_thread.append_container(ChatSocketContainer.socket_type)

    def disconnect_from_chat_room(self) -> None:
        if container := self.containers.get(ChatSocketContainer.socket_type, None):
            if isinstance(container, ChatSocketContainer):
                container.quit()

    def send_message(self, message: str) -> None:
        if container := self.containers.get(ChatSocketContainer.socket_type, None):
            if isinstance(container, ChatSocketContainer):
                container.send_message(self.login, message)
