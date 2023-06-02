import random

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QMovie

from AllUi.ui_Game import Ui_Game
from Shared.games.roulette.enums import RouletteColor
from Shared.games.enums import GameType
from chat.api import ChatAPI
from account.api import AccountInfo
from account.api import AccountAPI
from games.roulette.api import RouletteAPI, RouletteBet, RouletteState

class GameWindow(object):
    def __init__(self):
        self.widget = QtWidgets.QWidget()
        self.UI = Ui_Game()
        self.UI.setupUi(self.widget)

        self.chatApi = ChatAPI()
        self.chatApi.recievedMessage.connect(self.OnMessageRecieved)
        self.UI.messageEdit.returnPressed.connect(self.SendMessage)

        self.accountAPI = AccountAPI()
        self.accountAPI.responseAccountInfo.connect(self.UpdateAccountInfo)

        self.rouletteAPI = RouletteAPI()
        self.rouletteAPI.betRecieved.connect(self.OnBetTaken)
        self.rouletteAPI.resultRecieved.connect(self.UpdateRouletteState)

        self.blackBet = 0
        self.redBet = 0
        self.greenBet = 0

        #TODO connect dis shit
        self.UI.blackBetButton.clicked.connect(lambda : self.OnBetMaked(RouletteColor.BLACK))
        self.UI.redBetButton.clicked.connect(lambda : self.OnBetMaked(RouletteColor.RED))
        self.UI.greenBetButton.clicked.connect(lambda : self.OnBetMaked(RouletteColor.GREEN))

        self.RegisterGifs()

        self.startGif = QMovie("gifs//spinning.gif")
        self.UI.circle.setScaledContents(True)
        self.UI.circle.setMovie(self.startGif)
        self.startGif.jumpToFrame(0)

        self.UI.balanceLabel.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)
        self.UI.balanceLabel.setText("БАЛАНС: 21")

    def UpdateAccountInfo(self, newInfo):
        self.accountInfo = newInfo
        self.UI.balanceLabel.setText("БАЛАНС: " + str(newInfo['balance']))

    def UpdateRouletteState(self, color : RouletteColor, num : int):
        self.PlayGif(num)

    def UpdateRouletteStatus(self, status : RouletteState):
        if status == RouletteState.SPINNING:
            self.PlayGif(0)
        elif status == RouletteState.STOPPED:
            pass

    def RegisterGifs(self):
        self.gifs = []
        self.gifs.append(QMovie("gifs//infspinning.gif")) #0
        self.gifs.append(QMovie("gifs//black1-stop.gif")) #1
        self.gifs.append(QMovie("gifs//black2-stop.gif")) #2
        self.gifs.append(QMovie("gifs//black3-stop.gif")) #3
        self.gifs.append(QMovie("gifs//red1-stop.gif"))   #4
        self.gifs.append(QMovie("gifs//red2-stop.gif"))   #5
        self.gifs.append(QMovie("gifs//red3-stop.gif"))   #6
        self.gifs.append(QMovie("gifs//zero-stop.gif"))   #7
        self.gifs.append(QMovie("gifs//zero2-stop.gif"))  #8

    def OnBetMaked(self, type : RouletteColor):
        self.rouletteAPI.bet(RouletteBet(total=int(self.UI.betEdit.toPlainText()), color=type))

    def OnBetTaken(self, nick : str, bet : RouletteBet):
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

    def OnMessageRecieved(self, nickname : str, message : str):
        self.UI.chat.append("<b>" + nickname + ":</b>")
        self.UI.chat.append(message)
        self.UI.chat.append("")

    def SendMessage(self):
        if self.UI.messageEdit.text() == "":
            return

        self.chatApi.send_message(self.UI.messageEdit.text())
        self.UI.messageEdit.clear()

    def PlayGif(self, indOfGif : int):
        self.UI.circle.setMovie(self.gifs[indOfGif]) #TODO create movie from MaxGrig's gif
        self.gifs[indOfGif].start()
