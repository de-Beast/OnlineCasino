import random
from database import AccountsDB
from Shared.sockets.enums import SocketThreadType, RouletteColor

class Roulette():
    __instance = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls, *args, **kwargs)
        return cls.__instance
    def __init__(self):
        self.bets = {}

    def calculate(self) -> str:
        result = random.randint(1, 30)
        if result > 0 and result < 15:
            return RouletteColor.RED
        elif result > 14 and result < 29:
            return RouletteColor.BLACK
        else:
            return RouletteColor.GREEN
    def workflow(self) -> None:
        result = self.calculate()
        for login, bet_n_color in self.bets.items():
            if result is not bet_n_color.color:
                AccountsDB().change_balance(login, bet_n_color.balance - bet_n_color.bet)
                continue
                
            match bet_n_color.color:
                case RouletteColor.GREEN:
                    AccountsDB().change_balance(login, bet_n_color.balance + bet_n_color.bet * 10)
                case RouletteColor.RED | RouletteColor.BLACK:
                    AccountsDB().change_balance(login, bet_n_color.balance + bet_n_color.bet)


