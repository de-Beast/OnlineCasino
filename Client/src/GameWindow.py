from AllUi.ui_Game import Ui_Game
from PySide6 import QtCore, QtWidgets
from PySide6.QtGui import QMovie

from account.api import AccountAPI
from chat.api import ChatAPI
from games.roulette.api import (
    RouletteAPI,
    RouletteBet,
    RouletteBetResponse,
    RouletteState,
)
from Shared.games.roulette.enums import RouletteColor


class GameWindow(object):
    def __init__(self):
        self.widget = QtWidgets.QWidget()
        self.UI = Ui_Game()
        self.UI.setupUi(self.widget)

        self.UI.betEdit.textChanged.connect(self.OnBetEdit)

        self.chatApi = ChatAPI()
        self.chatApi.messageReceived.connect(self.OnMessageReceived)
        self.UI.messageEdit.returnPressed.connect(self.SendMessage)

        self.accountAPI = AccountAPI()
        self.accountAPI.responseAccountInfo.connect(self.UpdateAccountInfo)

        self.rouletteAPI = RouletteAPI()
        self.rouletteAPI.betReceived.connect(self.OnBetTaken)
        self.rouletteAPI.betResponse.connect(self.OnBetResponse)
        self.rouletteAPI.resultReceived.connect(self.UpdateRouletteState)
        self.rouletteAPI.rouletteStateChanged.connect(self.UpdateRouletteStatus)

        self.blackBet = 0
        self.redBet = 0
        self.greenBet = 0

        # TODO connect dis shit
        self.UI.blackBetButton.clicked.connect(lambda: self.OnBetMaked(RouletteColor.BLACK))
        self.UI.redBetButton.clicked.connect(lambda: self.OnBetMaked(RouletteColor.RED))
        self.UI.greenBetButton.clicked.connect(lambda: self.OnBetMaked(RouletteColor.GREEN))

        self.RegisterGifs()

        self.startGif = QMovie("gifs//spinning.gif")
        self.UI.circle.setScaledContents(True)
        self.UI.circle.setMovie(self.startGif)
        self.startGif.jumpToFrame(0)

        self.UI.balanceLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.UI.balanceLabel.setText("БАЛАНС:")

    def OnBetEdit(self):
        if not self.UI.betEdit.toPlainText().isnumeric():
            self.UI.betEdit.undo()

    def UpdateAccountInfo(self, newInfo):
        self.UI.balanceLabel.setText("БАЛАНС: " + str(newInfo["balance"]))

    def UpdateRouletteState(self, color: RouletteColor, num: int):
        if num >= 0:
            self.PlayGif(num)

    def UpdateRouletteStatus(self, status: RouletteState):
        if status == RouletteState.SPINNING:
            self.PlayGif(0)
        elif status == RouletteState.STOPPED:
            self.accountAPI.get_account_info()
            self.ClearBets()

    def RegisterGifs(self) -> None:
        self.gifs: list[QMovie] = []
        self.gifs.append(QMovie("gifs//infspinning.gif"))  # 0
        self.gifs.append(QMovie("gifs//black1-stop.gif"))  # 1
        self.gifs.append(QMovie("gifs//black2-stop.gif"))  # 2
        self.gifs.append(QMovie("gifs//black3-stop.gif"))  # 3
        self.gifs.append(QMovie("gifs//red1-stop.gif"))  # 4
        self.gifs.append(QMovie("gifs//red2-stop.gif"))  # 5
        self.gifs.append(QMovie("gifs//red3-stop.gif"))  # 6
        self.gifs.append(QMovie("gifs//zero-stop.gif"))  # 7
        self.gifs.append(QMovie("gifs//zero2-stop.gif"))  # 8

    def OnBetMaked(self, type: RouletteColor):
        if self.UI.betEdit.toPlainText() == "":
            return

        bet = RouletteBet(int(self.UI.betEdit.toPlainText()), type)
        self.rouletteAPI.bet(bet)

    def OnBetResponse(self, bet_response: RouletteBetResponse):
        match bet_response:
            case RouletteBetResponse.SUCCESS:
                self.UI.betEdit.clear()

    def ClearBets(self):
        self.UI.redBets.clear()
        self.redBet = 0
        self.UI.redBetsSum.setText("ОБЩАЯ СТАВКА: " + str(self.redBet))

        self.UI.blackBets.clear()
        self.blackBet = 0
        self.UI.blackBetsSum.setText("ОБЩАЯ СТАВКА: " + str(self.blackBet))

        self.UI.greenBets.clear()
        self.greenBet = 0
        self.UI.greenBetsSum.setText("ОБЩАЯ СТАВКА: " + str(self.greenBet))

    def OnBetTaken(self, nick: str, bet: RouletteBet):
        if bet.color == RouletteColor.RED:
            betSum = self.UI.redBetsSum
            betCont = self.UI.redBets
            self.redBet += bet.total
            betSize = self.redBet
        elif bet.color == RouletteColor.BLACK:
            betSum = self.UI.blackBetsSum
            betCont = self.UI.blackBets
            self.blackBet += bet.total
            betSize = self.blackBet
        else:
            self.greenBet += bet.total
            betSum = self.UI.greenBetsSum
            betCont = self.UI.greenBets
            betSize = self.greenBet

        betSum.setText("ОБЩАЯ СТАВКА: " + str(betSize))
        betCont.append("<b>" + nick + ":</b> " + str(bet.total))

    def OnMessageReceived(self, nickname: str, message: str):
        self.UI.chat.append("<b>" + nickname + ":</b>")
        self.UI.chat.append(message)
        self.UI.chat.append("")

    def SendMessage(self):
        if self.UI.messageEdit.text() == "":
            return

        self.chatApi.send_message(self.UI.messageEdit.text())
        self.UI.messageEdit.clear()

    def PlayGif(self, indOfGif: int):
        self.UI.circle.setMovie(self.gifs[indOfGif])  # TODO create movie from MaxGrig's gif
        self.gifs[indOfGif].start()
