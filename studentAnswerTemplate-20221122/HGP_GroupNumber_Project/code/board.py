from PyQt6.QtWidgets import QFrame, QProgressBar
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QPoint
from PyQt6.QtGui import QPainter, QPixmap, QPen, QBrush
from PyQt6.QtTest import QTest
from piece import Piece
from score_board import ScoreBoard

class Board(QFrame):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int) # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str) # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth  = 50     # board is 0 squares wide # TODO this needs updating
    boardHeight = 50     #
    timerSpeed  = 1000     # the timer updates every 1 millisecond
    counter     = 60    # the number the counter will count down from


    def __init__(self, parent):
        super().__init__(parent)
        self.initBoard()
        self.image = QPixmap("./icons/Board.png")


    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height())

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False      # game is not currently started
        self.start()                # start the game which will start the timer
        #0 représente une case vide, 1 représente les noirs (ce joueur commence) et 2 représente les blancs
        self.a = 0
        self.b = 0
        self.c = 0
        self.d = 0
        self.e = 0
        self.f = 0
        self.g = 0
        self.h = 0
        self.i = 0
        self.j = 0
        self.k = 0
        self.l = 0
        self.m = 0
        self.n = 0
        self.o = 0
        self.p = 0
        self.q = 0
        self.r = 0
        self.s = 0
        self.t = 0
        self.u = 0
        self.v = 0
        self.w = 0
        self.x = 0
        self.y = 0
        self.z = 0
        self.ab = 0
        self.ac = 0
        self.ad = 0
        self.ae = 0
        self.af = 0
        self.ag = 0
        self.ah = 0
        self.ai = 0
        self.aj = 0
        self.ak = 0
        self.al = 0
        self.am = 0
        self.an = 0
        self.ao = 0
        self.ap = 0
        self.aq = 0
        self.ar = 0
        self.ay = 0
        self.at = 0
        self.au = 0
        self.av = 0
        self.aw = 0
        self.ax = 0
        #il y'a 49 intersections donc on doit créer un tableau avc 49 cases et le remplir de 0, 1 ou 2
        '''[self.a, self.b, self.c, self.d, self.e, self.f, self.g],
          [self.h, self.i, self.j, self.k, self.l, self.m, self.n],
          [self.o, self.p, self.q, self.r, self.s, self.t, self.u],
          [self.v, self.w, self.x, self.y, self.z, self.ab, self.ac],
          [self.ad, self.ae, self.af, self.ag, self.ah, self.ai, self.aj],
          [self.ak, self.al, self.am, self.an, self.ao, self.ap, self.aq],
          [self.ar, self.ay, self.at, self.au, self.av, self.aw, self.ax],'''

        self.boardArray = []        # TODO - create a 2d int/Piece array to store the state of the game
        self.printBoardArray()    # TODO - uncomment this method after creating the array above

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))

    def mousePosToColRow(self, event):
        '''convert the mouse click event to a row and column'''

    def squareWidth(self):
        '''returns the width of one square in the board'''
        return self.contentsRect().width() / self.boardWidth

    def squareHeight(self):
        '''returns the height of one square of the board'''
        return self.contentsRect().height() / self.boardHeight

    def start(self):
        '''starts game'''
        self.isStarted = True                       # set the boolean which determines if the game has started to TRUE
        self.resetGame()                            # reset the game
        self.timer.start(self.timerSpeed, self)     # start the timer with the correct speed
        print("start () - timer is started")
        '''ScoreBoard.pbar.setValue(0)
        ScoreBoard.step = ScoreBoard.step + 1
        ScoreBoard.pbar.setValue(ScoreBoard.step)'''

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapt this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if self.counter == 1:
                print("Game over")
                self.timer.stop()
            self.counter -= 1
            print('timerEvent()', self.counter)
            self.updateTimerSignal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)      # if we do not handle an event we should pass it to the super
                                                        # class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.image)
        #self.drawBoardSquares(painter) #we don't draw the board bc we use a background
        self.drawPieces(painter)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location ["+str(event.position().x())+","+str(event.position().y())+"]"     # the location where a mouse click was registered
        print("mousePressEvent() - "+clickLoc)
        self.X = event.position().x()
        self.Y = event.position().y()
        print(self.X, self.Y)
        # TODO you could call some game logic here
        self.clickLocationSignal.emit(clickLoc)

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game
        '''
        self.image = QPixmap("./icons/Board.png")
        width = self.width()  # get the width of the current QImage in your application
        height = self.height()  # get the height of the current QImage in your application
        self.image = self.image.scaled(width, height)
        '''

    def tryMove(self, newX, newY):
        '''tries to move a piece'''
        '''
        Equation d'un cercle : (x−h)²+(y−k)²=r².
        Si newX et newY vérifie l'équation alors le point est dans la zone
        h : commence à 146 puis on ajoute 90 à chaque fois qu'on se décale sur la droite
        y : commence à 176 puis on ajoute 110 à chaque fois qu'on se décale vers le bas
        '''

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        # TODO set the default colour of the brush
        # draw settings (default)
        self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.GlobalColor.black  # documentation: https://doc.qt.io/qt-6/qt.html#GlobalColor-enum
        for row in range(0, Board.boardHeight):
            for col in range (0, Board.boardWidth):
                painter.save()
                colTransformation = self.squareWidth()* col # TODO set this value equal the transformation in the column direction
                rowTransformation = 0                       # TODO set this value equal the transformation in the row direction
                painter.translate(colTransformation,rowTransformation)
                painter.fillRect()                          # TODO provide the required arguments
                painter.restore()
                # TODO change the colour of the brush so that a checkered board is drawn

    def drawPieces(self, painter):
        '''draw the pieces on the board'''
        self.brushSize = 5
        #painter = QPainter(self.image)
        #if player 1 : Comment aller chercher l'attribut self.currentTurn de ScoreBoard ?
        painter.setPen(QPen(Qt.GlobalColor.black, self.brushSize))
        painter.setBrush(QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern))

        '''
        if player 2 :
        painter.setPen(QPen(Qt.GlobalColor.white, self.brushSize))
        painter.setBrush(QBrush(Qt.GlobalColor.white, Qt.BrushStyle.SolidPattern))
        
        '''
        radius = self.squareWidth() / 4
        center = QPointF(radius, radius)
        #painter.drawEllipse(center, radius, radius)
        painter.drawEllipse(125, 155, 50, 50)
        #A utiliser qu'à partir du moment où l'utilisateur clique sur la souris
        #painter.drawEllipse(self.X, self.Y, 400, 200)
        '''colour = Qt.GlobalColor.transparent # empty square could be modeled with transparent pieces
        for row in range(0, len(self.boardArray)):
            for col in range(0, len(self.boardArray[0])):
                painter.save()
                painter.translate()

                # TODO draw some the pieces as ellipses
                # TODO choose your colour and set the painter brush to the correct colour
                # draw settings (default)
                self.drawing = False
                self.brushSize = 3
                colour = Qt.GlobalColor.black
                radius = self.squareWidth() / 4
                center = QPointF(radius, radius)
                painter.drawEllipse(center, radius, radius)
                painter.restore()'''
