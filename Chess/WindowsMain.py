import pygame as p

import DataBase
from tkinter import *
import ChessEngine

WIDTH = 1024
HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


'''
figures images
'''


def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", "bp", "wp", "reverse"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    whiteSide = True
    moveMade = False
    animate = False
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()

    buttons = []
    buttons.append(ChessEngine.Button(len(buttons), "back"))
    buttons.append(ChessEngine.Button(len(buttons), "reset"))
    buttons.append(ChessEngine.Button(len(buttons), "comment"))
    buttons.append(ChessEngine.Button(len(buttons), "show"))
    buttons.append(ChessEngine.Button(len(buttons), "reverse"))
    validMoves = gs.getValidMoves()
    print(gs.board)
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    gameOver = False
    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0] // SQ_SIZE
                row = (location[1]  // SQ_SIZE) if whiteSide else 7 - (location[1] // SQ_SIZE)
                print(row, col, location[1])
                if not gameOver:

                    if col <= DIMENSION:
                        if sqSelected == (row, col):
                            sqSelected = ()
                            playerClicks = []
                        else:
                            sqSelected = (row, col)
                            playerClicks.append(sqSelected)
                        if len(playerClicks) == 2:
                            move = ChessEngine.Move(playerClicks[0], playerClicks[1], gs.board)
                            print(move.getChessNotation())
                            for i in range(len(validMoves)):
                                if move == validMoves[i]:
                                    gs.makeMove(validMoves[i])
                                    moveMade = True
                                    animate = True
                                    sqSelected = ()
                                    playerClicks = []
                            if not moveMade:
                                playerClicks = [sqSelected]
                # if button was pushed:
                if col > DIMENSION and ((row < len(buttons) and whiteSide) or (7 - row < len(buttons) and not whiteSide)):
                    row = row if whiteSide else 7 - row
                    if row == 0:  # undo move
                        gs.undoMove()
                        moveMade = True
                        animate = False
                        gameOver = False
                    if row == 1:  # reset the board
                        gs = ChessEngine.GameState()
                        validMoves = gs.getValidMoves()
                        sqSelected = ()
                        playerClicks = []
                        moveMade = False
                        animate = False
                        gameOver = False
                    if row == 2:  # make comment

                        root = Tk()
                        txt = Text(width=50, height=10)
                        txt.pack()
                        txt.insert(1.0, DataBase.getComment(gs.getFen()))
                        frame = Frame()
                        frame.pack()
                        Button(frame, text="Comment",
                               command=lambda: DataBase.makeComment(txt.get(1.0, END), getChar(gs.getFen()))).pack(
                            side=LEFT)
                        root.mainloop()
                    if row == 3:  # show comment
                        showComment(DataBase.getComment(getChar(gs.getFen())))

                    if row == 4:
                        if col == 9: #reverse board
                            whiteSide = not whiteSide
                            drawGameState(screen, gs, validMoves, sqSelected, buttons, whiteSide)


        if moveMade:
            if animate: animateMove(screen, gs.board, gs.moveLog[-1], clock, whiteSide)
            validMoves = gs.getValidMoves()
            moveMade = False
            animate = False
        drawGameState(screen, gs, validMoves, sqSelected, buttons, whiteSide)

        if gs.checkMate:
            gameOver = True
            if gs.whiteToMove:
                drawText(screen, "black wins by checkmate")
            else:
                drawText(screen, "white wins by checkmate")
        if gs.staleMate:
            gameOver = True
            drawText(screen, "Stalemate")

        clock.tick(MAX_FPS)
        p.display.flip()


'''
highliting moves
'''


def highlightSquares(screen, gs, validMoves, sqSelected, whiteSide):
    if sqSelected != ():
        r, c = sqSelected if whiteSide else (7-sqSelected[0], sqSelected[1])

        if gs.board[sqSelected[0]][c][0] == ('w' if gs.whiteToMove else 'b'):
            s = p.Surface((SQ_SIZE, SQ_SIZE))
            s.set_alpha(100)  # transparency
            s.fill(p.Color('yellow'))
            screen.blit(s, (c * SQ_SIZE, r * SQ_SIZE))
            for move in validMoves:
                if move.startRow == sqSelected[0] and move.startCol == c:
                    screen.blit(s, (move.endCol * SQ_SIZE, (move.endRow if whiteSide else 7-move.endRow) * SQ_SIZE))


def drawGameState(screen, gs, validMoves, sqSelected, buttons, whiteSide):
    drawBoard(screen)
    highlightSquares(screen, gs, validMoves, sqSelected, whiteSide)
    drawPieces(screen, gs.board, whiteSide)
    drawButtons(screen, buttons)


def drawBoard(screen):
    global colors
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r + c) % 2]
            p.draw.rect(screen, color, p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))


