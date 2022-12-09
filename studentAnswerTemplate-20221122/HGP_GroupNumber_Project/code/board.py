from PyQt6.QtWidgets import QProgressBar, QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPointF, QPoint, QRect
from PyQt6.QtGui import QPainter, QPixmap, QPen, QBrush, QCursor, QColor
from PyQt6.QtTest import QTest
import time
from piece import Piece


class Board(QWidget):  # base the board on a QFrame widget
    updateTimerSignal = pyqtSignal(int)  # signal sent when timer is updated
    clickLocationSignal = pyqtSignal(str)  # signal sent when there is a new click location

    # TODO set the board width and height to be square
    boardWidth = 6  # board is 0 squares wide # TODO this needs updating
    boardHeight = 6  #
    timerSpeed = 1000  # the timer updates every 1 millisecond
    counter = 120  # the number the counter will count down from

    def __init__(self, parent):
        super().__init__(parent)
        self.go = parent
        self.initBoard()
        self.image = QPixmap("./icons/Board.png")
        self.imageOrigin = QPixmap("./icons/Board.png")
        self.mainLabel = QLabel()
        self.mainLabel.setPixmap(self.image)
        self.mainLayout = QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.resize(800, 1000)
        self.draw = True
        '''self.cursor = QCursor()
        # self.image.setCursor(self.cursor)
        #self.cursor.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.cursor.setShape(Qt.CursorShape.ArrowCursor)
        QApplication.setOverrideCursor(self.cursor)
        print(self.cursor.shape())'''

    def resizeEvent(self, event):
        '''if self.contentsRect().width() > self.contentsRect().height():
            new_size = self.image.scaled(self.height(), self.height())
        else:
            new_size = self.image.scaled(self.width(), self.width())'''
        self.image = self.image.scaled(self.width(), self.height())

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False  # game is not currently started

        '''#self.start()                # start the game which will start the timer
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
        [self.a, self.b, self.c, self.d, self.e, self.f, self.g],
          [self.h, self.i, self.j, self.k, self.l, self.m, self.n],
          [self.o, self.p, self.q, self.r, self.s, self.t, self.u],
          [self.v, self.w, self.x, self.y, self.z, self.ab, self.ac],
          [self.ad, self.ae, self.af, self.ag, self.ah, self.ai, self.aj],
          [self.ak, self.al, self.am, self.an, self.ao, self.ap, self.aq],
          [self.ar, self.ay, self.at, self.au, self.av, self.aw, self.ax],'''
        self.boardArray = self.go.gameLogic.boardState  # TODO - create a 2d int/Piece array to store the state of the game
        self.printBoardArray()  # TODO - uncomment this method after creating the array above

    def printBoardArray(self):
        '''prints the boardArray in an attractive way'''
        print("boardArray:")
        print('\n'.join(['\t'.join([str(cell) for cell in row]) for row in self.boardArray]))
        '''
        if gameLogic.boardState.owner == 1
            painter.setPen(QPen(Qt.GlobalColor.white, self.brushSize))
            painter.setBrush(QBrush(Qt.GlobalColor.white, Qt.BrushStyle.SolidPattern))
            painter.drawEllipse(int(self.mouseX)-20, int(self.mouseY)-20, 50, 50)
            self.update()
        elif gameLogic.boardState.owner == 2
            same in black..  

        '''

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
        self.isStarted = True  # set the boolean which determines if the game has started to TRUE
        self.resetGame()  # reset the game
        self.timer.start(self.timerSpeed, self)  # start the timer with the correct speed
        print("start () - timer is started")

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
            # self.go.scoreBoard.setTimeRemaining(self.counter)
        else:
            super(Board, self).timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.image)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        clickLoc = "click location [" + str(event.position().x()) + "," + str(
            event.position().y()) + "]"  # the location where a mouse click was registered
        print("mousePressEvent() - " + clickLoc)
        self.mouseX = event.position().x()
        self.mouseY = event.position().y()
        print(self.mouseX, self.mouseY)
        # TODO you could call some game logic here
        self.clickLocationSignal.emit(clickLoc)
        # self.drawPieces()
        self.tryMove()

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game
        '''
        self.image = QPixmap("./icons/Board.png")
        width = self.width()  # get the width of the current QImage in your application
        height = self.height()  # get the height of the current QImage in your application
        self.image = self.image.scaled(width, height)
        '''

    def tryMove(self):
        '''tries to move a piece'''
        if self.draw:
            for newX in range(54, 594, 90):
                for newY in range(64, 724, 110):
                    if (self.mouseX - newX) ** 2 + (self.mouseY - newY) ** 2 <= 30.0 ** 2:
                        # self.cursor.setShape(Qt.CursorShape.PointingHandCursor)
                        # QApplication.setOverrideCursor(self.cursor)
                        col, row = self.pixelToInt(newX, newY)
                        if self.go.gameLogic.placeForPlayer[self.go.gameLogic.currentPlayer - 1][col][row]:
                            self.drawPieces(newX, newY, col, row)
                            # self.pixelToInt(newX, newY)  # affiche la colonne et la ligne de la pièce
                            if self.go.scoreBoard.currentTurn == "Player 1":
                                self.go.scoreBoard.currentTurn = "Player 2"
                            else:
                                self.go.scoreBoard.currentTurn = "Player 1"
                            self.go.scoreBoard.updateUi()
        '''
        Equation d'un cercle : (x−h)²+(y−k)²=r².
        Si newX et newY vérifie l'équation alors le point est dans la zone
        h : commence à 146 puis on ajoute 90 à chaque fois qu'on se décale sur la droite
        y : commence à 176 puis on ajoute 110 à chaque fois qu'on se décale vers le bas
        '''

    def pixelToInt(self, mouseX, mouseY):
        countC = -1
        countR = -1
        finalC = -1
        finalR = -1
        for i in range(54, 594, 90):
            countC += 1
            if i == mouseX:
                finalC = countC

        for j in range(64, 724, 110):
            countR += 1
            if j == mouseY:
                finalR = countR
        print(finalC, finalR)
        return finalC, finalR

    def drawBoardSquares(self, painter):
        '''draw all the square on the board'''
        self.brushSize = 3
        self.brushColor = Qt.GlobalColor.black
        painter.setPen(QPen(self.brushColor, self.brushSize))
        painter.fillRect(QRect(0, 0, self.contentsRect().width(), self.contentsRect().height()),
                         self.go.backgroundColor)

        if self.squareWidth() <= self.squareHeight():
            squareSide = self.squareWidth()
        else:
            squareSide = self.squareHeight()
        for row in range(0, Board.boardHeight):
            for col in range(0, Board.boardWidth):
                painter.save()
                colTransformation = squareSide * 0.5 + squareSide * col
                rowTransformation = squareSide * 0.5 + squareSide * row
                painter.fillRect(
                    QRect(int(colTransformation), int(rowTransformation), int(squareSide), int(squareSide)),
                    QColor("#E0BD6B"))
                painter.drawRect(
                    QRect(int(colTransformation), int(rowTransformation), int(squareSide), int(squareSide)))
                painter.restore()
                self.brushColor = self.go.backgroundColor

        # TODO set the default colour of the brush
        # draw settings (default)
        """self.drawing = False
        self.brushSize = 3
        self.brushColor = Qt.GlobalColor.black  # documentation: https://doc.qt.io/qt-6/qt.html#GlobalColor-enum
        for row in range(0, Board.boardHeight):
            for col in range (0, Board.boardWidth):
                row += 1
                col += 1
                painter.drawRect(row, col, 100, 100)

                painter.save()
                colTransformation = self.squareWidth()* col # TODO set this value equal the transformation in the column direction
                rowTransformation = 0                       # TODO set this value equal the transformation in the row direction
                painter.translate(colTransformation,rowTransformation)
                painter.fillRect(colTransformation, rowTransformation)     # TODO provide the required arguments
                painter.restore()
                # TODO change the colour of the brush so that a checkered board is drawn
                self.brushColor = Qt.GlobalColor.white"""

    def drawPieces(self, newX, newY, col, row):
        '''draw the pieces on the board'''
        self.brushSize = 5
        painter = QPainter(self.image)
        if self.go.scoreBoard.currentTurn == "Player 1":
            painter.setPen(QPen(Qt.GlobalColor.black, self.brushSize))
            painter.setBrush(QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern))
            painter.drawEllipse(int(newX) - 20, int(newY) - 20, 50, 50)
            self.update()
            self.go.gameLogic.update(Piece(col, row, self.go.gameLogic.currentPlayer))
            self.updateTheBoard(painter)
        else:
            painter.setPen(QPen(Qt.GlobalColor.white, self.brushSize))
            painter.setBrush(QBrush(Qt.GlobalColor.white, Qt.BrushStyle.SolidPattern))
            painter.drawEllipse(int(newX) - 20, int(newY) - 20, 50, 50)
            self.update()
            self.go.gameLogic.update(Piece(col, row, self.go.gameLogic.currentPlayer))
            self.updateTheBoard(painter)

        # painter.drawEllipse(125, 155, 50, 50)
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

    def updateTheBoard(self, painter):
        self.imageOrigin = self.imageOrigin.scaled(self.width(), self.height())
        painter.drawPixmap(QPoint(), self.imageOrigin)
        self.brushSize = 5
        row = -1
        for newX in range(54, 594, 90):
            col = -1
            row = row + 1
            for newY in range(64, 724, 110):
                col = col + 1
                if self.go.gameLogic.boardState[row][col].owner != 0:
                    if self.go.gameLogic.boardState[row][col].owner == 1:
                        painter.setPen(QPen(Qt.GlobalColor.black, self.brushSize))
                        painter.setBrush(QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern))
                    else:
                        painter.setPen(QPen(Qt.GlobalColor.white, self.brushSize))
                        painter.setBrush(QBrush(Qt.GlobalColor.white, Qt.BrushStyle.SolidPattern))
                    painter.drawEllipse(int(newX) - 20, int(newY) - 20, 50, 50)
                    self.update()

        """painter.setPen(QPen(Qt.GlobalColor.green, self.brushSize))
        painter.setBrush(QBrush(Qt.GlobalColor.green, Qt.BrushStyle.SolidPattern))
        painter.drawEllipse(150 - 20, 150 - 20, 50, 50)
        self.update()"""