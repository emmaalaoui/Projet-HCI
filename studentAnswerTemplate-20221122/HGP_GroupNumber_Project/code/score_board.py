from PyQt6.QtWidgets import QApplication, QDockWidget, QGridLayout, QMessageBox, QGroupBox, QMenuBar, QProgressBar, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QLabel, QScrollArea
from PyQt6.QtCore import pyqtSlot, QSize, Qt, QBasicTimer
from PyQt6.QtGui import QIcon, QAction, QPixmap, QCursor, QPen, QPainter
from board import Board
class ScoreBoard(QWidget):
    '''# base the score_board on a QDockWidget'''

    def __init__(self, go):
        super().__init__()
        self.go = go
        self.initUI()


    def initUI(self):
        '''initiates ScoreBoard UI'''

        self.vboxMain = QVBoxLayout()
        self.firstTimer = False
        self.firstSkip = False

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
        self.mainWidgetM.setTitle("Others")
        self.mainWidgetM.setStyleSheet("color: black;"
                                       "background-color: grey")
        '''self.mainWidgetR = QGroupBox()
        self.mainWidgetR.setTitle("Rules of Go")
        self.mainWidgetR.setStyleSheet("color: black;"
                                       "background-color: grey")'''
        self.mainLayoutB = QVBoxLayout()
        self.mainLayoutW = QVBoxLayout()
        self.mainLayoutM = QVBoxLayout()
        #self.mainLayoutR = QVBoxLayout()



        #self.mainWidgetB.setMaximumSize(self.width(), 250)
        #self.mainWidgetW.setMaximumSize(self.width(), 300)

        #create two labels which will be updated by signals
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemainingW = QLabel("Time remaining: ")
        self.label_timeRemainingB = QLabel("Time remaining: ")
        self.currentTurn = "Player 1"
        self.playerLabel = QLabel("Current Turn: " + self.currentTurn)
        self.mainLayoutM.addWidget(self.playerLabel)
        self.scoreW = QLabel("Score : ")
        self.scoreB = QLabel("Score : ")
        self.captureW = QLabel("Captures : " + str(self.go.gameLogic.captured[0]))
        self.captureB= QLabel("Captures : "+ str(self.go.gameLogic.captured[1]))
        #self.mainLayout.addWidget(self.label_clickLocation)
        self.mainLayoutW.addWidget(self.scoreW)
        self.mainLayoutB.addWidget(self.scoreB)
        self.mainLayoutW.addWidget(self.captureW)
        self.mainLayoutB.addWidget(self.captureB)
        self.matchButton = QPushButton("Match Details", self)
        self.matchButton.clicked.connect(self.matchDetails)
        self.matchButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        resetGame = QPushButton('Reset Game')
        resetGame.clicked.connect(self.clear)
        resetGame.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.mainLayoutM.addWidget(self.matchButton)
        self.mainLayoutM.addWidget(resetGame)
        self.timerButtonB = QPushButton('2 Minute Timer', self)
        self.timerButtonW = QPushButton('2 Minute Timer', self)
        self.timerButtonB.setStyleSheet("color: white;"
                                       "background-color: black;"
                                       "border-style: outset;"
                                       "border-width: 2px;"
                                       #"border-radius: 10px;"
                                       "border-color: white")
                                       #"font: bold 14px")

        self.timerButtonB.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.timerButtonW.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.timerButtonB.clicked.connect(self.buttonTimerB_clicked)
        self.timerButtonW.clicked.connect(self.buttonTimerW_clicked)
        self.pbarB = QProgressBar(self)
        self.pbarB.setMaximum(120)
        self.pbarB.setTextVisible(False)
        self.pbarB.setStyleSheet("border-style: solid;"
                                        #"border-width: 2px;"
                                        #"border-radius: 7px;"
                                        "text-align: center;"
                                        "background-color: white;"
                                        #"margin: 10px;"
                                        "border-color: black")
        # "font: bold 14px")
        self.pbarW = QProgressBar(self)
        self.pbarW.setMaximum(120)
        self.pbarW.setTextVisible(False)
        self.pbarW.setStyleSheet("border-style: solid;"
                                 # "border-width: 2px;"
                                 # "border-radius: 7px;"
                                 "text-align: center;"
                                 "background-color: white;"
                                 # "margin: 10px;"
                                 "border-color: black")
        self.stepB = 0
        self.stepW = 0
        self.timer = QBasicTimer()
        #self.pbarB.setOrientation(Qt.Orientation.Vertical)
        #self.pbarW.setOrientation(Qt.Orientation.Vertical)
        self.mainLayoutB.addWidget(self.timerButtonB)
        self.mainLayoutW.addWidget(self.timerButtonW)
        self.mainLayoutB.addWidget(self.pbarB)
        self.mainLayoutW.addWidget(self.pbarW)
        self.mainLayoutB.addWidget(self.label_timeRemainingB)
        self.mainLayoutW.addWidget(self.label_timeRemainingW)
        self.skipButtonB = QPushButton('Skip Turn')
        self.skipButtonW = QPushButton('Skip Turn')
        self.skipButtonB.setStyleSheet("color: white;"
                                        "background-color: black;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        #"border-radius: 10px;"
                                        "border-color: white")
                                        #"font: bold 14px")
        self.skipButtonB.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.skipButtonB.clicked.connect(self.buttonSkip_clicked)
        self.mainLayoutB.addWidget(self.skipButtonB)
        self.skipButtonW.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.skipButtonW.clicked.connect(self.buttonSkip_clicked)
        self.mainLayoutW.addWidget(self.skipButtonW)
        closeButton = QPushButton('END GAME')
        '''closeButton.setStyleSheet("color: white;"
                                        "background-color: black;"
                                        "border-style: outset;"
                                        "border-width: 2px;"
                                        "border-radius: 10px;"
                                        "border-color: white")
                                        # "font: bold 14px")'''
        closeButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        closeButton.clicked.connect(self.buttonEnd_cliked)

        '''self.scroll = QScrollArea()
        self.scroll.setWidget(QLabel("How To Play:"+"\n"+self.rules()))
        self.scroll.setWidgetResizable(True)
        #self.rules = QLabel("How To Play:"+"\n"+self.rules())
        self.mainLayoutR.addWidget(self.scroll)'''
        self.rulesButton = QPushButton('How To Play', self)
        self.rulesButton.clicked.connect(self.rules)
        self.mainLayoutM.addWidget(self.rulesButton)
        self.mainLayoutM.addWidget(closeButton)
        self.rulesButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.borderRed()
        #self.setWidget(self.mainWidgetB)
        #self.setWidget(self.mainWidgetW)

        self.mainWidgetB.setLayout(self.mainLayoutB)
        self.mainWidgetW.setLayout(self.mainLayoutW)
        self.mainWidgetM.setLayout(self.mainLayoutM)
        #self.mainWidgetR.setLayout(self.mainLayoutR)
        self.vboxMain.addWidget(self.mainWidgetB)
        self.vboxMain.addWidget(self.mainWidgetW)
        self.vboxMain.addWidget(self.mainWidgetM)
        #self.vboxMain.addWidget(self.mainWidgetR)
        self.setLayout(self.vboxMain)

    def center(self):
        '''centers the window on the screen, you do not need to implement this method'''

    def make_connection(self, board):
        '''this handles a signal sent from the board class'''
        # when the clickLocationSignal is emitted in board the setClickLocation slot receives it
        board.clickLocationSignal.connect(self.setClickLocation)
        # when the updateTimerSignal is emitted in the board the setTimeRemaining slot receives it
        #board.updateTimerSignal.connect(self.setTimeRemaining) #on n'utilise plus le timer de la prof ds board

    @pyqtSlot(str) # checks to make sure that the following slot is receiving an argument of the type 'int'
    def setClickLocation(self, clickLoc):
        '''updates the label to show the click location'''
        self.label_clickLocation.setText("Click Location:" + clickLoc)
        print('slot ' + clickLoc)

    '''Méthode de la prof pour afficher le timer de board
    @pyqtSlot(int)
    def setTimeRemaining(self, timeRemainng):
        updates the time remaining label to show the time remaining
        if timeRemainng > 60:
            update = "Time Remaining:" + "1 min " + str(timeRemainng - 60) + " s"
        else:
            update = "Time Remaining:" + str(timeRemainng) +" s"

        self.label_timeRemainingB.setText(update)
        print('slot '+update)
        #self.redraw()'''

        # Here I made the buttonEnd_clicked method to close the window when a player cliks on the End button
    def buttonEnd_cliked(self):
        self.go.close()

    def buttonTimerB_clicked(self):
        self.firstTimer = True
        if self.timer.isActive():
            #self.go.board.timer.stop()
            self.firstTimer = False
            self.timerButtonB.setText('Start')
            self.timerButtonW.setText('Stop')
        elif self.timerButtonB.text() == 'Time Over':
            self.pbarB.setValue(0)
            self.stepB = 0
            # I want that my progress bar updates during 2 minutes (to do a 2-minutes timer)
            # So I choose to start my timer every 1200 milliseconds because 1200 milliseconds equal 1.2 seconds
            # My progress bar max is 100 so 1.2*100 = 120 seconds --> 2 minutes
            #self.timer.start(1000, self)
            #self.go.board.start()
            #self.timerButtonB.setText('Stop')
        else:
            self.timer.start(1000, self)
            #self.go.board.start()
            self.timerButtonB.setText('Stop')

    def buttonTimerW_clicked(self):
        self.firstTimer = False
        if self.timer.isActive():
            self.firstTimer = True
            self.timerButtonW.setText('Start')
            self.timerButtonB.setText('Stop')
        elif self.timerButtonW.text() == 'Time Over':
            self.pbarW.setValue(0)
            self.stepW = 0
            # I want that my progress bar updates during 2 minutes (to do a 2-minutes timer)
            # So I choose to start my timer every 1200 milliseconds because 1200 milliseconds equal 1.2 seconds
            # My progress bar max is 100 so 1.2*100 = 120 seconds --> 2 minutes
            #self.timer.start(1200, self)
            #self.go.board.start()
            #self.timerButtonW.setText('Stop')
        else:
            self.timer.start(1000, self)
            #self.go.board.start()
            self.timerButtonW.setText('Stop')

    def timerEvent(self, e):

        if self.firstTimer:
            self.stepB = self.stepB + 1
            self.pbarB.setValue(self.stepB)
        else:
            self.stepW = self.stepW + 1
            self.pbarW.setValue(self.stepW)

        if self.stepB < 60:
            update = "Time Remaining: " + "1 min " + str(60 - self.stepB) + " s"
        else:
            update = "Time Remaining: " + str(120 - self.stepB) + " s"

        self.label_timeRemainingB.setText(update)
        print('slot ' + update)

        if self.stepW < 60:
            update = "Time Remaining: " + "1 min " + str(60 - self.stepW) + " s"
        else:
            update = "Time Remaining: " + str(120 - self.stepW) + " s"

        self.label_timeRemainingW.setText(update)
        print('slot ' + update)

        if self.stepB >= 120:
            self.timer.stop()
            self.timerButtonB.setText('Time Over')
        elif self.stepW >= 120:
            self.timer.stop()
            self.timerButtonW.setText('Time Over')

    def clear(self):
        self.go.board.image = QPixmap("./icons/Board.png")
        self.go.board.resize(800, 1000) #à retravailler !
        self.currentTurn = "Player 1"
        self.stepB = 0
        self.pbarB.setValue(self.stepB)
        self.label_timeRemainingB.setText('Time remaining:')
        self.stepW = 0
        self.pbarW.setValue(self.stepW)
        self.label_timeRemainingW.setText('Time remaining:')
        self.timer = 0
        self.timerButtonB.setText('2 Minute Timer')
        self.timerButtonW.setText('2 Minute Timer')
        '''width = self.width()  # get the width of the current QImage in your application
        height = self.height()  # get the height of the current QImage in your application
        self.go.board.image = image.scaled(height, height)'''
        self.update()
        self.updateUi()

    def buttonSkip_clicked(self, s):
        if self.currentTurn == "Player 1":
            self.currentTurn = "Player 2"
            print(self.currentTurn)
            self.timerButtonB.setText('Start')
            self.timerButtonW.setText('Stop')
            self.firstTimer = False

        else:
            self.currentTurn = "Player 1"
            print(self.currentTurn)
            self.timerButtonW.setText('Start')
            self.timerButtonB.setText('Stop')
            self.firstTimer = True
        self.updateUi()


    def matchDetails(self):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Match Details")
        dialog.setWindowIcon(QIcon("./icons/compare-match-icon.webp"))
        text = ""
        count = 0
        for i in range(0, 100, 1):
            #if self.go.board.tryMove():
                count = i
                text = str(count) + "."

        text += self.currentTurn
        dialog.setText(text)
        button = dialog.exec()

        if button == QMessageBox.StandardButton.Ok:
            print("OK!")

    def borderRed(self):
        if self.currentTurn == "Player 1":
            self.mainWidgetB.setObjectName("ColoredGroupBox")
            self.mainWidgetB.setStyleSheet("QGroupBox#ColoredGroupBox { border: 1px solid red;}")
            self.mainWidgetW.setObjectName("ColoredGroupBox")
            self.mainWidgetW.setStyleSheet("QGroupBox#ColoredGroupBox { border: 1px solid white;}")
        else:
            self.mainWidgetB.setStyleSheet("color: white;"
                                           "background-color: black")
            self.mainWidgetW.setObjectName("ColoredGroupBox")
            self.mainWidgetW.setStyleSheet("QGroupBox#ColoredGroupBox { border: 1px solid red;}")
            self.mainWidgetB.setObjectName("ColoredGroupBox")
            self.mainWidgetB.setStyleSheet("QGroupBox#ColoredGroupBox { border: 1px solid black;}")

    def rules(self):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Rules")
        dialog.setWindowIcon(QIcon("./icons/rules.png"))
        text = "A game of Go starts with an empty board.\n" \
                "Each player has an effectively unlimited supply\n" \
                "of pieces (called stones), one taking the black stones,\n" \
                "the other taking white ones. The main object of the game\n" \
                "is to use your stones to form territories by surrounding\n" \
                "vacant areas of the board. It is also possible to capture\n" \
                "your opponent's stones by completely surrounding them.\n" \
                "Players take turns, placing one of their stones\n" \
                "on a vacant point at each turn, with Black playing first.\n" \
                "Note that stones are placed on the intersections of the lines\n" \
                "rather than in the squares and once played stones are not moved.\n" \
                "However they may be captured, in which case they are removed,\n" \
                "and kept by the capturing player as prisoners.\n" \
                "Let the games begin ! 😊"

        dialog.setText(text)
        button = dialog.exec()

        if button == QMessageBox.StandardButton.Ok:
            print("OK!")

        # Here I made the updateUI method to update the UI
    def updateUi(self):
        self.playerLabel.setText("Current Turn: " + self.currentTurn)
        self.playerLabel.adjustSize()
        self.borderRed()

    def deletePiece(self, newX, newY):
        '''delete a piece on the board'''
        self.brushSize = 5
        print("aa")
        painter = QPainter(self.go.board.image)
        painter.setPen(QPen(Qt.GlobalColor.red, self.brushSize))
        painter.drawLine(int(newX)-20, int(newY)-20, int(newX)+40, int(newY)+40)
        painter.drawLine(int(newX) - 20, int(newY) + 40, int(newX) + 40, int(newY) - 20)
        self.update()

    def final(self):
        if self.buttonSkip_clicked():
            self.firstSkip = False
            print("cc")
        elif self.buttonSkip_clicked():
            self.firstSkip = True
            print("ff")
        '''if self.firstSkip | self.timerButtonB.text() == 'Timer Over' | self.timerButtonW.text() == 'Timer Over':
            self.go.board.draw = False
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Rules")
            dialog.setWindowIcon(QIcon("./icons/final.jpg"))
            text = "Click on the pieces you want to delete."

            dialog.setText(text)
            button = dialog.exec()

            if button == QMessageBox.StandardButton.Ok:
                print("OK!")
            for newX in range(54, 774, 90):
                for newY in range(64, 944, 110):
                    if (self.go.board.mouseX - newX) ** 2 + (self.go.board.mouseY - newY) ** 2 <= 30.0 ** 2:
                        self.deletePiece(newX, newY)
        self.update()'''







