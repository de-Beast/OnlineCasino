from typing import TYPE_CHECKING

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401
from PySide6.QtCore import QObject

from Shared import SlotStorage
from Shared.games import GameType

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
        slot = self.slot_storage.create_and_store_slot(
            f"remove_container_{len(self.socket_containers)}",
            self.remove_container,
            socket_container,
            len(self.socket_containers),
        )
        socket_container.exit.connect(slot)

        socket_container.messageReceived.connect(self.message_received)

        self.socket_containers.append(socket_container)

    def message_received(self, nickname: str, message: str) -> None:
        for socket_thread in self.socket_containers:
            socket_thread.send_message(nickname, message)

    def remove_container(self, socket_container: "ChatSocketContainer", index: int) -> None:
        socket_container.exit.disconnect(self.slot_storage.pop(f"remove_container_{index}"))
        socket_container.messageReceived.disconnect(self.message_received)
        self.socket_containers.remove(socket_container)


class ChatManager(QObject):
    chat_rooms: dict[str, ChatRoom] = {GameType.ROULETTE: ChatRoom()}

    @classmethod
    def connect_to_chat_room(cls, socket_container: "ChatSocketContainer", game_room: GameType) -> None:
        cls.chat_rooms[game_room].add_socket(socket_container)
