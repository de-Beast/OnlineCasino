import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import Signal

from abstract import APIBase
from Shared.sockets import SocketThreadType

from .containers import ChatSocketContainer


class ChatAPI(APIBase):
    recievedMessage = Signal(str, str)

    def on_container_added(self, socket_type: SocketThreadType, *args) -> None:
        container: ChatSocketContainer = self.socket_thread.containers[socket_type]
        if isinstance(container, ChatSocketContainer):
            container.messageRecieved.connect(self.recievedMessage.emit)
        else:
            return

        self.socket_thread.containerAdded.disconnect(self.slot_storage.pop("on_container_added"))
        container.run(*args)

    def connect_to_chat_room(self, room_id: str) -> None:
        if ChatSocketContainer.socket_type in self.socket_thread.containers.keys():
            return

        slot = self.slot_storage.create_and_store_slot(
            "on_container_added", self.on_container_added, None, ChatSocketContainer.socket_type, room_id
        )
        self.socket_thread.containerAdded.connect(slot)
        self.socket_thread.add_container(ChatSocketContainer.socket_type)

    def disconnect_from_chat_room(self) -> None:
        if container := self.socket_thread.containers.get(ChatSocketContainer.socket_type, None):
            if isinstance(container, ChatSocketContainer):
                container.quit()

    def send_message(self, nickname: str, message: str) -> None:
        if container := self.socket_thread.containers.get(ChatSocketContainer.socket_type, None):
            if isinstance(container, ChatSocketContainer):
                container.send_message(nickname, message)
