import random

import PySide6  # type: ignore # noqa: F401
from __feature__ import snake_case, true_property  # type: ignore # noqa: F401
from PySide6.QtCore import QTimer, Signal

from database import AccountsDB
from Shared import SlotStorage
from Shared.abstract import QSingleton, ThreadBase
from Shared.games.roulette import RouletteBet, RouletteBetResponse, RouletteColor


class Roulette(ThreadBase, metaclass=QSingleton):
    result = Signal(RouletteColor)
    betMade = Signal(str, RouletteBet)

    makeBet = Signal(str, RouletteBet)
    betResponse = Signal(RouletteBetResponse)

    bet_interval = 10_000
    spin_interval = 10_000

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self._slot_storage = SlotStorage()
        self.bets: dict[str, RouletteBet] = {}

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

        self.process_payout()
        spin_timer.start()

    def closed_bets(self, *args) -> None:
        self.betResponse.emit(RouletteBetResponse.CLOSED)

    def end_spin(self, bet_timer: QTimer) -> None:
        self.makeBet.disconnect(self.closed_bets)
        self.makeBet.connect(self.add_bet)
        bet_timer.start()

    def add_bet(self, login: str, bet: RouletteBet) -> None:
        if login in self.bets.keys():
            self.betResponse.emit(RouletteBetResponse.ALREADY_BET)
            return

        balance = AccountsDB().get_balance(login)
        if balance is None or balance < bet.total:
            self.betResponse.emit(RouletteBetResponse.OUT_OF_BALANCE)
            return

        self.bets[login] = bet
        self.betResponse.emit(RouletteBetResponse.SUCCESS)
        self.betMade.emit(login, bet)

    def calculate(self) -> RouletteColor:
        result = random.randint(1, 30)
        if result > 0 and result < 15:
            return RouletteColor.RED
        elif result > 14 and result < 29:
            return RouletteColor.BLACK
        else:
            return RouletteColor.GREEN

    def process_payout(self) -> None:
        db = AccountsDB()

        result = self.calculate()
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

        self.result.emit(result)
