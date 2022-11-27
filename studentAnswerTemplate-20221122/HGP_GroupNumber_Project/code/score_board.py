from PyQt6.QtWidgets import QDockWidget, QApplication, QToolBar, QProgressBar, QVBoxLayout, QPushButton, QWidget, QLabel #TODO import additional Widget classes as desired
from PyQt6.QtCore import pyqtSlot, QSize, Qt
from PyQt6.QtGui import QIcon, QAction
#from board import Board Pourquoi ça ne fonctionne pas ?
class ScoreBoard(QDockWidget):
    '''# base the score_board on a QDockWidget'''

    def __init__(self):
        super().__init__()
        self.initUI()


        #why it doesn't work ?
        '''mainMenu = self.menuBar()  # create a menu bar
        mainMenu.setNativeMenuBar(False)
        fileMenu = mainMenu.addMenu(
            " File")  # add the file menu to the menu bar, the space is required as "File" is reserved in Mac

        clearAction = QAction(QIcon("./icons/clear.png"), "Clear", self)  # create a clear action with a png as an icon
        clearAction.setShortcut("Ctrl+C")  # connect this clear action to a keyboard shortcut
        fileMenu.addAction(clearAction)  # add this action to the file menu
        clearAction.triggered.connect(self.clear)'''

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
        self.timerButton.clicked.connect(self.buttonTimer_clicked)
        self.pbar = QProgressBar(self)
        self.step = 0
        self.pbar.setOrientation(Qt.Orientation.Vertical)
        self.mainLayout.addWidget(self.timerButton)
        self.mainLayout.addWidget(self.pbar)
        closeButton = QPushButton('END GAME')
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
        '''updates the time remaining label to show the time remaining'''
        update = "Time Remaining:" + str(timeRemainng)
        self.label_timeRemaining.setText(update)
        print('slot '+update)
        # self.redraw()

        # Here I made the buttonEnd_clicked method to close the window when a player cliks on the End button
    def buttonEnd_cliked(self):
        self.close()
        #à retravailler

    def buttonTimer_clicked(self):
        print("test")
        #Board.start()