'''
move animation
'''


def animateMove(screen, board, move, clock, whiteSide):
    global colors
    deltaRow = move.endRow - move.startRow if whiteSide else -(move.endRow - move.startRow)
    deltaCol = move.endCol - move.startCol
    framesPerSquare = 10
    frameCount = (abs(deltaCol) + abs(deltaRow)) * framesPerSquare
    for frame in range(frameCount + 1):
        r, c = ((move.startRow if whiteSide else 7-move.startRow) + deltaRow * (frame / frameCount), move.startCol + deltaCol * (frame / frameCount))
        drawBoard(screen)
        drawPieces(screen, board, whiteSide)
        color = colors[(move.startRow + move.startCol) % 2] if whiteSide else colors[((move.startRow + move.startCol)+1) % 2]
        endSquare = p.Rect(move.endCol * SQ_SIZE, (move.endRow if whiteSide else 7-move.endRow) * SQ_SIZE, SQ_SIZE, SQ_SIZE)
        p.draw.rect(screen, color, endSquare)
        if move.pieceCaptured != "--":
            screen.blit(IMAGES[move.pieceCaptured], endSquare)
        screen.blit(IMAGES[move.pieceMoved], p.Rect(c * SQ_SIZE, r * SQ_SIZE, SQ_SIZE, SQ_SIZE))
        p.display.flip()
        clock.tick(90)


def drawPieces(screen, board, whiteSide):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece != "--":
                screen.blit(IMAGES[piece], p.Rect(c * SQ_SIZE, (r if whiteSide else 7 - r) * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawButtons(screen, buttons):
    for button in buttons:
        if not button.name in ("reverse",):
            smallfont = p.font.SysFont('Corbel', 65)
            p.draw.rect(screen, p.Color("gray"),
                        p.Rect(9 * SQ_SIZE, button.row * SQ_SIZE, DIMENSION * SQ_SIZE, SQ_SIZE))
            for i in range(4):
                p.draw.rect(screen, (0, 0, 0),
                            (9 * SQ_SIZE - i, button.row * SQ_SIZE - i, DIMENSION * SQ_SIZE, SQ_SIZE), 1)
            screen.blit(smallfont.render(button.name, True, 'white'), (11 * SQ_SIZE, (button.row) * SQ_SIZE))
        else:
            p.draw.rect(screen, p.Color("gray"),
                        p.Rect(9 * SQ_SIZE, button.row * SQ_SIZE, SQ_SIZE, SQ_SIZE))
            for i in range(4):
                p.draw.rect(screen, (0, 0, 0),
                            (9 * SQ_SIZE - i, button.row * SQ_SIZE - i, SQ_SIZE, SQ_SIZE), 1)
            screen.blit(IMAGES[button.name], p.Rect(9 * SQ_SIZE, button.row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def drawText(screen, text):
    font = p.font.SysFont("Helvitca", 32, True, False)
    textObject = font.render(text, 0, p.Color("Black"))
    textLocation = p.Rect(0, 0, WIDTH // 2, HEIGHT).move(WIDTH // 4 - textObject.get_width() // 2,
                                                         HEIGHT // 2 - textObject.get_height() // 2)
    screen.blit(textObject, textLocation)


def showComment(txt):
    label = Label(None, text=txt, font=('Times', '18'))
    label.pack()
    label.mainloop()


def getChar(string):
    char = ''
    for i in string:
        char += i
    return char





main()
