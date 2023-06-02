import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore  # noqa: F401;
from PySide6.QtCore import Signal

from Shared.abstract import SocketContainerBase
from Shared.games import GameType
from Shared.sockets.enums import SocketType


class ChatSocketContainer(SocketContainerBase):
    socket_type = SocketType.CHAT

    messageRecieved = Signal(str, str)

    _sendMessage = Signal(str, str)
    _connectToRoom = Signal(GameType)

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        slot = self.slot_storage.create_slot(self._send_message)
        self._sendMessage.connect(slot)
        slot = self.slot_storage.create_and_store_slot("connect_to_room", self.connect_to_room)
        self._connectToRoom.connect(slot)

    def run(self, game_room: GameType = GameType.ROULETTE) -> None:
        slot = self.slot_storage.create_and_store_slot("recieve_message", self.recieve_message)
        self.socket.readyRead.connect(slot)
        self._connectToRoom.emit(game_room)

    def exit(self) -> None:
        super().exit()
        self.socket.readyRead.disconnect(self.slot_storage.pop("recieve_message"))

    def connect_to_room(self, game_room: GameType) -> None:
        self._connectToRoom.disconnect(self.slot_storage.pop("connect_to_room"))
        self.send_data_package(game_room)

    def send_message(self, nickname: str, message: str) -> None:
        self._sendMessage.emit(nickname, message)

    def _send_message(self, nickname: str, message: str) -> None:
        self.send_data_package(nickname, message)

    def recieve_message(self) -> None:
        data: tuple[str, str] | None = self.recieve_data_package(str, str)
        if data is None:
            return

        (nickname, message) = data
        self.messageRecieved.emit(nickname, message)
