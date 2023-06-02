from typing import Callable, Self

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import Signal

from abstract import APIBase
from Shared.abstract import SocketContainerBase
from Shared.games.roulette import RouletteBet, RouletteBetResponse, RouletteColor
from Shared.sockets import SocketType

from .containers import RouletteSocketContainer
from Shared.games.roulette import RouletteState


class RouletteAPI(APIBase):
    betResponse = Signal(RouletteBetResponse)
    resultRecieved = Signal(RouletteColor, int)
    rouletteStateChanged = Signal(RouletteState)
    betRecieved = Signal(str, RouletteBet)

    @staticmethod
    def on_container_added(*, slot_name: str):
        def inner(func: Callable):
            def wrapper(self: Self, socket_type: SocketType, *args) -> None:
                container = self.containers[socket_type]
                func(self, container)
                self.socket_thread.containerAdded.disconnect(self.slot_storage.pop(slot_name))
                container.run(*args)

            return wrapper

        return inner

    @on_container_added(slot_name="setup_container")
    def setup_container(self, container: SocketContainerBase) -> None:
        if not isinstance(container, RouletteSocketContainer):
            return
        container.betResponse.connect(self.betResponse.emit)
        container.resultRecieved.connect(self.resultRecieved.emit)
        container.rouletteStateChanged.connect(self.rouletteStateChanged.emit)
        container.betRecieved.connect(self.betRecieved.emit)

    def connect_to_game(self) -> None:
        if RouletteSocketContainer.socket_type in self.socket_thread.containers.keys():
            return

        slot = self.slot_storage.create_and_store_slot(
            "setup_container", self.setup_container, None, RouletteSocketContainer.socket_type
        )
        self.socket_thread.containerAdded.connect(slot)
        self.socket_thread.add_container(RouletteSocketContainer.socket_type)

    def bet(self, bet: RouletteBet) -> None:
        if container := self.containers.get(RouletteSocketContainer.socket_type, None):
            if isinstance(container, RouletteSocketContainer):
                container.send_bet(self.login, bet)

    def disconnect_from_game(self) -> None:
        if container := self.containers.get(RouletteSocketContainer.socket_type, None):
            if isinstance(container, RouletteSocketContainer):
                container.quit()
