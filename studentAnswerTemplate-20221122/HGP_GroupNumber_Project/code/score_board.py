from PyQt6.QtWidgets import QDockWidget, QApplication, QMenuBar, QProgressBar, QVBoxLayout, QPushButton, QWidget, QLabel #TODO import additional Widget classes as desired
from PyQt6.QtCore import pyqtSlot, QSize, Qt, QBasicTimer
from PyQt6.QtGui import QIcon, QAction, QPixmap, QCursor
from board import Board
class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''

    def __init__(self, go):
        super().__init__()
        self.initUI()
        self.go = go

        mainMenu = QMenuBar() # create a menu bar
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(
            " File")  # add the file menu to the menu bar, the space is required as "File" is reserved in Mac

        clearAction = QAction(QIcon("./icons/clear.png"), "Clear", self)  # create a clear action with a png as an icon
        clearAction.setShortcut("Ctrl+C")  # connect this clear action to a keyboard shortcut
        fileMenu.addAction(clearAction)  # add this action to the file menu
        clearAction.triggered.connect(self.clear)

    def initUI(self):
        '''initiates ScoreBoard UI'''
        self.resize(200, 200)
        self.center()
        self.setWindowTitle('ScoreBoard')
        #create a widget to hold other widgets
        self.mainWidget = QWidget()
        self.mainLayout = QVBoxLayout()
        self.mainWidget.setMaximumSize(220, self.height())
        #self.toolbar = QToolBar("My main toolbar")
        #self.toolbar.setIconSize(QSize(16, 16))

        #create two labels which will be updated by signals
        self.label_clickLocation = QLabel("Click Location: ")
        self.label_timeRemaining = QLabel("Time remaining: ")
        self.currentTurn = "Player 1"
        self.playerLabel = QLabel("Current Turn: " + self.currentTurn)
        self.mainLayout.addWidget(self.playerLabel)
        self.mainWidget.setLayout(self.mainLayout)
        #self.mainLayout.addWidget(self.label_clickLocation)
        #self.toolbar.addWidget(self.label_clickLocation)
        self.mainLayout.addWidget(self.label_timeRemaining)
        #self.toolbar.addWidget(self.label_timeRemaining)
        self.timerButton = QPushButton('One Minute Timer', self)
        self.timerButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.timerButton.clicked.connect(self.buttonTimer_clicked)
        self.pbar = QProgressBar(self)
        self.step = 0
        self.timer = QBasicTimer()
        self.pbar.setOrientation(Qt.Orientation.Vertical)
        self.mainLayout.addWidget(self.timerButton)
        self.mainLayout.addWidget(self.pbar)
        skipButton = QPushButton('Skip Turn')
        skipButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        skipButton.clicked.connect(self.buttonSkip_clicked)
        self.mainLayout.addWidget(skipButton)
        closeButton = QPushButton('END GAME')
        closeButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        closeButton.clicked.connect(self.buttonEnd_cliked)
        self.mainLayout.addWidget(closeButton)
        #self.toolbar.addWidget(closeButton)
        #self.setWidget(self.toolbar)
        self.setWidget(self.mainWidget)
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
            self.timerButton.setText('Start')
        elif self.timerButton.text() == 'Time Over':
            self.pbar.setValue(0)
            self.step = 0
            # I want that my progress bar updates during 1 minute (to do a 1-minute timer)
            # So I choose to start my timer every 600 milliseconds because 600 milliseconds equal 0.6 seconds
            # My progress bar max is 100 so 0.6*100 = 60 seconds --> 1 minute
            self.timer.start(600, self)
            self.timerButton.setText('Stop')
        else:
            self.timer.start(600, self)
            self.timerButton.setText('Stop')
            board = Board(self)
            board.start()

    def timerEvent(self, e):
        if self.step >= 100:
            self.timer.stop()
            self.timerButton.setText('Time Over')

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
        self.timerButton.setText('One Minute Timer')
        board = Board(self)
        board.timer.stop() #ne fonctionne pas !
        self.updateUi()

        # Here I made the updateUI method to update the UI
    def updateUi(self):
        self.playerLabel.setText("Current Turn: " + self.currentTurn)
        self.playerLabel.adjustSize()




