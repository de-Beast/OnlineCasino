import random

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtGui import QMovie

from Client.AllUi.ui_Game import Ui_Game
from Client.src.client_sockets.socket_threads.chat import ChatSocketThread

class GameWindow(object):
    def __init__(self):
        self.widget = QtWidgets.QWidget()
        self.UI = Ui_Game()
        self.UI.setupUi(self.widget)


        self.chatThread = ChatSocketThread()

        self.chatThread.responseRecieved.connect(self.OnMessageRecieved)
        self.UI.messageEdit.returnPressed.connect(self.SendMessage)

        #TODO connect dis shit
        self.UI.blackBetButton.clicked.connect(lambda : self.OnBetMaked("black"))
        self.UI.redBetButton.clicked.connect(lambda : self.OnRedBetMaked("red"))
        self.UI.greenBetButton.clicked.connect(lambda : self.OnBetMaked("green"))

        self.RegisterGifs()

        self.startGif = QMovie("gifs//spinning.gif")
        self.UI.circle.setScaledContents(True)
        self.UI.circle.setMovie(self.startGif)
        self.startGif.jumpToFrame(0)

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

    def OnBetMaked(self, type):
        ...
        self.PlayGif(random.randint(0, len(self.gifs) - 1))

    def OnBetTaken(self, type):
        pass

    def OnMessageRecieved(self, nickname : str, message : str):
        self.UI.chat.append("<b>" + nickname + ":</b>")
        self.UI.chat.append(message)
        self.UI.chat.append("")

    def SendMessage(self):
        if self.UI.messageEdit.text() == "":
            return

        self.chatThread.send_message("bagel", self.UI.messageEdit.text) #TODO get nickname

        self.OnMessageRecieved("<b>bagel:</b>", self.UI.messageEdit.text())
        self.UI.messageEdit.clear()

    def PlayGif(self, indOfGif : int):
        self.UI.circle.setMovie(self.gifs[indOfGif]) #TODO create movie from MaxGrig's gif
        self.gifs[indOfGif].start()
