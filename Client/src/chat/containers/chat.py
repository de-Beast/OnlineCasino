import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import Signal

from abstract import ClientSocketContainer
from Shared.games import GameType
from Shared.sockets.enums import SocketType


class ChatSocketContainer(ClientSocketContainer):
    socket_type = SocketType.CHAT

    messageReceived = Signal(str, str)

    start = Signal(GameType)
    _sendMessage = Signal(str, str)

    def on_start(self, game_room: GameType) -> None:
        super().on_start()
        self.start.disconnect(self.on_start)

        self._sendMessage.connect(self._send_message)
        self.readyRead.connect(self.receive_message)

        self.send_data_package(game_room)

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
