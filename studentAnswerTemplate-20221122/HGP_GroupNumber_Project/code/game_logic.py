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
        self.currentPlayer = 1
        self.placeForPlayer = [[[True] * self.dimensionBoard] * self.dimensionBoard] * 2
        print(self.placeForPlayer)
        self.groups = [[], []]
        self.captured = [0, 0]
        self.previousBoards = []
        self.scores = [0, 0]

    def update(self, piece):

        # Create some variables to check the state of the board at every updates
        neighbour = 0
        left = False
        right = False
        top = False
        bottom = False
        boardOwners = [[0] * self.dimensionBoard] * self.dimensionBoard
        suicideRule = []

        self.boardState[piece.x][
            piece.y].owner = self.currentPlayer  # Change the owner of the piece (add the new piece to the board)

        # Save the owners for the koRule
        for i in self.boardState:
            for j in i:
                boardOwners[j.x][j.y] = j.owner

        self.previousBoards.append(boardOwners)

        # Test if this new piece is near an existing piece (group)
        if piece.x != 0:
            if self.boardState[piece.x - 1][piece.y].owner == self.currentPlayer:
                neighbour = neighbour + 1
                left = True
        if piece.x != self.dimensionBoard - 1:
            if self.boardState[piece.x + 1][piece.y].owner == self.currentPlayer:
                neighbour = neighbour + 1
                right = True
        if piece.y != 0:
            if self.boardState[piece.x][piece.y - 1].owner == self.currentPlayer:
                neighbour = neighbour + 1
                top = True
        if piece.y != self.dimensionBoard - 1:
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
                    fusions.pop(i)

        # If there is no groups near the new piece, create a new piece group
        else:
            self.groups[self.currentPlayer - 1].append(PieceGroup(self.boardState[piece.x][piece.y]))

        # Reset the liberties of each piece groups for each player
        for k in range(0, 2):
            for i in self.groups[k]:
                i.liberties = 0
                libertiescoord = []
                for j in i.pieces:
                    if j.x != 0:
                        if self.boardState[j.x - 1][j.y].owner == 0:
                            if [j.x - 1, j.y] in libertiescoord:
                                libertiescoord.append([j.x - 1, j.y])
                                i.liberties = i.liberties + 1
                    if j.x != self.dimensionBoard - 1:
                        if self.boardState[j.x + 1][j.y].owner == 0:
                            if [j.x + 1, j.y] in libertiescoord:
                                libertiescoord.append([j.x + 1, j.y])
                                i.liberties = i.liberties + 1
                    if j.y != 0:
                        if self.boardState[j.x][j.y - 1].owner == 0:
                            if [j.x, j.y - 1] in libertiescoord:
                                libertiescoord.append([j.x, j.y - 1])
                                i.liberties = i.liberties + 1
                    if j.y != self.dimensionBoard - 1:
                        if self.boardState[j.x][j.y + 1].owner == 0:
                            if [j.x, j.y + 1] in libertiescoord:
                                libertiescoord.append([j.x, j.y + 1])
                                i.liberties = i.liberties + 1

                # If liberties goes to 1, the player can't play to this last liberties if this place blocks all liberties (KO rule)
                if i.liberties == 1:
                    playable = False
                    toCheck = [self.boardState[libertiescoord[0][0]], self.boardState[libertiescoord[0][1]]]
                    if toCheck[0] != 0:
                        if self.boardState[toCheck[0] - 1][toCheck[1]].owner == 0:
                            playable = True
                    if toCheck[0] != self.dimensionBoard - 1:
                        if self.boardState[toCheck[0] + 1][toCheck[1]].owner == 0:
                            playable = True
                    if toCheck[1] != 0:
                        if self.boardState[toCheck[0]][toCheck[1] - 1].owner == 0:
                            playable = True
                    if toCheck[1] != self.dimensionBoard - 1:
                        if self.boardState[toCheck[0]][toCheck[1] + 1].owner == 0:
                            playable = True
                    if not playable:
                        suicideRule.append([k, toCheck[0]], toCheck[1])

                # If liberties goes to 0, the other player get the pieces and the group is deleted
                if i.liberties == 0:
                    self.captured[(k + 1) % 2] = self.captured[(k + 1) % 2] + len(i.pieces)
                    for j in i.pieces:
                        j.owner = 0
                    self.groups[k].remove(i)

        # Update the list of position where the players can play
        self.placeForPlayer = [[[True] * self.dimensionBoard] * self.dimensionBoard] * 2

        for i in self.boardState:
            for j in i:
                if j.owner != 0:
                    for k in range(0, 2):
                        self.placeForPlayer[k][j.x][j.y] = False

        for i in suicideRule:
            self.placeForPlayer[i[0]][i[1]][i[2]] = False

        # Test the futures enbale positions for koRule
        for k in range(0, 2):
            for i in range(0, self.dimensionBoard):
                for j in range(0, self.dimensionBoard):
                    if self.placeForPlayer[k][i][j]:
                        boardOwners[i][j] = k + 1
                        if boardOwners in self.previousBoards:
                            self.placeForPlayer[k][i][j] = False
                        boardOwners[i][j] = 0

        self.changePlayer()
    def changePlayer(self):  # Change the current player
        if self.currentPlayer == 1:
            self.currentPlayer = 2
        else:
            self.currentPlayer = 1

    def scoreCount(self): #AVANT D'APPELER CETTE FONCTION, FAIRE RETIRER DU PLATEAU LES PIECES DE TROP PAR LES JOUEURS !!!
        voidGroups = []
        for i in range(0, self.dimensionBoard):
            for j in range(0, self.dimensionBoard):
                neighbour = 0
                top = False
                left = False
                if self.boardState[i][j].owner == 0:
                    if i == 0 and j == 0:
                            voidGroups.append(PieceGroup(self.boardState[i][j]))
                    elif i == 0:
                        if self.boardState[i][j-1].owner != 0:
                            voidGroups.append(PieceGroup(self.boardState[i][j]))
                        else:
                            for k in voidGroups:
                                if k.pieces.count(self.boardState[i][j-1]) != 0:
                                    k.addPiece(self.boardState[i][j])
                    elif j == 0:
                        if self.boardState[i-1][j].owner != 0:
                            voidGroups.append(PieceGroup(self.boardState[i][j]))
                        else:
                            for k in voidGroups:
                                if k.pieces.count(self.boardState[i-1][j]) != 0:
                                    k.addPiece(self.boardState[i][j])
                    else:
                        if self.boardState[i-1][j].owner != 0:
                            neighbour = neighbour + 1
                            top = True
                        if self.boardState[i][j-1].owner != 0:
                            neighbour = neighbour + 1
                            left = True
                        if neighbour >= 1:
                            if top:
                                for k in voidGroups:
                                    if k.pieces.count(self.boardState[i-1][j]) != 0:
                                        k.addPiece(self.boardState[i][j])
                            else:
                                for k in voidGroups:
                                    if k.pieces.count(self.boardState[i][j-1]) != 0:
                                        k.addPiece(self.boardState[i][j])
                            if neighbour>1:
                                for k in voidGroups:
                                    if k.pieces.count(self.boardState[i-1][j]) != 0:
                                        for l in voidGroups:
                                            if l.pieces.count(self.boardState[i][j-1]) != 0:
                                                for m in l.pieces:
                                                    k.addPiece(m)
                                                voidGroups.remove(l)
                        else:
                            voidGroups.append(PieceGroup(self.boardState[i][j]))

        for i in voidGroups:
            for j in i.pieces:
                if j.x != 0:
                    if self.boardState[j.x-1][j.y].owner != 0:
                        i.owners[self.boardState[j.x-1][j.y].owner-1] = i.owners[self.boardState[j.x-1][j.y].owner-1] + 1
                if j.x != self.boardState - 1:
                    if self.boardState[j.x+1][j.y].owner != 0:
                        i.owners[self.boardState[j.x+1][j.y].owner-1] = i.owners[self.boardState[j.x+1][j.y].owner-1] + 1
                if j.y != 0:
                    if self.boardState[j.x][j.y-1].owner != 0:
                        i.owners[self.boardState[j.x][j.y-1].owner-1] = i.owners[self.boardState[j.x][j.y-1].owner-1] + 1
                if j.y != self.boardState - 1:
                    if self.boardState[j.x][j.y+1].owner != 0:
                        i.owners[self.boardState[j.x][j.y+1].owner-1] = i.owners[self.boardState[j.x][j.y+1].owner-1] + 1

