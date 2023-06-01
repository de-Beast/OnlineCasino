from typing import TYPE_CHECKING

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtCore import QObject

from Shared import SlotStorage

if TYPE_CHECKING:
    from .containers import ChatSocketContainer


class ChatRoom(QObject):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._slot_storage = SlotStorage()
        self._socket_containers: list["ChatSocketContainer"] = []

    @property
    def slot_storage(self) -> SlotStorage:
        return self._slot_storage

    @property
    def socket_containers(self) -> list["ChatSocketContainer"]:
        return self._socket_containers

    def add_socket(self, socket_container: "ChatSocketContainer") -> None:
        self.socket_containers.append(socket_container)

        slot = self.slot_storage.create_slot(self.socket_containers.remove, socket_container)
        socket_container.finished.connect(slot)

        slot = self.slot_storage.create_slot(self.message_recieved)
        socket_container.messageRecieved.connect(slot)

    def message_recieved(self, nickname: str, message: str) -> None:
        for socket_thread in self.socket_containers:
            socket_thread.send_message(nickname, message)


class ChatManager(QObject):
    chat_rooms: dict[str, ChatRoom] = {"roulette": ChatRoom()}

    @classmethod
    def connect_to_chat_room(cls, socket_container: "ChatSocketContainer", room_id: str) -> None:
        cls.chat_rooms[room_id].add_socket(socket_container)
