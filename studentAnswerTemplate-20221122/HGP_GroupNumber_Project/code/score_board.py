from PyQt6.QtWidgets import QApplication, QDockWidget, QGridLayout, QMessageBox, QGroupBox, QMenuBar, QProgressBar, QHBoxLayout, QVBoxLayout, QPushButton, QWidget, QLabel, QScrollArea
from PyQt6.QtCore import pyqtSlot, QSize, Qt, QBasicTimer
from PyQt6.QtGui import QIcon, QAction, QPixmap, QCursor, QPen, QPainter, QFont
from board import Board
class ScoreBoard(QWidget):
    '''# base the score_board on a QWidget'''

    def __init__(self, go):
        super().__init__()
        self.go = go
        self.initUI()


    def initUI(self):
        '''initiates ScoreBoard UI'''

        self.vboxMain = QVBoxLayout()
        self.firstTimer = False
        self.text = ""
        self.count = 0

        # Here we create 3 GroupBoxs to hold other widgets : one for Player 1, one for Player 2 and one for other things
        # needed to play the game.
        self.mainWidgetB = QGroupBox()
        self.mainWidgetB.setTitle("Player 1 - Black Stones")
        '''self.mainWidgetB.setStyleSheet("color: white;"
                                       "background-color: black")'''

        self.mainWidgetW = QGroupBox()
        self.mainWidgetW.setTitle("Player 2 - White Stones")
        '''self.mainWidgetW.setStyleSheet("color: black;"
                                       "background-color: white")'''
        self.mainWidgetM = QGroupBox()
        self.mainWidgetM.setTitle("Others")
        self.mainWidgetM.setStyleSheet("color: black;"
                                       "background-color: grey")

        self.mainLayoutB = QVBoxLayout()
        self.mainLayoutW = QVBoxLayout()
        self.mainLayoutM = QVBoxLayout()

        # Here we create all the Widgets needed for the game (label, button, timer...).
        self.label_timeRemainingW = QLabel("Time remaining: ")
        self.label_timeRemainingB = QLabel("Time remaining: ")
        self.currentTurn = "Player 1"
        self.playerLabel = QLabel("Current Turn: " + self.currentTurn)
        self.playerLabel.setStyleSheet("font-weight: bold")
        self.mainLayoutM.addWidget(self.playerLabel)
        self.captureW = QLabel("Captures : " + str(self.go.gameLogic.captured[1]))
        self.captureB= QLabel("Captures : " + str(self.go.gameLogic.captured[0]))
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
        self.timerButtonB.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.timerButtonW.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.timerButtonB.clicked.connect(self.buttonTimerB_clicked)
        self.timerButtonW.clicked.connect(self.buttonTimerW_clicked)
        self.pbarB = QProgressBar(self)
        self.pbarB.setMaximum(120)
        self.pbarB.setTextVisible(False)
        self.pbarW = QProgressBar(self)
        self.pbarW.setMaximum(120)
        self.pbarW.setTextVisible(False)
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
        self.skipButtonB.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.skipButtonB.clicked.connect(self.buttonSkip_clicked)
        self.mainLayoutB.addWidget(self.skipButtonB)
        self.skipButtonW.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.skipButtonW.clicked.connect(self.buttonSkip_clicked)
        self.mainLayoutW.addWidget(self.skipButtonW)
        closeButton = QPushButton('END GAME')
        closeButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        closeButton.clicked.connect(self.buttonEnd_cliked)
        self.rulesButton = QPushButton('How To Play', self)
        self.rulesButton.clicked.connect(self.rules)
        self.mainLayoutM.addWidget(self.rulesButton)
        self.mainLayoutM.addWidget(closeButton)
        self.rulesButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.borderRed()

        self.mainWidgetB.setLayout(self.mainLayoutB)
        self.mainWidgetW.setLayout(self.mainLayoutW)
        self.mainWidgetM.setLayout(self.mainLayoutM)
        self.vboxMain.addWidget(self.mainWidgetB)
        self.vboxMain.addWidget(self.mainWidgetW)
        self.vboxMain.addWidget(self.mainWidgetM)
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

    # Here we made the buttonEnd_clicked method to close the window when a player cliks on the End button and
    # to display the End Game Window if it is the end of the game.

    def buttonEnd_cliked(self):
        if self.go.board.draw:
            self.go.close()
        else:
            print("game over")
            self.go.gameLogic.scoreCount()
            self.go.updateEndWindow()
            self.go.close()
            self.go.endGameWindow.show()

    # Here we made the buttonTimerB_clicked method to start/stop the timer when the Player 1 cliks on the Timer button.
    def buttonTimerB_clicked(self):
        self.firstTimer = True
        if self.timer.isActive():
            self.firstTimer = False
            self.timerButtonB.setText('Start')
            self.timerButtonW.setText('Stop')
        elif self.timerButtonB.text() == 'Time Over':
            self.pbarB.setValue(0)
            self.stepB = 0
            self.pbarB.setStyleSheet("""
                                QProgressBar::chunk
                                {
                                    background-color: green
                                }""")
            self.timer.start(1000, self)
            self.timerButtonB.setText('Stop')
        else:
            self.timer.start(1000, self)
            self.timerButtonB.setText('Stop')

    # Here we made the buttonTimerW_clicked method to start/stop the timer when the Player 2 cliks on the Timer button.
    def buttonTimerW_clicked(self):
        self.firstTimer = False
        if self.timer.isActive():
            self.firstTimer = True
            self.timerButtonW.setText('Start')
            self.timerButtonB.setText('Stop')
        elif self.timerButtonW.text() == 'Time Over':
            self.pbarW.setValue(0)
            self.stepW = 0
            self.pbarW.setStyleSheet("""
                                QProgressBar::chunk
                                {
                                    background-color: green
                                }""")
            self.timer.start(1200, self)
            self.timerButtonW.setText('Stop')
        else:
            self.timer.start(1000, self)
            self.timerButtonW.setText('Stop')

    # Here we made the timerEvent method to set the timer.
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

        if self.stepB > 100:
            self.pbarB.setFormat('Hurry up!')
            self.pbarB.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.pbarB.setTextVisible(True)
            self.pbarB.setStyleSheet("""
                    QProgressBar::chunk
                    {
                        background-color: red
                    }""")
        if self.stepW > 100:
            self.pbarW.setFormat('Hurry up!')
            self.pbarW.setAlignment(Qt.AlignmentFlag.AlignCenter)
            self.pbarW.setTextVisible(True)
            self.pbarW.setStyleSheet("""
                    QProgressBar::chunk
                    {
                        background-color: red
                    }""")

        if self.stepB >= 120:
            self.timer.stop()
            self.timerButtonB.setText('Time Over')
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Time Over...")
            dialog.setWindowIcon(QIcon("./icons/timer.png"))
            text = "Player 1 looses, his time is over.\n" \
                   "Congratulations to Player 2, you win !"

            dialog.setText(text)
            button = dialog.exec()

            if button == QMessageBox.StandardButton.Ok:
                print("OK!")
        elif self.stepW >= 120:
            self.timer.stop()
            self.timerButtonW.setText('Time Over')
            dialog = QMessageBox(self)
            dialog.setWindowTitle("Time Over...")
            dialog.setWindowIcon(QIcon("./icons/timer.png"))
            text = "Player 2 looses, his time is  over.\n" \
                   "Congratulations to Player 1, you win !"

            dialog.setText(text)
            button = dialog.exec()

            if button == QMessageBox.StandardButton.Ok:
                print("OK!")

    # Here we made the clear method to reset the game.
    def clear(self):
        """self.go.board.image = QPixmap("./icons/Board.png")
        self.go.board.image = self.go.board.image.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)
        self.currentTurn = "Player 1"
        self.stepB = 0
        self.pbarB.setValue(self.stepB)
        self.label_timeRemainingB.setText('Time remaining:')
        self.stepW = 0
        self.pbarW.setValue(self.stepW)
        self.label_timeRemainingW.setText('Time remaining:')
        self.timerButtonB.setText('2 Minute Timer')
        self.timerButtonW.setText('2 Minute Timer')
        self.timer.stop()
        self.go.gameLogic.__init__()
        self.go.board.__init__()"""
        self.go.hide()
        self.go.__init__()
        """painter = QPainter(self.go.board.image)
        self.go.board.updateTheBoard(painter)
        self.update()
        self.updateUi()"""

    # Here we made the buttonSkip_clicked method to skip your turn and change the current player.
    def buttonSkip_clicked(self, s):
        self.history("a", "a")
        if self.currentTurn == "Player 1":
            self.currentTurn = "Player 2"
            self.go.gameLogic.currentPlayer = 2
            print(self.currentTurn)
            self.timerButtonB.setText('Start')
            self.timerButtonW.setText('Stop')
            self.firstTimer = False
            self.go.board.count += 1
            self.go.gameLogic.captured[1] += 1


        else:
            self.currentTurn = "Player 1"
            self.go.gameLogic.currentPlayer = 1
            print(self.currentTurn)
            self.timerButtonW.setText('Start')
            self.timerButtonB.setText('Stop')
            self.firstTimer = True
            self.go.board.count += 1
            self.go.gameLogic.captured[0] += 1
        self.updateUi()
        if self.go.board.count == 2:
            print("end")
            # Here we turn the boolean draw into false, and we display a MessageBox to explain that the game
            # is over (two consecutive passes terminates the game).
            self.go.board.draw = False
            dialog = QMessageBox(self)
            dialog.setWindowTitle("The End")
            dialog.setWindowIcon(QIcon("./icons/final.jpg"))
            text = "The gamer is over.\n" \
                   "Now, each your turn, click on the pieces you want to delete.\n" \
                   "When finished, clik on the button END GAME to find out the score and the winner! 😉 "

            dialog.setText(text)
            button = dialog.exec()

            if button == QMessageBox.StandardButton.Ok:
                print("OK!")

    def history(self, col, row):
        self.count += 1
        if col == "a" and row == "a":
            self.text += str(self.count) + "." + self.currentTurn + ":\t" + \
                     "skipped\n"
        else:
            self.text += str(self.count) + "." + self.currentTurn + ":\t" + \
                     "col: " + str(col) + "\trow: " + str(row) + "\n"

    # Here we made the matchDetails method to display the game history.
    def matchDetails(self):
        dialog = QMessageBox(self)
        dialog.setWindowTitle("Match Details")
        dialog.setWindowIcon(QIcon("./icons/compare-match-icon.png"))
        dialog.setText(self.text)
        button = dialog.exec()

        if button == QMessageBox.StandardButton.Ok:
            print("OK!")
        self.updateUi()

    # Here we made the borderRed method to change the GroupBox's border in red.
    # It changes depending on the current player.
    def borderRed(self):
        #if self.go.board.draw:
        if self.currentTurn == "Player 1":
            self.mainWidgetB.setObjectName("ColoredGroupBox")
            self.mainWidgetB.setStyleSheet("QGroupBox#ColoredGroupBox { border: 2px solid red;}")
            self.mainWidgetW.setObjectName("ColoredGroupBox")
            self.mainWidgetW.setStyleSheet("QGroupBox#ColoredGroupBox { border: 4px solid white;}")
        else:
            self.mainWidgetB.setStyleSheet("color: white;"
                                           "background-color: black")
            self.mainWidgetW.setObjectName("ColoredGroupBox")
            self.mainWidgetW.setStyleSheet("QGroupBox#ColoredGroupBox { border: 2px solid red;}")
            self.mainWidgetB.setObjectName("ColoredGroupBox")
            self.mainWidgetB.setStyleSheet("QGroupBox#ColoredGroupBox { border: 2px solid black;}")

    # Here we made the rules method to display a message box with the rules of the game.
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

    # Here we made the updateUI method to update the UI.
    def updateUi(self):
        self.playerLabel.setText("Current Turn: " + self.currentTurn)
        self.playerLabel.adjustSize()
        self.captureW.setText("Captures : " + str(self.go.gameLogic.captured[1]))
        self.captureW.adjustSize()
        self.captureB.setText("Captures : " + str(self.go.gameLogic.captured[0]))
        self.captureB.adjustSize()
        self.borderRed()










