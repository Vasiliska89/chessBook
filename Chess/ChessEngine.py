class GameState():
    def __init__(self):
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bp", "bp", "bp", "bp", "bp", "bp", "bp", "bp"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wp", "wp", "wp", "wp", "wp", "wp", "wp", "wp"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]
        ]
        self.moveFunctions = {'R': (((1, 0), (0, 1), (-1, 0), (0, -1)), True), 'N': (((1, 2), (2, 1), (2, -1), (1, -2), (-1, -2), (-2, -1),(-2, 1), (-1, 2) ), False),
                              'B': (((1, 1), (-1, 1), (1, -1), (-1, -1)), True), 'Q': (((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)), True),
                              'K': (((1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)), False)}

        self.whiteToMove = True
        self.moveLog = []
        self.whiteKingLocation = (7, 4)
        self.blackKingLocation = (0, 4)
        self.checkMate = False
        self.staleMate = False
        self.enpassantPossible = ()
        self.currentCastlingRights = CastleRights(True, True, True, True)
        self.castleRightsLog = [CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)]
    def getFen(self):
        fen = ""
        for i in range(len(self.board)):
            for j in range(len(self.board[1])):
                fen+= self.board[i][j]
        fen+="w" if self.whiteToMove else "b"
        if self.currentCastlingRights.wks:
            fen+="wks"
        if self.currentCastlingRights.wqs:
            fen+="wqs"
        if self.currentCastlingRights.bks:
            fen+="bks"
        if self.currentCastlingRights.bqs:
            fen+="bqs"
        if len(self.enpassantPossible)==0:
            fen+="-"
        else:
            r, c = self.enpassantPossible
            fen+=str(r)+str(c)
        return fen
    def makeMove(self, move):
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)
        self.whiteToMove = not self.whiteToMove
        if move.pieceMoved == "wK":
            self.whiteKingLocation = (move.endRow, move.endCol)
        elif move.pieceMoved == "bK":
            self.blackKingLocation = (move.endRow, move.endCol)

        if move.isPawnPromotion:
            self.board[move.endRow][move.endCol] = move.pieceMoved[0]+'Q'

        if move.isEnpassantMove:
            self.board[move.startRow][move.endCol] = "--"
        if move.pieceMoved[1] == 'p' and abs(move.startRow-move.endRow)==2:
            self.enpassantPossible = ((move.startRow+move.endRow)//2 , move.startCol )
        else:
            self.enpassantPossible = ()
        #castle move
        if move.isCastleMove:
            if move.endCol-move.startCol==2: #kingside castle
                self.board[move.endRow][move.endCol-1] = self.board[move.endRow][7]
                self.board[move.endRow][7] = "--"
            else:
                self.board[move.endRow][move.endCol + 1] = self.board[move.endRow][0]
                self.board[move.endRow][0] = "--"



        #castling rights update:
        self.updateCastlingRights(move)
        self.castleRightsLog.append(CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                             self.currentCastlingRights.wqs, self.currentCastlingRights.bqs))


    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove
            if move.pieceMoved == "wK":
                self.whiteKingLocation = (move.startRow, move.startCol)
            elif move.pieceMoved == "bK":
                self.blackKingLocation = (move.startRow, move.startCol)

            #undo en passant:
            if move.isEnpassantMove:
                self.board[move.endRow][move.endCol] = "--"
                self.board[move.startRow][move.endCol] = move.pieceCaptured
                self.enpassantPossible = (move.endRow, move.endCol)

            #undo a 2square pawn advance:
            if move.pieceMoved[1] == 'p' and abs(move.endRow-move.startRow)==2:
                self.enpassantPossible = ()
            #undo castling rights
            self.castleRightsLog.pop()
            newRights = self.castleRightsLog[-1]
            self.currentCastlingRights = CastleRights(newRights.wks, newRights.bks,
                                                      newRights.wqs, newRights.bqs)
            #undo castling move
            if move.isCastleMove:
                if move.endCol-move.startCol==2:
                    self.board[move.endRow][7]= self.board[move.endRow][move.endCol-1]
                    self.board[move.endRow][move.endCol-1] = "--"
                else:
                    self.board[move.endRow][0]= self.board[move.endRow][move.endCol+1]
                    self.board[move.endRow][move.endCol+1] = "--"



    '''
    update castle rights
    '''

    def updateCastlingRights(self, move):
        if move.pieceMoved == "wK":
            self.currentCastlingRights.wks = False
            self.currentCastlingRights.wqs = False
        if move.pieceMoved == "bK":
            self.currentCastlingRights.bks = False
            self.currentCastlingRights.bqs = False
        if move.pieceMoved == "wR":
            if move.startRow == 7:
                if move.startCol == 0:
                    self.currentCastlingRights.wqs = False
                if move.startCol == 7:
                    self.currentCastlingRights.wks = False
        if move.pieceMoved == "bR":
            if move.startRow == 0:
                if move.startCol == 0:
                    self.currentCastlingRights.bqs = False
                if move.startCol == 7:
                    self.currentCastlingRights.bks = False
            

    def getValidMoves(self):
        tempEnpassantPossible = self.enpassantPossible
        tempCastleRights = CastleRights(self.currentCastlingRights.wks, self.currentCastlingRights.bks,
                                        self.currentCastlingRights.wqs, self.currentCastlingRights.bqs)
        moves = self.getAllPossibleMoves()
        if self.whiteToMove:
            self.getCastleMoves(self.whiteKingLocation[0], self.whiteKingLocation[1], moves, True)
        else:
            self.getCastleMoves(self.blackKingLocation[0], self.blackKingLocation[1], moves, False)
        for i in range(len(moves) - 1, -1, -1):
            self.makeMove(moves[i])
            self.whiteToMove = not self.whiteToMove
            if self.inCheck():
                moves.remove(moves[i])
            self.whiteToMove = not self.whiteToMove
            self.undoMove()
        if len(moves) == 0:
            if self.inCheck():
                self.checkMate = True
            else:
                self.staleMate = True
        else:
            self.checkMate = False
            self.staleMate = False
        self.enpassantPossible = tempEnpassantPossible
        self.currentCastlingRights = tempCastleRights
        return moves

    def inCheck(self):
        if self.whiteToMove:
            return self.squareUnderAttack(self.whiteKingLocation[0], self.whiteKingLocation[1])
        else:
            return self.squareUnderAttack(self.blackKingLocation[0], self.blackKingLocation[1])

    def squareUnderAttack(self, r, c):
        self.whiteToMove = not self.whiteToMove
        oppMoves = self.getAllPossibleMoves()
        self.whiteToMove = not self.whiteToMove
        for move in oppMoves:
            if move.endRow == r and move.endCol == c:
                return True
        return False

    def getAllPossibleMoves(self):
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]  # color
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    if piece == 'p':
                        self.getPawnMoves(r, c, moves)
                    else:
                        self.getPieceMoves(r, c, moves, self.moveFunctions[piece])
        return moves

    def getPawnMoves(self, r, c, moves):
        if self.whiteToMove:
            if self.board[r - 1][c] == "--":
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c >= 1:
                if self.board[r - 1][c - 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
                elif (r-1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c - 1), self.board, isEnpassantMove=True))
            if c <= 6:
                if self.board[r - 1][c + 1][0] == 'b':
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))
                elif (r-1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r - 1, c + 1), self.board, isEnpassantMove=True))
        else:
            if self.board[r + 1][c] == "--":
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c >= 1:
                if self.board[r + 1][c - 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
                elif (r+1, c-1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c - 1), self.board, isEnpassantMove=True))
            if c <= 6:
                if self.board[r + 1][c + 1][0] == 'w':
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))
                elif (r+1, c+1) == self.enpassantPossible:
                    moves.append(Move((r, c), (r + 1, c + 1), self.board, isEnpassantMove=True))

    def getPieceMoves(self, r, c, moves, piece):
        directions, longMover = piece
        allyColor = "w" if self.whiteToMove else "b"
        for direction in directions:
            steps = 1
            pathIsFree = True

            while (pathIsFree):
                endRow = r + steps * direction[0]
                endCol = c + steps * direction[1]
                if 0 <= endRow < 8 and 0 <= endCol < 8:
                    endPiece = self.board[endRow][endCol]
                    if endPiece[0] != allyColor:
                        moves.append(Move((r, c), (endRow, endCol), self.board))
                    else:
                        pathIsFree = False
                    if endPiece[0] !='-':
                        pathIsFree = False
                else:
                    pathIsFree = False
                steps+=1
                pathIsFree = pathIsFree and longMover

    '''
    generate all valid castling moves for the king
    '''
    def getCastleMoves(self, r, c, moves, allyColor):
        if self.squareUnderAttack(r, c): return
        if (self.whiteToMove and self.currentCastlingRights.wks) or ((not self.whiteToMove) and self.currentCastlingRights.bks):
            self.getKingSideCastleMoves(r, c, moves, allyColor)
        if (self.whiteToMove and self.currentCastlingRights.wqs) or ((not self.whiteToMove) and self.currentCastlingRights.bqs):
            self.getQueenSideCastleMoves(r, c, moves, allyColor)


    def getKingSideCastleMoves(self, r, c, moves, allycolor):
        if self.board[r][c+1]=="--" and self.board[r][c+2]=="--":
            if (not self.squareUnderAttack(r, c+1)) and (not self.squareUnderAttack(r, c+2)):
                moves.append(Move((r, c), (r, c+2), self.board, isCastleMove=True))


    def getQueenSideCastleMoves(self, r, c, moves, allycolor):
        if self.board[r][c-1]=="--" and self.board[r][c-2]=="--" and self.board[r][c-3]=="--":
            if (not self.squareUnderAttack(r, c-1)) and (not self.squareUnderAttack(r, c-2)):
                moves.append(Move((r, c), (r, c-2), self.board, isCastleMove=True))

class CastleRights():
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks #wks - white king side, boolean
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move():
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board, isEnpassantMove = False, isCastleMove = False):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.isPawnPromotion = False
        if self.pieceMoved == "wp" and self.endRow == 0:
            self.isPawnPromotion = True
        if self.pieceMoved == "bp" and self.endRow == 7:
            self.isPawnPromotion = True

        self.isEnpassantMove = isEnpassantMove
        if self.isEnpassantMove:
            self.pieceCaptured = "wp" if self.pieceMoved=="bp" else "bp"

        #castle move
        self.isCastleMove = isCastleMove


        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]


class Button():
    def __init__(self, row, name):
        self.row = row
        self.name = name
