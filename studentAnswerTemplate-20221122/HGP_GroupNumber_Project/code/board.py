from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QBasicTimer, pyqtSignal, QPoint, QRect
from PyQt6.QtGui import QPainter, QPixmap, QPen, QBrush, QCursor, QColor, QMouseEvent
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
        self.draw = True
        self.count = 0
        self.setMouseTracking(True)
        # Here we create 4 different cursors depending on mouse position and game state.
        self.whiteCursor = QCursor(QPixmap("./icons/White.png"))
        self.blackCursor = QCursor(QPixmap("./icons/Black.png"))
        self.normalCursor = QCursor(QPixmap("./icons/Cursor.png"))
        self.crossCursor = QCursor(QPixmap("./icons/Cross.png"))
        self.setCursor(self.normalCursor)

    # Here we create the resizeEvent method to resize the board.
    def resizeEvent(self, event):
        self.image = self.image.scaled(self.width(), self.height(), Qt.AspectRatioMode.KeepAspectRatioByExpanding)

    def initBoard(self):
        '''initiates board'''
        self.timer = QBasicTimer()  # create a timer for the game
        self.isStarted = False  # game is not currently started
        self.boardArray = self.go.gameLogic.boardState  # TODO - create a 2d int/Piece array to store the state of the game

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

    def timerEvent(self, event):
        '''this event is automatically called when the timer is updated. based on the timerSpeed variable '''
        # TODO adapt this code to handle your timers
        if event.timerId() == self.timer.timerId():  # if the timer that has 'ticked' is the one in this class
            if self.counter == 1:
                self.timer.stop()
            self.counter -= 1
            self.updateTimerSignal.emit(self.counter)
        else:
            super(Board, self).timerEvent(event)  # if we do not handle an event we should pass it to the super
            # class for handling

    def paintEvent(self, event):
        '''paints the board and the pieces of the game'''
        painter = QPainter(self)
        painter.drawPixmap(QPoint(), self.image)

    def mousePressEvent(self, event):
        '''this event is automatically called when the mouse is pressed'''
        self.mouseX = event.position().x()
        self.mouseY = event.position().y()
        # TODO you could call some game logic here
        # self.drawPieces()
        self.tryMove()

    # Here we create the mouseMoveEvent to put the conditions to the cursors.
    def mouseMoveEvent(self, a0: QMouseEvent) -> None:
        col = -1
        itIsIn = False
        forCross = False
        for newX in range(int(8.434 * self.image.width() / 100), int(92 * self.image.width() / 100),
                          int(13.855 * self.image.width() / 100)):
            col = col + 1
            row = -1
            for newY in range(int(8.434 * self.image.width() / 100), int(92 * self.image.width() / 100),
                              int(13.855 * self.image.width() / 100)):
                row = row + 1

                if (a0.position().x() - newX) ** 2 + (a0.position().y() - newY) ** 2 <= 30.0 ** 2 and self.go.gameLogic.placeForPlayer[self.go.gameLogic.currentPlayer - 1][col][row]:
                    itIsIn = True
                if (a0.position().x() - newX) ** 2 + (a0.position().y() - newY) ** 2 <= 30.0 ** 2 and self.go.gameLogic.boardState[col][row].owner != 0:
                    forCross = True
        if not self.draw:
            if forCross and self.cursor() != self.crossCursor:
                self.setCursor(self.crossCursor)
            elif not forCross and self.cursor() != self.normalCursor:
                self.setCursor(self.normalCursor)
        else:
            if itIsIn and self.cursor() == self.normalCursor:
                if self.go.gameLogic.currentPlayer == 2:
                    self.setCursor(self.whiteCursor)
                else:
                    self.setCursor(self.blackCursor)
            elif not itIsIn and self.cursor() != self.normalCursor:
                    self.setCursor(self.normalCursor)

    def resetGame(self):
        '''clears pieces from the board'''
        # TODO write code to reset game

    # Here we create the method tryMove to allow the player to make a move.
    def tryMove(self):
        '''tries to move a piece'''
        self.count = 0
        if self.draw:
            for newX in range(int(8.434*self.image.width()/100), int(92*self.image.width()/100), int(13.855*self.image.width()/100)):
                for newY in range(int(8.434*self.image.width()/100), int(92*self.image.width()/100), int(13.855*self.image.width()/100)):
                    if (self.mouseX - newX) ** 2 + (self.mouseY - newY) ** 2 <= 30.0 ** 2:
                        # self.cursor.setShape(Qt.CursorShape.PointingHandCursor)
                        # QApplication.setOverrideCursor(self.cursor)
                        col, row = self.pixelToInt(newX, newY)
                        if self.go.gameLogic.placeForPlayer[self.go.gameLogic.currentPlayer - 1][col][row]:
                            self.go.scoreBoard.history(col, row)
                            self.drawPieces(newX, newY, col, row)
                            # self.pixelToInt(newX, newY)  # affiche la colonne et la ligne de la pièce
                            if self.go.scoreBoard.currentTurn == "Player 1":
                                self.go.scoreBoard.currentTurn = "Player 2"
                            else:
                                self.go.scoreBoard.currentTurn = "Player 1"
                            self.go.scoreBoard.updateUi()
        else:
            for newX in range(int(8.434 * self.image.width() / 100), int(92 * self.image.width() / 100), int(13.855 * self.image.width() / 100)):
                for newY in range(int(8.434 * self.image.width() / 100), int(92 * self.image.width() / 100), int(13.855 * self.image.width() / 100)):
                    if (self.mouseX - newX) ** 2 + (self.mouseY - newY) ** 2 <= 30.0 ** 2:
                        col, row = self.pixelToInt(newX, newY)
                        if self.go.gameLogic.boardState[col][row].owner != 0:
                            self.go.gameLogic.captured[self.go.gameLogic.boardState[col][row].owner % 2] += 1
                            self.go.gameLogic.boardState[col][row].owner = 0
                            self.deletePiece(newX, newY)
                            self.go.scoreBoard.updateUi()
        '''
        Equation of a circle : (x−h)²+(y−k)²=r².
        '''

    # Here we create the method pixelToInt to convert the position of the mouse (in pixel) in one column and one row.
    def pixelToInt(self, mouseX, mouseY):
        countC = -1
        countR = -1
        finalC = -1
        finalR = -1
        for i in range(int(8.434 * self.image.width() / 100), int(92 * self.image.width() / 100), int(13.855 * self.image.width() / 100)):
            countC += 1
            if i == mouseX:
                finalC = countC

        for j in range(int(8.434 * self.image.width() / 100), int(92 * self.image.width() / 100), int(13.855 * self.image.width() / 100)):
            countR += 1
            if j == mouseY:
                finalR = countR
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

    # Here we create the method drawPieces to draw the pieces (black and white).
    def drawPieces(self, newX, newY, col, row):
        '''draw the pieces on the board'''
        self.brushSize = 5
        painter = QPainter(self.image)
        if self.go.scoreBoard.currentTurn == "Player 1":
            painter.setPen(QPen(Qt.GlobalColor.black, self.brushSize))
            painter.setBrush(QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern))
            radius = int(25 * self.image.width() / 490)
            painter.drawEllipse(int(newX) - int(radius ** 0.5), int(newY) - int(radius ** 0.5), radius * 2, radius * 2)
            self.update()
            self.go.gameLogic.update(Piece(col, row, self.go.gameLogic.currentPlayer))
            self.updateTheBoard(painter)
        else:
            painter.setPen(QPen(Qt.GlobalColor.white, self.brushSize))
            painter.setBrush(QBrush(Qt.GlobalColor.white, Qt.BrushStyle.SolidPattern))
            radius = int(25 * self.image.width() / 490)
            painter.drawEllipse(int(newX) - int(radius / 2 ** 0.5), int(newY) - int(radius / 2 ** 0.5), radius * 2, radius * 2)
            self.update()
            self.go.gameLogic.update(Piece(col, row, self.go.gameLogic.currentPlayer))
            self.updateTheBoard(painter)

    # Here we create the method deletePiece to allow the player to delete the pieces he wants at the end of the game.
    def deletePiece(self, newX, newY):
        '''delete a piece on the board'''
        self.brushSize = 5
        painter = QPainter(self.image)
        painter.setPen(QPen(Qt.GlobalColor.red, self.brushSize))
        radius = int(20 * self.image.width() / 490)
        painter.drawLine(int(newX) - int(radius), int(newY) - int(radius), int(newX) + 2*int(radius), int(newY) + 2*int(radius))
        painter.drawLine(int(newX) - int(radius), int(newY) + 2*int(radius), int(newX) + 2*int(radius), int(newY) - int(radius))
        self.update()

    # Here we create the method updateTheBoard to update the board when a piece is placed or captured for example.
    def updateTheBoard(self, painter):
        self.imageOrigin = self.imageOrigin.scaled(self.width(), self.height())
        painter.drawPixmap(QPoint(), self.imageOrigin)
        self.brushSize = 5
        row = -1
        for newX in range(int(8.434 * self.image.width() / 100), int(92 * self.image.width() / 100), int(13.855 * self.image.width() / 100)):
            col = -1
            row = row + 1
            for newY in range(int(8.434 * self.image.width() / 100), int(92 * self.image.width() / 100), int(0.96*13.855 * self.image.width() / 100)):
                col = col + 1
                if self.go.gameLogic.boardState[row][col].owner != 0:
                    if self.go.gameLogic.boardState[row][col].owner == 1:
                        painter.setPen(QPen(Qt.GlobalColor.black, self.brushSize))
                        painter.setBrush(QBrush(Qt.GlobalColor.black, Qt.BrushStyle.SolidPattern))
                    else:
                        painter.setPen(QPen(Qt.GlobalColor.white, self.brushSize))
                        painter.setBrush(QBrush(Qt.GlobalColor.white, Qt.BrushStyle.SolidPattern))
                    radius = int(25*self.image.width()/490)
                    painter.drawEllipse(int(newX) - int(radius/2**0.5), int(newY) - int(radius/2**0.5), radius*2, radius*2)
        self.update()
