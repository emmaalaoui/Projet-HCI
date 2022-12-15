from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from board import Board
from score_board import ScoreBoard
from game_logic import GameLogic
from endGameWindow import EndGameWindow


class Go(QMainWindow):

    def __init__(self, startWidth, bool, pos):
        super().__init__()
        print(self.y())
        self.widthMinusHeight = 180  # 138
        self.formerWidth = startWidth
        self.formerHeight = self.formerWidth - self.widthMinusHeight
        self.firstResize = True
        self.widthResizement = False
        self.heightResizement = False
        print(self.width(), self.height())
        self.resize(self.formerWidth, self.formerHeight)
        print(self.width(), self.height())
        self.setMinimumSize(self.formerWidth - 5, self.formerHeight - 5)
        self.setMaximumSize(1080, 1080-138)
        self.initUI(bool, pos)

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self, bool, pos):
        '''initiates application UI'''
        self.gameLogic = GameLogic()
        self.scoreBoard = ScoreBoard(self)
        self.board = Board(self)
        self.endGameWindow = EndGameWindow(self)
        # self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.myScoreBoard = QHBoxLayout()
        self.myScoreBoard.addWidget(self.board, 7)
        self.myScoreBoard.addWidget(self.scoreBoard, 1)
        mainWidget = QWidget()
        mainWidget.setLayout(self.myScoreBoard)
        self.setCentralWidget(mainWidget)
        self.scoreBoard.make_connection(self.board)

        if bool:
            self.center()
        else:
            self.move(pos[0], pos[1])
        self.setStyleSheet("background-color: light grey")
        self.setWindowTitle("GroupProject - Go - HGP-FT02")
        self.setWindowIcon(
            QIcon("./icons/go.png"))
        self.show()

    def showEndWindow(self):
        self.hide()
        self.endGameWindow.show()

    def updateEndWindow(self):
        self.endGameWindow.updateEndGameWindow()

    def resizeEvent(self, event):
        if not self.firstResize:
            if self.formerHeight != self.height() and self.formerWidth != self.width():
                if abs(self.formerHeight - self.height()) < abs(self.formerWidth - self.width()):
                    self.formerHeight = self.height()
                else:
                    self.formerWidth = self.width()
            if self.formerHeight == self.height():
                if self.width() - self.height() != self.widthMinusHeight:
                    self.formerWidth = self.width()
                    self.resize(self.width(), self.width() - self.widthMinusHeight)
            else:
                if self.formerWidth == self.width():
                    if self.width() - self.height() != self.widthMinusHeight:
                        self.formerHeight = self.height()
                        self.resize(self.height() + self.widthMinusHeight, self.height())

        elif self.firstResize:
            self.firstResize = False


    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())
        # size = self.geometry()
        # self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2)
