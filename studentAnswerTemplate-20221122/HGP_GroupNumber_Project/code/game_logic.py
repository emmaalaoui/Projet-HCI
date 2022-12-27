from pieceGroup import PieceGroup
from piece import Piece


class GameLogic:
    # In this class there will be all the logic of the game, when a piece is placed, it calls the methods of this class that check if some pieces must be deleted...
    # The pieces are undeletable and uncreable, it is only their owner who will change: 0 for nothing, 1 for player 1 and 2 for player 2

    # TODO add code here to manage the logic of your game
    def __init__(self):
        super().__init__()
        self.dimensionBoard = 7  # The number of places on the board
        self.scores = [0, 0]  # The scores of each players

        # Creation of a list which will be the representation of the board
        self.boardState = []
        for i in range(0, self.dimensionBoard):  # First with some 0 to give the good size to the list
            array = [0] * self.dimensionBoard
            self.boardState.append(array)
        for i in range(0, self.dimensionBoard):  # Then fill the list with pieces which will firstly have 0 as owner
            for j in range(0, self.dimensionBoard):
                self.boardState[i][j] = Piece(i, j, 0)

        # Creation of a list which will be the representation of the places of the board where the players can play
        # In the beginning, the players can put a piece everywhere
        self.placeForPlayer = []
        for k in range(0, 2):
            array2 = []
            for i in range(0, self.dimensionBoard):
                array = [True] * self.dimensionBoard
                array2.append(array)
            self.placeForPlayer.append(array2)

        self.currentPlayer = 1  # This variable is 1 or two depending on the current player
        self.groups = [[], []]  # This is a list containing all groups of pieces of the both players
        self.captured = [0, 0]  # Number of pieces captured by the players
        self.previousBoards = []  # A list containing all the boards that have been diplayed during the game for the KO-Rule
        self.territories = [0, 0]  # Number of squares which are in the territories of the players

    def update(self, piece):

        # Create some variables to check the state of the board at every updates
        neighbour = 0
        left = False
        right = False
        top = False
        bottom = False
        suicideRule = []  # Variable containing the localisation of the square where a player can't play to respect the suicide rule
        boardOwners = []  # List containing the owners of all pieces to check the KO-Rule
        voidGroups = []  # List of non-piece groups (groups of pieces with 0 as owner)
        self.territories = [0, 0]  # Reset the variable to recalculate the territories at every updates
        notSuicide = []  # Variable containing the localisation of the square where a player can actualy play and respect the suicide rule because playing here will eat some enemies pieces
        deleted = False

        self.boardState[piece.x][piece.y].owner = self.currentPlayer  # Change the owner of the piece (add the new piece to the board)

        # Creation of the boardOwners list
        for i in range(0, self.dimensionBoard):  # Create the boardOwners list
            array = [0] * self.dimensionBoard
            boardOwners.append(array)
        for i in self.boardState:  # Filling of the boardOwners list with owners
            for j in i:
                boardOwners[j.x][j.y] = j.owner

        temporaryPreviousBoard = boardOwners  # Save the state of the board before all changes

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
            addAble = True
            for i in self.groups[self.currentPlayer - 1]:
                addList = False
                if piece.x != 0:
                    if self.boardState[piece.x - 1][piece.y] in i.pieces:
                        addList = True
                if piece.x != self.dimensionBoard - 1:
                    if self.boardState[piece.x + 1][piece.y] in i.pieces:
                        addList = True
                if piece.y != 0:
                    if self.boardState[piece.x][piece.y - 1] in i.pieces:
                        addList = True
                if piece.y != self.dimensionBoard - 1:
                    if self.boardState[piece.x][piece.y + 1] in i.pieces:
                        addList = True
                if addList and addAble:
                    addAble = False
                    i.addPiece(self.boardState[piece.x][piece.y])

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

                # Delete the double element (if a same group touch the new piece on multiple sides)
                fusions = set(fusions)
                fusions = list(fusions)

                for i in range(1, len(fusions)):
                    for j in fusions[i].pieces:
                        fusions[0].addPiece(j)
                    self.groups[self.currentPlayer - 1].remove(fusions[i])

        # If there is no groups near the new piece, create a new piece group
        else:
            self.groups[self.currentPlayer - 1].append(PieceGroup(self.boardState[piece.x][piece.y]))

        # Reset and recalculate the liberties of each piece groups for each player
        for k in range(0, 2):
            toDelete = []
            for i in self.groups[k]:
                i.liberties = 0
                libertiescoord = []
                for j in i.pieces:
                    if j.x != 0:
                        if self.boardState[j.x - 1][j.y].owner == 0:
                            if [j.x - 1, j.y] not in libertiescoord:
                                libertiescoord.append([j.x - 1, j.y])
                                i.liberties = i.liberties + 1
                    if j.x != self.dimensionBoard - 1:
                        if self.boardState[j.x + 1][j.y].owner == 0:
                            if [j.x + 1, j.y] not in libertiescoord:
                                libertiescoord.append([j.x + 1, j.y])
                                i.liberties = i.liberties + 1
                    if j.y != 0:
                        if self.boardState[j.x][j.y - 1].owner == 0:
                            if [j.x, j.y - 1] not in libertiescoord:
                                libertiescoord.append([j.x, j.y - 1])
                                i.liberties = i.liberties + 1
                    if j.y != self.dimensionBoard - 1:
                        if self.boardState[j.x][j.y + 1].owner == 0:
                            if [j.x, j.y + 1] not in libertiescoord:
                                libertiescoord.append([j.x, j.y + 1])
                                i.liberties = i.liberties + 1

                # If liberties goes to 1, the player can't play to this last liberties if this place blocks all liberties (suicide rule)
                # But it checks the suicide rule only for groups which already exists
                if i.liberties == 1:
                    playable = False
                    toCheck = [libertiescoord[0][0], libertiescoord[0][1]]
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
                        suicideRule.append([k, toCheck[0], toCheck[1]])
                # If liberties goes to 0, the other player get the pieces and the group is deleted
                if i.liberties == 0 and self.currentPlayer != k+1:
                    self.captured[(k + 1) % 2] = self.captured[(k + 1) % 2] + len(i.pieces)
                    for j in i.pieces:
                        j.owner = 0
                    toDelete.append(i)
            for i in toDelete:
                deleted = True
                self.groups[k].remove(i)

        # If a piece has been deleted, recalculate the liberties of groups
        if deleted:
            for k in range(0, 2):
                for i in self.groups[k]:
                    i.liberties = 0
                    libertiescoord = []
                    for j in i.pieces:
                        if j.x != 0:
                            if self.boardState[j.x - 1][j.y].owner == 0:
                                if [j.x - 1, j.y] not in libertiescoord:
                                    libertiescoord.append([j.x - 1, j.y])
                                    i.liberties = i.liberties + 1
                        if j.x != self.dimensionBoard - 1:
                            if self.boardState[j.x + 1][j.y].owner == 0:
                                if [j.x + 1, j.y] not in libertiescoord:
                                    libertiescoord.append([j.x + 1, j.y])
                                    i.liberties = i.liberties + 1
                        if j.y != 0:
                            if self.boardState[j.x][j.y - 1].owner == 0:
                                if [j.x, j.y - 1] not in libertiescoord:
                                    libertiescoord.append([j.x, j.y - 1])
                                    i.liberties = i.liberties + 1
                        if j.y != self.dimensionBoard - 1:
                            if self.boardState[j.x][j.y + 1].owner == 0:
                                if [j.x, j.y + 1] not in libertiescoord:
                                    libertiescoord.append([j.x, j.y + 1])
                                    i.liberties = i.liberties + 1

        # Update the list of position where the players can play
        # Reset the list which indicates the places where players can play
        self.placeForPlayer = []
        for k in range(0, 2):
            array2 = []
            for i in range(0, self.dimensionBoard):
                array = [True] * self.dimensionBoard
                array2.append(array)
            self.placeForPlayer.append(array2)

        # If a piece is on a square, nobody can play on this square anymore
        for i in self.boardState:
            for j in i:
                if j.owner != 0:
                    for k in range(0, 2):
                        self.placeForPlayer[k][j.x][j.y] = False

        # Disable positions for SuicidRule
        for i in suicideRule:
            if suicideRule.count([(i[0] + 1) % 2, i[1], i[2]]) == 0:  # Check if the place is a suicide place for both player because if it is, players can actualy play here because it eats enemy pieces
                self.placeForPlayer[i[0]][i[1]][i[2]] = False
            else:
                notSuicide.append([i[1], i[2]])

        # Check the suicide rule for new groups the players could create by adding a new piece on the board
        for k in range(0, 2):
            for i in range(0, self.dimensionBoard):
                for j in range(0, self.dimensionBoard):
                    if self.placeForPlayer[k][i][j]:
                        enemies = 0
                        if i != 0:
                            if self.boardState[i - 1][j].owner == (k + 1) % 2 + 1:
                                enemies = enemies + 1
                        else:
                            enemies = enemies + 1
                        if i != self.dimensionBoard - 1:
                            if self.boardState[i + 1][j].owner == (k + 1) % 2 + 1:
                                enemies = enemies + 1
                        else:
                            enemies = enemies + 1
                        if j != 0:
                            if self.boardState[i][j - 1].owner == (k + 1) % 2 + 1:
                                enemies = enemies + 1
                        else:
                            enemies = enemies + 1
                        if j != self.dimensionBoard - 1:
                            if self.boardState[i][j + 1].owner == (k + 1) % 2 + 1:
                                enemies = enemies + 1
                        else:
                            enemies = enemies + 1
                        if enemies == 4:
                            self.placeForPlayer[k][i][j] = False

        # Test the futures enbale positions for koRule
        for k in range(0, 2):
            for i in range(0, self.dimensionBoard):
                for j in range(0, self.dimensionBoard):
                    if self.placeForPlayer[k][i][j]:
                        boardOwners[i][j] = k + 1
                        if boardOwners in self.previousBoards:
                            self.placeForPlayer[k][i][j] = False
                        boardOwners[i][j] = 0
        self.previousBoards.append(temporaryPreviousBoard)

        # Check if a suicide is really a suicide or if it takes an enemy group and so it is not a suicide
        for k in range(0, 2):
            for i in range(0, self.dimensionBoard):
                for j in range(0, self.dimensionBoard):
                    if not self.placeForPlayer[k][i][j]:
                        if i != 0:
                            for l in self.groups[(k+1) % 2]:
                                if l.pieces.count(self.boardState[i - 1][j]) != 0:
                                    if l.liberties == 1:
                                        self.placeForPlayer[k][i][j] = True
                        if i != self.dimensionBoard - 1:
                            for l in self.groups[(k+1) % 2]:
                                if l.pieces.count(self.boardState[i + 1][j]) != 0:
                                    if l.liberties == 1:
                                        self.placeForPlayer[k][i][j] = True
                        if j != 0:
                            for l in self.groups[(k+1) % 2]:
                                if l.pieces.count(self.boardState[i][j - 1]) != 0:
                                    if l.liberties == 1:
                                        self.placeForPlayer[k][i][j] = True
                        if j != self.dimensionBoard - 1:
                            for l in self.groups[(k+1) % 2]:
                                if l.pieces.count(self.boardState[i][j + 1]) != 0:
                                    if l.liberties == 1:
                                        self.placeForPlayer[k][i][j] = True

        # Calculate the territories for each player
        # Create void groups which are groups of pieces with 0 as owner
        for i in range(0, self.dimensionBoard):
            for j in range(0, self.dimensionBoard):
                neighbour = 0
                top = False
                if self.boardState[i][j].owner == 0:
                    if i == 0 and j == 0:
                        voidGroups.append(PieceGroup(self.boardState[i][j]))
                    elif i == 0:
                        if self.boardState[i][j - 1].owner != 0:
                            voidGroups.append(PieceGroup(self.boardState[i][j]))
                        else:
                            for k in voidGroups:
                                if k.pieces.count(self.boardState[i][j - 1]) != 0:
                                    k.addPiece(self.boardState[i][j])
                    elif j == 0:
                        if self.boardState[i - 1][j].owner != 0:
                            voidGroups.append(PieceGroup(self.boardState[i][j]))
                        else:
                            for k in voidGroups:
                                if k.pieces.count(self.boardState[i - 1][j]) != 0:
                                    k.addPiece(self.boardState[i][j])
                    else:
                        if self.boardState[i - 1][j].owner == 0:
                            neighbour = neighbour + 1
                            top = True
                        if self.boardState[i][j - 1].owner == 0:
                            neighbour = neighbour + 1
                        if neighbour >= 1:
                            if top:
                                for k in voidGroups:
                                    if k.pieces.count(self.boardState[i - 1][j]) != 0:
                                        k.addPiece(self.boardState[i][j])
                            else:
                                for k in voidGroups:
                                    if k.pieces.count(self.boardState[i][j - 1]) != 0:
                                        k.addPiece(self.boardState[i][j])
                            if neighbour > 1:
                                for k in voidGroups:
                                    if k.pieces.count(self.boardState[i - 1][j]) != 0:
                                        for l in voidGroups:
                                            if l.pieces.count(self.boardState[i][j - 1]) != 0:
                                                if l != k:
                                                    for m in l.pieces:
                                                        k.addPiece(m)
                                                    voidGroups.remove(l)
                        else:
                            voidGroups.append(PieceGroup(self.boardState[i][j]))

        # Calculate the number of black and white neighbours
        for i in voidGroups:
            for j in i.pieces:
                if j.x != 0:
                    if self.boardState[j.x - 1][j.y].owner != 0:
                        i.owners[self.boardState[j.x - 1][j.y].owner - 1] = i.owners[self.boardState[j.x - 1][
                                                                                         j.y].owner - 1] + 1
                if j.x != self.dimensionBoard - 1:
                    if self.boardState[j.x + 1][j.y].owner != 0:
                        i.owners[self.boardState[j.x + 1][j.y].owner - 1] = i.owners[self.boardState[j.x + 1][
                                                                                         j.y].owner - 1] + 1
                if j.y != 0:
                    if self.boardState[j.x][j.y - 1].owner != 0:
                        i.owners[self.boardState[j.x][j.y - 1].owner - 1] = i.owners[self.boardState[j.x][
                                                                                         j.y - 1].owner - 1] + 1
                if j.y != self.dimensionBoard - 1:
                    if self.boardState[j.x][j.y + 1].owner != 0:
                        i.owners[self.boardState[j.x][j.y + 1].owner - 1] = i.owners[self.boardState[j.x][
                                                                                         j.y + 1].owner - 1] + 1

        # If there are only black neighbours add the number of pieces of this group to black territory and vice versa for white
        for i in voidGroups:
            if i.owners[1] == 0 and i.owners[0] != 0:
                self.territories[0] = self.territories[0] + len(i.pieces)
            elif i.owners[0] == 0 and i.owners[1] != 0:
                self.territories[1] = self.territories[1] + len(i.pieces)

        self.changePlayer()  # Finally change the player at the end of the update

    def changePlayer(self):  # Change the current player
        if self.currentPlayer == 1:
            self.currentPlayer = 2
        else:
            self.currentPlayer = 1

    def scoreCount(self):  # Calculate the scores at the end of the game
        # Firstly calculate a last time the territories of the players (like we did at every update)
        voidGroups = []
        for i in range(0, self.dimensionBoard):
            for j in range(0, self.dimensionBoard):
                neighbour = 0
                top = False
                if self.boardState[i][j].owner == 0:
                    if i == 0 and j == 0:
                        voidGroups.append(PieceGroup(self.boardState[i][j]))
                    elif i == 0:
                        if self.boardState[i][j - 1].owner != 0:
                            voidGroups.append(PieceGroup(self.boardState[i][j]))
                        else:
                            for k in voidGroups:
                                if k.pieces.count(self.boardState[i][j - 1]) != 0:
                                    k.addPiece(self.boardState[i][j])
                    elif j == 0:
                        if self.boardState[i - 1][j].owner != 0:
                            voidGroups.append(PieceGroup(self.boardState[i][j]))
                        else:
                            for k in voidGroups:
                                if k.pieces.count(self.boardState[i - 1][j]) != 0:
                                    k.addPiece(self.boardState[i][j])
                    else:
                        if self.boardState[i - 1][j].owner == 0:
                            neighbour = neighbour + 1
                            top = True
                        if self.boardState[i][j - 1].owner == 0:
                            neighbour = neighbour + 1
                        if neighbour >= 1:
                            if top:
                                for k in voidGroups:
                                    if k.pieces.count(self.boardState[i - 1][j]) != 0:
                                        k.addPiece(self.boardState[i][j])
                            else:
                                for k in voidGroups:
                                    if k.pieces.count(self.boardState[i][j - 1]) != 0:
                                        k.addPiece(self.boardState[i][j])
                            if neighbour > 1:
                                for k in voidGroups:
                                    if k.pieces.count(self.boardState[i - 1][j]) != 0:
                                        for l in voidGroups:
                                            if l.pieces.count(self.boardState[i][j - 1]) != 0:
                                                if l != k:
                                                    for m in l.pieces:
                                                        k.addPiece(m)
                                                    voidGroups.remove(l)
                        else:
                            voidGroups.append(PieceGroup(self.boardState[i][j]))

        for i in voidGroups:
            for j in i.pieces:
                if j.x != 0:
                    if self.boardState[j.x - 1][j.y].owner != 0:
                        i.owners[self.boardState[j.x - 1][j.y].owner - 1] = i.owners[self.boardState[j.x - 1][
                                                                                         j.y].owner - 1] + 1
                if j.x != self.dimensionBoard - 1:
                    if self.boardState[j.x + 1][j.y].owner != 0:
                        i.owners[self.boardState[j.x + 1][j.y].owner - 1] = i.owners[self.boardState[j.x + 1][
                                                                                         j.y].owner - 1] + 1
                if j.y != 0:
                    if self.boardState[j.x][j.y - 1].owner != 0:
                        i.owners[self.boardState[j.x][j.y - 1].owner - 1] = i.owners[self.boardState[j.x][
                                                                                         j.y - 1].owner - 1] + 1
                if j.y != self.dimensionBoard - 1:
                    if self.boardState[j.x][j.y + 1].owner != 0:
                        i.owners[self.boardState[j.x][j.y + 1].owner - 1] = i.owners[self.boardState[j.x][
                                                                                         j.y + 1].owner - 1] + 1

        # Add to the scores the territories
        for i in voidGroups:
            if i.owners[1] == 0 and i.owners[0] != 0:
                self.scores[0] = self.scores[0] + len(i.pieces)
            elif i.owners[0] == 0 and i.owners[1] != 0:
                self.scores[1] = self.scores[1] + len(i.pieces)

        # Each pieces on the board adds 1 to the score of the player
        for i in self.boardState:
            for j in i:
                if j.owner == 1:
                    self.scores[0] = self.scores[0] + 1
                elif j.owner == 2:
                    self.scores[1] = self.scores[1] + 1

        # Finally the captured pieces or pull out from the score
        self.scores[0] = self.scores[0] - self.captured[1]
        self.scores[1] = self.scores[1] - self.captured[0] + 7.5  # White have a komi (7.5 bonus points because blakc starts)
