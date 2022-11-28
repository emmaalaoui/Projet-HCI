from pieceGroup import PieceGroup
class GameLogic:



    print("Game Logic Object Created")
    # TODO add code here to manage the logic of your game
    def __init__(self):
        super().__init__()
        self.dimensionBoard = 7
        self.boardState = [[0]*self.dimensionBoard]*self.dimensionBoard
        print(self.boardList)
        self.currentPlayer = 1
        self.placeForPlayer = [[[1]*self.dimensionBoard]*self.dimensionBoard]*2
        self.groups[[], []]

    def update(self, piece):

        # Create some variables to check the state of the board at every updates
        neighbour = 0
        left = False
        right = False
        top = False
        bottom = False

        self.boardState[piece.x][piece.y] = piece  # add the new piece to the board

        # Test if this new piece is near an existing piece (group)
        if piece.x != 0:
            if self.boardState[piece.x-1][piece.y].getOwner() == self.currentPlayer:
                neighbour = neighbour + 1
                left = True
        if piece.x != self.dimensionBoard:
            if self.boardState[piece.x+1][piece.y].getOwner() == self.currentPlayer:
                neighbour = neighbour + 1
                right = True
        if piece.y != 0:
            if self.boardState[piece.x][piece.y-1].getOwner() == self.currentPlayer:
                neighbour = neighbour + 1
                top = True
        if piece.y != self.dimensionBoard:
            if self.boardState[piece.x][piece.y+1].getOwner() == self.currentPlayer:
                neighbour = neighbour + 1
                bottom = True

        # If the piece is near an existed group, add it to it
        if neighbour > 0:
            for i in self.groups[self.currentPlayer - 1]:
                if self.boardState[piece.x-1][piece.y] in i.getPieces() or self.boardState[piece.x+1][piece.y] in i.getPieces() or self.boardState[piece.x][piece.y-1] in i.getPieces() or self.boardState[piece.x][piece.y+1] in i.getPieces():
                    i.addPiece(piece)

            # Fusion 2 groups if a piece makes the link between them
            if neighbour > 1:
                fusions = []
                if top:
                    for i in self.groups[self.currentPlayer - 1]:
                        if self.boardState[piece.x][piece.y - 1] in i.getPieces():
                            fusions.append(i)
                if bottom:
                    for i in self.groups[self.currentPlayer - 1]:
                        if self.boardState[piece.x][piece.y + 1] in i.getPieces():
                            fusions.append(i)
                if left:
                    for i in self.groups[self.currentPlayer - 1]:
                        if self.boardState[piece.x - 1][piece.y] in i.getPieces():
                            fusions.append(i)
                if right:
                    for i in self.groups[self.currentPlayer - 1]:
                        if self.boardState[piece.x + 1][piece.y] in i.getPieces():
                            fusions.append(i)

                fusions = set(fusions)
                print(fusions)

                for i in range(1, len(fusions)):
                    for j in fusions[i].getPieces():
                        fusions[0].addPiece(j)
                    del fusions[i]

        # If there is no groups near the new piece, create a new piece
        else:
            self.groups[self.currentPlayer].append(PieceGroup(piece))

        # Change the current player
        if self.currentPlayer == 1:
            self.currentPlayer = 2
        else:
            self.currentPlayer = 1

