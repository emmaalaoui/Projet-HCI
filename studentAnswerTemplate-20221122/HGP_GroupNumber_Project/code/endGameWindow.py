from PyQt6.QtWidgets import QVBoxLayout, QWidget, QLabel
from PyQt6.QtGui import QIcon, QFont

class EndGameWindow(QWidget):
    print("A group of piece has been created")

    def __init__(self, go):
        super().__init__()
        self.go = go  # This variable contains the main window
        self.vbox = QVBoxLayout()
        self.winner = ""

        # Set the font for important texts
        self.fontTitle = QFont()
        self.fontTitle.setBold(True)
        self.fontTitle.setUnderline(True)
        self.fontTitle.setPixelSize(16)

        # Determine the winner


        # Set this window layout
        self.setFixedSize(300, 100)
        self.go.center()
        self.setWindowTitle("And the winner is...")
        self.setWindowIcon(QIcon("./icons/win.png"))
        self.hide()

    def updateEndGameWindow(self):

        if self.go.gameLogic.scores[0] > self.go.gameLogic.scores[1]:
            self.winner = "black"
        elif self.go.gameLogic.scores[0] < self.go.gameLogic.scores[1]:
            self.winner = "white"

        # Set this window widgets
        if self.winner == "":
            self.text1 = QLabel("You are both winners !!!")
        else:
            self.text1 = QLabel("The winner is " + self.winner + " !!!")
        self.text3 = QLabel("Congratulations !")
        self.text1.setFont(self.fontTitle)
        self.text2 = QLabel("Scores: " + str(self.go.gameLogic.scores[0]) + " vs " + str(self.go.gameLogic.scores[1]))
        self.text3.setFont(self.fontTitle)
        self.fontTitle.setUnderline(False)
        self.text2.setFont(self.fontTitle)
        self.vbox.addStretch(6)
        self.vbox.addWidget(self.text1)
        self.vbox.addWidget(self.text2)
        self.vbox.addStretch()
        self.vbox.addWidget(self.text3)
        self.vbox.addStretch(6)
        self.setLayout(self.vbox)

        print("ouais ouais")

        print(self.go.gameLogic.scores)
        print(self.winner)
        print(self.text2.text())
