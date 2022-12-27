from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget
from PyQt6.QtGui import QIcon
from board import Board
from score_board import ScoreBoard
from game_logic import GameLogic
from endGameWindow import EndGameWindow


class Go(QMainWindow):

    def __init__(self, startWidth, bool, pos):  # Set the window's size
        super().__init__()
        self.widthMinusHeight = 180
        self.formerWidth = startWidth
        self.formerHeight = self.formerWidth - self.widthMinusHeight
        self.firstResize = True
        self.widthResizement = False
        self.heightResizement = False
        self.setMinimumSize(self.formerWidth - 5, self.formerHeight - 5)
        self.resize(self.formerWidth, self.formerHeight)
        self.setMaximumSize(1080, 1080-self.widthMinusHeight)
        if bool:
            self.center()
        else:
            self.move(pos[0], pos[1])
        self.initUI()

    def getBoard(self):
        return self.board

    def getScoreBoard(self):
        return self.scoreBoard

    def initUI(self):  # Create all instances of the main classes and set the main display
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

        self.setStyleSheet("background-color: light grey")
        self.setWindowTitle("GroupProject - Go - HGP-FT02")
        self.setWindowIcon(QIcon("./icons/go.png"))
        self.show()

    def showEndWindow(self):
        self.hide()
        self.endGameWindow.show()

    def updateEndWindow(self):
        self.endGameWindow.updateEndGameWindow()

    def resizeEvent(self, event):  # Require the resize to have diagonal proprotions
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


    def center(self):  # When the user open the app, center the window
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())
