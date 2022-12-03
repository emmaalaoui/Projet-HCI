from PyQt6.QtWidgets import QApplication, QDockWidget, QGridLayout, QGroupBox, QMenuBar, QProgressBar, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QLabel #TODO import additional Widget classes as desired
from PyQt6.QtCore import pyqtSlot, QSize, Qt, QBasicTimer
from PyQt6.QtGui import QIcon, QAction, QPixmap, QCursor
from board import Board
class ScoreBoard(QWidget):
    '''# base the score_board on a QDockWidget'''

    def __init__(self, go):
        super().__init__()
        self.initUI()
        self.go = go

    def initUI(self):
        '''initiates ScoreBoard UI'''
        ''''IMPORTANT '''
        # pour t'expliquer, j'aimerai créer 3 QGroupBox : une pour le player 1, une pour le player 2 et une autre pour les
        # match details sauf que pour avoir 3 QGroupBox à la suite il faut créer une GridLayout et y ajouter les QGroupBox
        # sauf que pour l'instant la grid se créée dans une nouvelle fenêtre au lieu de se mettre à droite du plateau
        # peux-tu regarder dans la classe go stp ? Merci :)
        # B pour black, W pour white, M pour match et R pour rules

        self.grid = QGridLayout()
        self.setLayout(self.grid)

        #self.resize(200, 200)
        #self.center()
        #self.setWindowTitle('ScoreBoard')

        #create a widget to hold other widgets
        self.mainWidgetB = QGroupBox()
        self.mainWidgetB.setTitle("Player 1 - Black Stones")
        self.mainWidgetB.setStyleSheet("color: white;"
                                       "background-color: black")

        self.mainWidgetW = QGroupBox()
        self.mainWidgetW.setTitle("Player 2 - White Stones")
        self.mainWidgetW.setStyleSheet("color: black;"
                                       "background-color: white")
        self.mainWidgetM = QGroupBox()
        self.mainWidgetM.setTitle("Match Details")
        self.mainWidgetM.setStyleSheet("color: black;"
                                       "background-color: white")
        self.mainWidgetR = QGroupBox()
        self.mainWidgetR.setTitle("Rules of Go")
        self.mainWidgetR.setStyleSheet("color: black;"
                                       "background-color: white")
        self.mainLayoutB = QVBoxLayout()
        self.mainLayoutW = QVBoxLayout()
        self.mainLayoutM = QVBoxLayout()
        self.mainLayoutR = QVBoxLayout()



        #self.mainWidgetB.setMaximumSize(self.width(), 250)
        #self.mainWidgetW.setMaximumSize(self.width(), 300)

        #create two labels which will be updated by signals
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemainingW = QLabel("Time remaining: ")
        self.label_timeRemainingB = QLabel("Time remaining: ")
        self.currentTurn = "Player 1"
        self.playerLabelB = QLabel("Current Turn: " + self.currentTurn)
        self.playerLabelW = QLabel("Current Turn: " + self.currentTurn)
        self.mainLayoutB.addWidget(self.playerLabelB)
        self.mainLayoutW.addWidget(self.playerLabelW)
        self.scoreW = QLabel("Score : ")
        self.scoreB = QLabel("Score : ")
        self.captureW = QLabel("Captures : ")
        self.captureB= QLabel("Captures : ")
        #self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayoutB.addWidget(self.label_timeRemainingB)
        self.mainLayoutW.addWidget(self.label_timeRemainingW)
        self.mainLayoutW.addWidget(self.scoreW)
        self.mainLayoutB.addWidget(self.scoreB)
        self.mainLayoutW.addWidget(self.captureW)
        self.mainLayoutB.addWidget(self.captureB)
        self.details = QLabel("Match Details :"+"\n"+self.matchDetails())
        resetGame = QPushButton('Reset Game')
        resetGame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.mainLayoutM.addWidget(self.details)
        self.mainLayoutM.addWidget(resetGame)
        self.timerButtonB = QPushButton('One Minute Timer', self)
        self.timerButtonW = QPushButton('One Minute Timer', self)
        self.timerButtonB.setStyleSheet("color: white;"
                                       "background-color: black;"
                                       "border-style: outset;"
                                       "border-width: 2px;"
                                       #"border-radius: 10px;"
                                       "border-color: white")
                                       #"font: bold 14px")

        self.timerButtonB.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.timerButtonW.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.timerButtonB.clicked.connect(self.buttonTimer_clicked)
        self.timerButtonW.clicked.connect(self.buttonTimer_clicked)
        self.pbarB = QProgressBar(self)
        self.pbarW = QProgressBar(self)
        self.step = 0
        self.timer = QBasicTimer()
        self.pbarB.setOrientation(Qt.Orientation.Vertical)
        self.pbarW.setOrientation(Qt.Orientation.Vertical)
        self.mainLayoutB.addWidget(self.timerButtonB)
        self.mainLayoutW.addWidget(self.timerButtonW)
        self.mainLayoutB.addWidget(self.pbarB)
        self.mainLayoutW.addWidget(self.pbarW)
        skipButtonB = QPushButton('Skip Turn')
        skipButtonW = QPushButton('Skip Turn')
        skipButtonB.setStyleSheet("color: white;"
                                        "background-color: black;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        # "border-radius: 10px;"
                                        "border-color: white")
        # "font: bold 14px")
        skipButtonB.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        skipButtonW.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        skipButtonB.clicked.connect(self.buttonSkip_clicked)
        skipButtonW.clicked.connect(self.buttonSkip_clicked)
        self.mainLayoutB.addWidget(skipButtonB)
        self.mainLayoutW.addWidget(skipButtonW)
        closeButtonB = QPushButton('END GAME')
        closeButtonB.setStyleSheet("color: white;"
                                        "background-color: black;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        # "border-radius: 10px;"
                                        "border-color: white")
        # "font: bold 14px")
        closeButtonB.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        closeButtonB.clicked.connect(self.buttonEnd_cliked)
        closeButtonW = QPushButton('END GAME')
        closeButtonW.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        closeButtonW.clicked.connect(self.buttonEnd_cliked)
        self.mainLayoutB.addWidget(closeButtonB)
        self.mainLayoutW.addWidget(closeButtonW)
        self.rules = QLabel("How To Play:"+"\n"+self.rules())
        self.mainLayoutR.addWidget(self.rules)

        #self.setWidget(self.mainWidgetB)
        #self.setWidget(self.mainWidgetW)

        self.mainWidgetB.setLayout(self.mainLayoutB)
        self.mainWidgetW.setLayout(self.mainLayoutW)
        self.mainWidgetM.setLayout(self.mainLayoutM)
        self.mainWidgetR.setLayout(self.mainLayoutR)
        self.grid.addWidget(self.mainWidgetB, 0, 0)
        self.grid.addWidget(self.mainWidgetW, 1, 0)
        self.grid.addWidget(self.mainWidgetM, 2, 0)
        self.grid.addWidget(self.mainWidgetR, 3, 0)
        self.show()

    def center(self):
        '''centers the window on the screen, you do not need to implement this method'''

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        board.updateTimerSignal.connect(self.setTimeRemaining)

    @pyqtSlot(str) # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location:" + clickLoc)
        print('slot ' + clickLoc)

    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        print("cc")
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining:" + str(timeRemainng)
        self.label_timeRemaining.setText(update)
        print('slot '+update)
        #self.redraw()

        # Here I made the buttonEnd_clicked method to close the window when a player cliks on the End button
    def buttonEnd_cliked(self):
        self.go.close()
        #à retravailler

    def buttonTimer_clicked(self):
        if self.timer.isActive():
            self.timer.stop()
            self.timerButtonB.setText('Start')
            self.timerButtonW.setText('Start')
        elif self.timerButtonB.text() == 'Time Over' | self.timerButtonW.text() == 'Time Over':
            self.pbar.setValue(0)
            self.step = 0
            # I want that my progress bar updates during 1 minute (to do a 1-minute timer)
            # So I choose to start my timer every 600 milliseconds because 600 milliseconds equal 0.6 seconds
            # My progress bar max is 100 so 0.6*100 = 60 seconds --> 1 minute
            self.timer.start(600, self)
            self.timerButtonB.setText('Stop')
            self.timerButtonW.setText('Stop')
        else:
            self.timer.start(600, self)
            self.timerButtonB.setText('Stop')
            self.timerButtonW.setText('Stop')
            board = Board(self)
            board.start()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.timerButtonB.setText('Time Over')
            self.timerButtonW.setText('Time Over')

        self.step = self.step + 1
        self.pbar.setValue(self.step)

    def clear(self):
        self.image = QPixmap("./icons/Board.png")
        width = self.width()  # get the width of the current QImage in your application
        height = self.height()  # get the height of the current QImage in your application
        self.image = self.image.scaled(width, height)

    def buttonSkip_clicked(self, s):
        if self.currentTurn == "Player 1":
            self.currentTurn = "Player 2"
            print(self.currentTurn)

        else:
            self.currentTurn = "Player 1"
            print(self.currentTurn)
        self.pbar.setValue(0)
        self.step = 0
        self.timer.stop()
        #self.timerButtonB.setText('One Minute Timer')
        self.timerButtonW.setText('One Minute Timer')
        board = Board(self)
        board.timer.stop() #ne fonctionne pas !
        self.updateUi()

    def matchDetails(self):
        self.text = ""
        count = 0
        #board = Board(self)
        for i in range(0, 100, 1):
            # if board.tryMove():
            count = i
            self.text = str(count) + "."



        self.text += self.currentTurn
        return self.text

    def rules(self):

        text1 = "A game of Go starts with an empty board. Each player has an effectively unlimited supply of pieces"
        text2 = " (called stones), one taking the black stones, the other taking white." + "\n"
        text3 = "The main object of the game is to use your stones to form territories by surrounding vacant areas of the board." + "\n"
        text4 = "It is also possible to capture your opponent's stones by completely surrounding them."+"\n"
        text5 ="Players take turns, placing one of their stones on a vacant point at each turn, with Black playing first."+"\n"
        text6 = "Note that stones are placed on the intersections of the lines rather than in the squares and once played stones are not moved."+"\n"
        text7 = "However they may be captured, in which case they are removed from the board, and kept by the capturing player as prisoners."
        text8= "\n" + "Let the games begin ! 😊"

        text = text1+text2+text3+text4+text5+text6+text7+text8
        return text




        # Here I made the updateUI method to update the UI
    def updateUi(self):
        #self.playerLabelB.setText("Current Turn: " + self.currentTurn)
        #self.playerLabelB.adjustSize()
        self.playerLabelW.setText("Current Turn: " + self.currentTurn)
        self.playerLabelW.adjustSize()




