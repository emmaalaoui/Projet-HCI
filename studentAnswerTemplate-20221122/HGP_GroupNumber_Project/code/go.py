from PyQt6.QtWidgets import QMainWindow, QHBoxLayout, QWidget,QLayout
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon
from board import Board
from score_board import ScoreBoard
from game_logic import GameLogic
from endGameWindow import EndGameWindow

class Go(QMainWindow):

    def __init__(self):
        super().__init__()
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
        #self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.scoreBoard)
        self.myScoreBoard = QHBoxLayout()
        self.myScoreBoard.addWidget(self.board, 6)
        self.myScoreBoard.addWidget(self.scoreBoard, 1)
        mainWidget = QWidget()
        mainWidget.setLayout(self.myScoreBoard)
        self.setCentralWidget(mainWidget)
        self.scoreBoard.make_connection(self.board)

        self.resize(850, 850)
        self.center()
        self.setStyleSheet("background-color: light grey")
        self.setWindowTitle("Project - Go - Emma&Yann")
        self.setWindowIcon(
            QIcon("./icons/logo.png"))
        self.show()

    def showEndWindow(self):
        self.hide()
        self.endGameWindow.show()
    def center(self):
        '''centers the window on the screen'''
        gr = self.frameGeometry()
        screen = self.screen().availableGeometry().center()

        gr.moveCenter(screen)
        self.move(gr.topLeft())
        #size = self.geometry()
        #self.move((screen.width() - size.width()) / 2,(screen.height() - size.height()) / 2)



