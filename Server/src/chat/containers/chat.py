import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import Signal

from abstract import ServerSocketContainer
from Shared.games import GameType
from Shared.sockets import SocketType

from ..chat_manager import ChatManager


class ChatSocketContainer(ServerSocketContainer):
    socket_type = SocketType.CHAT

    messageReceived = Signal(str, str)

    _sendMessage = Signal(str, str)

    def on_start(self) -> None:
        self._sendMessage.connect(self._send_message)
        self.readyRead.connect(self.connect_to_chat_room)

    def connect_to_chat_room(self) -> None:
        data = self.receive_data_package(GameType)
        if data is None:
            return
        self.readyRead.disconnect(self.connect_to_chat_room)

        (room_id,) = data
        ChatManager.connect_to_chat_room(self, room_id)

        self.readyRead.connect(self.receive_message)

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
