import pygame as p
from Chess import ChessEngine
WIDTH = 1024
HEIGHT = 512
DIMENSION = 8
SQ_SIZE = HEIGHT//DIMENSION
MAX_FPS = 15
IMAGES = {}


def loadImages():
    pieces = ["bR", "bN", "bB", "bQ", "bK", "wR", "wN", "wB", "wQ", "wK", "bp", "wp"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))

def main():
    moveMade = False
    p.init()
    screen = p.display.set_mode((WIDTH, HEIGHT))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    gs = ChessEngine.GameState()


    buttons = []
    buttons.append(ChessEngine.Button(len(buttons), "back"))

    validMoves = gs.getValidMoves()
    print(gs.board)
    loadImages()
    running = True
    sqSelected = ()
    playerClicks = []
    while running:
        for e in p.event.get():
            if e.type==p.QUIT:
                running = False
            elif e.type ==p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                col = location[0]//SQ_SIZE
                row = location[1]//SQ_SIZE
                if col<=DIMENSION:
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
                                sqSelected = ()
                                playerClicks = []
                        if not moveMade:
                            playerClicks = [sqSelected]
                elif row<len(buttons):
                    moveMade = execute(row, gs)



        if moveMade:
            validMoves = gs.getValidMoves()
            moveMade = False
        drawGameState(screen, gs, buttons)
        clock.tick(MAX_FPS)
        p.display.flip()

def drawGameState(screen, gs, buttons):
    drawBoard(screen)
    drawPieces(screen, gs.board)
    drawButtons(screen, buttons)

def drawBoard(screen):
    colors = [p.Color("white"), p.Color("gray")]
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            color = colors[(r+c) % 2]
            p.draw.rect(screen, color, p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawPieces(screen, board):
    for r in range(DIMENSION):
        for c in range(DIMENSION):
            piece = board[r][c]
            if piece!="--":
                screen.blit(IMAGES[piece], p.Rect(c*SQ_SIZE, r*SQ_SIZE, SQ_SIZE, SQ_SIZE))

def drawButtons(screen, buttons):
    for button in buttons:
        smallfont = p.font.SysFont('Corbel', 65)
        p.draw.rect(screen, p.Color("gray"), p.Rect(9 * SQ_SIZE, button.row * SQ_SIZE, DIMENSION*SQ_SIZE, SQ_SIZE))
        screen.blit(smallfont.render(button.name , True , 'white'), (11*SQ_SIZE, (button.row)*SQ_SIZE))

def execute(row, gs):
    if row == 0:
        gs.undoMove()
        moveMade = True
    return moveMade

main()


















