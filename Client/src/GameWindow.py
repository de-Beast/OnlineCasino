import random

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QMovie

from Client.AllUi.ui_Game import Ui_Game
from Shared.games.roulette.enums import RouletteColor
from Shared.games.enums import GameType
from Client.src.chat.api import ChatAPI
from Client.src.games.roulette.api import RouletteAPI, RouletteBet

class GameWindow(object):
    def __init__(self):
        self.widget = QtWidgets.QWidget()
        self.UI = Ui_Game()
        self.UI.setupUi(self.widget)

        self.chatApi = ChatAPI()
        self.chatApi.recievedMessage.connect(self.OnMessageRecieved)
        self.UI.messageEdit.returnPressed.connect(self.SendMessage)

        self.rouletteAPI = RouletteAPI()

        #TODO connect dis shit
        self.UI.blackBetButton.clicked.connect(lambda : self.OnBetMaked(RouletteColor.BLACK))
        self.UI.redBetButton.clicked.connect(lambda : self.OnBetMaked(RouletteColor.RED))
        self.UI.greenBetButton.clicked.connect(lambda : self.OnBetMaked(RouletteColor.GREEN))

        self.RegisterGifs()

        self.startGif = QMovie("gifs//spinning.gif")
        self.UI.circle.setScaledContents(True)
        self.UI.circle.setMovie(self.startGif)
        self.startGif.jumpToFrame(0)


        self.UI.balanceLabel.setText("БАЛАНС: 21")

        self.OnMessageRecieved("sopernik_vrazhina", "тебе конец!!!")

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
        ...
        self.PlayGif(random.randint(0, len(self.gifs) - 1))
        self.rouletteAPI.bet(RouletteBet(total=int(self.UI.betEdit.toPlainText()), color=type))

    def OnBetTaken(self, bet : RouletteBet):
        if type == RouletteColor.RED:
            betSum = self.UI.redBetsSum
            betCont = self.UI.redBets
        elif type == RouletteColor.BLACK:
            betSum = self.UI.blackBetsSum
            betCont = self.UI.blackBets
        else:
            betSum = self.UI.greenBetsSum
            betCont = self.UI.greenBets

        betSize = 333
        betSum.setText("ОБЩАЯ СТАВКА: " + str(betSize))
        betCont.append("<b>nick:</b> " + str(betSize))

    def OnMessageRecieved(self, nickname : str, message : str):
        self.UI.chat.append("<b>" + nickname + ":</b>")
        self.UI.chat.append(message)
        self.UI.chat.append("")

    def SendMessage(self):
        if self.UI.messageEdit.text() == "":
            return

        self.chatApi.send_message(self.UI.messageEdit.text)

        self.UI.messageEdit.clear()

    def PlayGif(self, indOfGif : int):
        self.UI.circle.setMovie(self.gifs[indOfGif]) #TODO create movie from MaxGrig's gif
        self.gifs[indOfGif].start()
