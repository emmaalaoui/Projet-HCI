from pieceGroup import PieceGroup
class GameLogic:



    print("Game Logic Object Created")
    # TODO add code here to manage the logic of your game
    def __init__(self):
        super().__init__()
        self.boardState = [[0]*7]*7
        print(self.boardList)
        self.currentPlayer = 1
        self.placeForPlayer = [[[1]*7]*7]*2
        self.groups[[], []]

    def update(self, piece):
        neighbour = 0
        self.boardState[piece.x][piece.y] = piece
        self.placeForPlayer[self.currentPlayer][piece.x][piece.y] = 0

        if self.boardState[piece.x-1][piece.y].getOwner() == self.currentPlayer:
            neighbour = neighbour + 1

        if self.boardState[piece.x+1][piece.y].getOwner() == self.currentPlayer:
            neighbour = neighbour + 1

        if self.boardState[piece.x][piece.y-1].getOwner() == self.currentPlayer:
            neighbour = neighbour + 1

        if self.boardState[piece.x][piece.y+1].getOwner() == self.currentPlayer:
            neighbour = neighbour + 1

        if neighbour > 0:
            if neighbour > 1:
                for i in self.groups[self.currentPlayer - 1]:
                    if self.boardState[piece.x-1][piece.y] in i.getPieces() or self.boardState[piece.x+1][piece.y] in i.getPieces() or self.boardState[piece.x][piece.y-1] in i.getPieces() or self.boardState[piece.x][piece.y+1] in i.getPieces():
                        i.addPiece(piece)
        else:
            self.groups[self.currentPlayer].append(PieceGroup(piece))


        if self.currentPlayer == 1:
            self.currentPlayer = 2
        else:
            self.currentPlayer = 1

