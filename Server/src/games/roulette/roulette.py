import random
from collections import deque
from typing import TYPE_CHECKING

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import QTimer, Signal

from database import AccountsDB
from Shared import SlotStorage
from Shared.abstract import QSingleton, SocketContainerBase, ThreadBase
from Shared.games.roulette import (
    RouletteBet,
    RouletteBetResponse,
    RouletteColor,
    RouletteState,
)

if TYPE_CHECKING:
    from .containers import RouletteSocketContainer


class Roulette(ThreadBase, metaclass=QSingleton):
    result = Signal(RouletteColor, int)
    betMade = Signal(str, RouletteBet)
    stateChanged = Signal(RouletteState)

    makeBet = Signal(SocketContainerBase, str, RouletteBet)

    bet_interval = 10_000
    spin_interval = 10_000

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._slot_storage = SlotStorage()
        self.bets: dict[str, RouletteBet] = {}
        self.last_results: deque[RouletteColor] = deque(maxlen=12)

        self.state = RouletteState.STOPPED

    @property
    def slot_storage(self) -> SlotStorage:
        if not isinstance(self._slot_storage, SlotStorage):
            raise RuntimeError("Invalid slot storage")

        return self._slot_storage

    def thread_workflow(self) -> None:
        self.makeBet.connect(self.add_bet)

        bet_timer = QTimer()
        bet_timer.single_shot_ = True
        bet_timer.interval = self.bet_interval

        spin_timer = QTimer()
        spin_timer.single_shot_ = True
        spin_timer.interval = self.spin_interval

        slot = self.slot_storage.create_and_store_slot("start_spin", self.start_spin, spin_timer)
        bet_timer.timeout.connect(slot)

        slot = self.slot_storage.create_and_store_slot("after_spin", self.end_spin, bet_timer)
        spin_timer.timeout.connect(slot)

        bet_timer.start()
        self.exec()

    def start_spin(self, spin_timer: QTimer) -> None:
        self.makeBet.disconnect(self.add_bet)
        self.makeBet.connect(self.closed_bets)
        self.state = RouletteState.SPINNING
        self.stateChanged.emit(self.state)
        spin_timer.start()

    def closed_bets(self, container: "RouletteSocketContainer", *args) -> None:
        container.betResponse.emit(RouletteBetResponse.CLOSED)

    def end_spin(self, bet_timer: QTimer) -> None:
        self.makeBet.disconnect(self.closed_bets)

        self.process_payout()
        self.state = RouletteState.STOPPED
        self.stateChanged.emit(self.state)

        self.makeBet.connect(self.add_bet)
        bet_timer.start()

    def add_bet(self, container: "RouletteSocketContainer", login: str, bet: RouletteBet) -> None:
        if login in self.bets.keys():
            container.betResponse.emit(RouletteBetResponse.ALREADY_BET)
            return

        balance = AccountsDB().get_balance(login)
        if balance is None or balance < bet.total:
            container.betResponse.emit(RouletteBetResponse.OUT_OF_BALANCE)
            return

        self.bets[login] = bet
        container.betResponse.emit(RouletteBetResponse.SUCCESS)
        self.betMade.emit(login, bet)

    def calculate(self) -> tuple[RouletteColor, int]:
        result = random.randint(1, 30)
        if result > 0 and result < 15:
            return RouletteColor.RED, random.randint(4, 6)
        elif result > 14 and result < 29:
            return RouletteColor.BLACK, random.randint(1, 3)
        else:
            return RouletteColor.GREEN, random.randint(7, 8)

    def process_payout(self) -> None:
        db = AccountsDB()

        result, sector = self.calculate()
        match result:
            case RouletteColor.GREEN:
                multiplier = 10
            case RouletteColor.RED | RouletteColor.BLACK:
                multiplier = 1

        for login, bet in self.bets.items():
            balance = db.get_balance(login)
            total = bet.total * multiplier if bet.color == result else -bet.total
            db.change_balance(login, balance + total)

        self.bets.clear()

        self.last_results.append(result)
        self.result.emit(result, sector)
