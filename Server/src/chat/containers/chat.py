import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import Signal

from Shared.abstract import SocketContainerBase
from Shared.games import GameType
from Shared.sockets import SocketType

from ..chat_manager import ChatManager


class ChatSocketContainer(SocketContainerBase):
    socket_type = SocketType.CHAT

    messageReceived = Signal(str, str)

    _sendMessage = Signal(str, str)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        slot = self.slot_storage.create_slot(self._send_message)
        self._sendMessage.connect(slot)

    def run(self) -> None:
        self.socket.readyRead.connect(self.connect_to_chat_room)
        self.connect_to_chat_room()

    def connect_to_chat_room(self) -> None:
        data: tuple[GameType] | None = self.receive_data_package(GameType)
        if data is None:
            return
        self.socket.readyRead.disconnect(self.connect_to_chat_room)

        (room_id,) = data
        ChatManager.connect_to_chat_room(self, room_id)

        slot = self.slot_storage.create_and_store_slot("receive_message", self.receive_message)
        self.socket.readyRead.connect(slot)

    def exit(self) -> None:
        super().exit()
        self.socket.readyRead.disconnect(self.slot_storage.pop("receive_message"))

    def send_message(self, nickname: str, message: str) -> None:
        self._sendMessage.emit(nickname, message)

    def _send_message(self, nickname: str, message: str) -> None:
        self.send_data_package(nickname, message)

    def receive_message(self) -> None:
        data: tuple[str, str] | None = self.receive_data_package(str, str)
        if data is None:
            return

        (nickname, message) = data
        self.messageReceived.emit(nickname, message)
