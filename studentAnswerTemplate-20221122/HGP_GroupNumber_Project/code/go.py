from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget, QLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from board import Board
from score_board import ScoreBoard
from game_logic import GameLogic
from endGameWindow import EndGameWindow


class Go(QMainWindow):

    def __init__(self):
        super().__init__()
        self.widthMinusHeight = 138
        self.formerWidth = 690
        self.formerHeight = self.formerWidth - self.widthMinusHeight
        self.firstResize = True
        self.widthResizement = False
        self.heightResizement = False
        self.con = True
        self.count = 0
        print(self.width(), self.height())
        self.resize(self.formerWidth, self.formerHeight)
        print(self.width(), self.height())
        self.setMinimumSize(self.formerWidth - 5, self.formerHeight - 5)
        self.setMaximumSize(660+138, 660)
        self.initUI()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):
        '''initiates application UI'''
        self.gameLogic = GameLogic()
        self.scoreBoard = ScoreBoard(self)
        self.board = Board(self)
        self.endGameWindow = EndGameWindow(self)
        # self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.myScoreBoard = QHBoxLayout()
        self.myScoreBoard.addWidget(self.board, 6)
        self.myScoreBoard.addWidget(self.scoreBoard, 1)
        mainWidget = QWidget()
        mainWidget.setLayout(self.myScoreBoard)
        self.setCentralWidget(mainWidget)
        self.scoreBoard.make_connection(self.board)


        # self.center()
        self.setStyleSheet("background-color: light grey")
        self.setWindowTitle("GroupProject - Go - HGP-FT02")
        self.setWindowIcon(
            QIcon("./icons/logo.png"))
        self.show()

    def showEndWindow(self):
        self.hide()
        self.endGameWindow.show()

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
                    self.count = self.count + 1
            else:
                if self.formerWidth == self.width():
                    if self.width() - self.height() != self.widthMinusHeight:
                        self.formerHeight = self.height()
                        self.resize(self.height() + self.widthMinusHeight, self.height())
                        self.count = self.count + 1

        elif self.firstResize:
            print(self.firstResize)
            self.firstResize = False


    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())
        # size = self.geometry()
        # self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2)
