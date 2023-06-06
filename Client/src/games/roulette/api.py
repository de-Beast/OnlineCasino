import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import Signal

from abstract import APIBase
from Shared.games.roulette import (
    RouletteBet,
    RouletteBetResponse,
    RouletteColor,
    RouletteState,
)

from .containers import RouletteSocketContainer


class RouletteAPI(APIBase):
    betResponse = Signal(RouletteBetResponse)
    resultReceived = Signal(RouletteColor, int)
    rouletteStateChanged = Signal(RouletteState)
    betReceived = Signal(str, RouletteBet)

    @APIBase.on_container_added(slot_name="setup_container")
    def setup_container(self, container: RouletteSocketContainer) -> None:
        container.betResponse.connect(self.betResponse.emit)
        container.resultReceived.connect(self.resultReceived.emit)
        container.rouletteStateChanged.connect(self.rouletteStateChanged.emit)
        container.betReceived.connect(self.betReceived.emit)

    def connect_to_game(self) -> None:
        if RouletteSocketContainer.socket_type in self.socket_thread.containers.keys():
            return

        slot = self.slot_storage.create_and_store_slot(
            "setup_container", self.setup_container, None, RouletteSocketContainer
        )
        self.socket_thread.containerAdded.connect(slot)
        self.socket_thread.append_container(RouletteSocketContainer.socket_type)

    def bet(self, bet: RouletteBet) -> None:
        if container := self.containers.get(RouletteSocketContainer.socket_type, None):
            if isinstance(container, RouletteSocketContainer):
                container.send_bet(self.login, bet)

    def disconnect_from_game(self) -> None:
        if container := self.containers.get(RouletteSocketContainer.socket_type, None):
            if isinstance(container, RouletteSocketContainer):
                container.quit()
