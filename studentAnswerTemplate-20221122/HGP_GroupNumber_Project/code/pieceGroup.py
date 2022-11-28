class PieceGroup:
    print("A group of piece has been created")

    def __init__(self, originalPiece):
        super().__init__()
        self.pieces = [originalPiece]
        self.numberPiece = 1
        self.liberties = 4

    def getPieces(self):
        return self.pieces

    def addPiece(self, newPiece):
        self.pieces.append(newPiece)

    def setLiberties(self, board):
        self.liberties