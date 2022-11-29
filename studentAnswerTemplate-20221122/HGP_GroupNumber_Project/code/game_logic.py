from pieceGroup import PieceGroup
from piece import Piece


class GameLogic:

    # The pieces are undeletable and uncreable, it is only their owner who will change :
    # 0 for nothing, 1 for player 1 and 2 for player 2

    print("Game Logic Object Created")

    # TODO add code here to manage the logic of your game
    def __init__(self):
        super().__init__()
        self.dimensionBoard = 7
        self.boardState = [[0] * self.dimensionBoard] * self.dimensionBoard
        for i in range(0, self.dimensionBoard):
            for j in range(0, self.dimensionBoard):
                self.boardState[i][j] = Piece(i, j, 0)
        print(self.boardList)
        self.currentPlayer = 1
        self.placeForPlayer = [[[1] * self.dimensionBoard] * self.dimensionBoard] * 2
        self.groups = [[], []]
        self.captured = [0, 0]

    def update(self, piece):

        # Create some variables to check the state of the board at every updates
        neighbour = 0
        left = False
        right = False
        top = False
        bottom = False

        self.boardState[piece.x][
            piece.y].owner = self.currentPlayer  # Change the owner of the piece (add the new piece to the board)

        # Test if this new piece is near an existing piece (group)
        if piece.x != 0:
            if self.boardState[piece.x - 1][piece.y].owner == self.currentPlayer:
                neighbour = neighbour + 1
                left = True
        if piece.x != self.dimensionBoard:
            if self.boardState[piece.x + 1][piece.y].owner == self.currentPlayer:
                neighbour = neighbour + 1
                right = True
        if piece.y != 0:
            if self.boardState[piece.x][piece.y - 1].owner == self.currentPlayer:
                neighbour = neighbour + 1
                top = True
        if piece.y != self.dimensionBoard:
            if self.boardState[piece.x][piece.y + 1].owner == self.currentPlayer:
                neighbour = neighbour + 1
                bottom = True

        # If the piece is near an existed group, add it to it
        if neighbour > 0:
            for i in self.groups[self.currentPlayer - 1]:
                if self.boardState[piece.x - 1][piece.y] in i.pieces or self.boardState[piece.x + 1][
                    piece.y] in i.pieces or self.boardState[piece.x][piece.y - 1] in i.pieces or \
                        self.boardState[piece.x][piece.y + 1] in i.pieces:
                    i.addPiece(piece)

            # Fusion 2 groups if a piece makes the link between them
            if neighbour > 1:
                fusions = []
                if top:
                    for i in self.groups[self.currentPlayer - 1]:
                        if self.boardState[piece.x][piece.y - 1] in i.pieces:
                            fusions.append(i)
                if bottom:
                    for i in self.groups[self.currentPlayer - 1]:
                        if self.boardState[piece.x][piece.y + 1] in i.pieces:
                            fusions.append(i)
                if left:
                    for i in self.groups[self.currentPlayer - 1]:
                        if self.boardState[piece.x - 1][piece.y] in i.pieces:
                            fusions.append(i)
                if right:
                    for i in self.groups[self.currentPlayer - 1]:
                        if self.boardState[piece.x + 1][piece.y] in i.pieces:
                            fusions.append(i)

                fusions = set(fusions)
                print(fusions)

                for i in range(1, len(fusions)):
                    for j in fusions[i].pieces:
                        fusions[0].addPiece(j)
                    del fusions[i]

        # If there is no groups near the new piece, create a new piece group
        else:
            self.groups[self.currentPlayer - 1].append(PieceGroup(piece))

        # Reset the liberties of each piece groups for each player
        for k in range(0, 1):
            for i in self.groups[k]:
                i.liberties = 0
                libertiescoord = []
                for j in i.pieces:
                    if j.x != 0:
                        if self.boardState[j.x - 1][j.y].owner == 0:
                            if [j.x - 1, j.y] in libertiescoord:
                                libertiescoord.append([j.x - 1, j.y])
                                i.liberties = i.liberties + 1
                    if j.x != self.dimensionBoard:
                        if self.boardState[j.x + 1][j.y].owner == 0:
                            if [j.x + 1, j.y] in libertiescoord:
                                libertiescoord.append([j.x + 1, j.y])
                                i.liberties = i.liberties + 1
                    if j.y != 0:
                        if self.boardState[j.x][j.y - 1].owner == 0:
                            if [j.x, j.y - 1] in libertiescoord:
                                libertiescoord.append([j.x, j.y - 1])
                                i.liberties = i.liberties + 1
                    if j.y != self.dimensionBoard:
                        if self.boardState[j.x][j.y + 1].owner == 0:
                            if [j.x, j.y + 1] in libertiescoord:
                                libertiescoord.append([j.x, j.y + 1])
                                i.liberties = i.liberties + 1

                # If liberties go to 0, the other player get the pieces and the group is deleted
                if i.liberties == 0:
                    self.captured[(k + 1) % 2] = self.captured[(k + 1) % 2] + len(i.pieces)
                    for j in i.pieces:
                        j.owner = 0
                    del i

        # Change the current player
        if self.currentPlayer == 1:
            self.currentPlayer = 2
        else:
            self.currentPlayer = 1

