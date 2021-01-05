#lowercase = black
import pygame
import chess

import os

bb = pygame.transform.scale2x(pygame.image.load(os.path.join("images","bb.png")))
bk = pygame.transform.scale2x(pygame.image.load(os.path.join("images","bk.png")))
bn = pygame.transform.scale2x(pygame.image.load(os.path.join("images","bn.png")))
bp = pygame.transform.scale2x(pygame.image.load(os.path.join("images","bp.png")))
bq = pygame.transform.scale2x(pygame.image.load(os.path.join("images","bq.png")))
br = pygame.transform.scale2x(pygame.image.load(os.path.join("images","br.png")))

wb = pygame.transform.scale2x(pygame.image.load(os.path.join("images","wb.png")))
wk = pygame.transform.scale2x(pygame.image.load(os.path.join("images","wk.png")))
wn = pygame.transform.scale2x(pygame.image.load(os.path.join("images","wn.png")))
wp = pygame.transform.scale2x(pygame.image.load(os.path.join("images","wp.png")))
wq = pygame.transform.scale2x(pygame.image.load(os.path.join("images","wq.png")))
wr = pygame.transform.scale2x(pygame.image.load(os.path.join("images","wr.png")))

selected = pygame.image.load(os.path.join("images","selected.png"))

blackPiecesSprites = [bb, bk, bn, bp, bq, br]
whitePiecesSprites = [wb, wk, wn, wp, wq, wr]
WIN_WIDTH  = 800
WIN_HEIGHT = 800

win = pygame.display.set_mode((WIN_WIDTH,WIN_HEIGHT))
icon = pygame.image.load(os.path.join("images","icon.png"))
pygame.display.set_icon(icon)

board = chess.Board()
#board.push(chess.Move.null())
#move = chess.Move.from_uci("d2d4")
#board.push(move)

def updateWindow():
    pygame.display.update()

def drawSquares(win, tiles):
    for tile in tiles:
        selected = False
        pygame.draw.rect(win,(151, 168, 118) if selected else (186, 189, 182) if tile[0] == "Black" else (238, 238, 236), 
        ((ord(tile[1][0])-97) * 100, (int(tile[1][1])-1) * 100, 100, 100) )

def drawPieces(win, board):
    tabuleiro = board.fen().split()[0].split('/')
    for row,piece in enumerate(tabuleiro):
        column = 0
        for i in range(len(piece)):
            try:
                num = int(piece[i])
                column+=num
            except:
                
                if piece[i] == 'r':
                    win.blit(br, (column *100, row*100))
                if piece[i] == 'n':
                    win.blit(bn, (column *100, row*100))
                if piece[i] == 'b':
                    win.blit(bb, (column *100, row*100))
                if piece[i] == 'q':
                    win.blit(bq, (column *100, row*100))
                if piece[i] == 'k':
                    win.blit(bk, (column *100, row*100))
                if piece[i] == 'p':
                    win.blit(bp, (column *100, row*100))

                if piece[i] == 'R':
                    win.blit(wr, (column *100, row*100))
                if piece[i] == 'N':
                    win.blit(wn, (column *100, row*100))
                if piece[i] == 'B':
                    win.blit(wb, (column *100, row*100))
                if piece[i] == 'Q':
                    win.blit(wq, (column *100, row*100))
                if piece[i] == 'K':
                    win.blit(wk, (column *100, row*100))
                if piece[i] == 'P':
                    win.blit(wp, (column *100, row*100))

                column+=1

def showPossibleMovesForPosition(win, board, tile):
    #list(board.legal_moves)[0].uci()
    moves = list(board.legal_moves)
    movelist = []
    for move in moves:
        if move.uci()[:2] == tile:
            movelist.append(move.uci())
    for move in movelist:
        pygame.draw.rect(win,(10, 200, 200, 128),((ord(move[2])-97) * 100 + 40, abs( (int(move[3])-8)) * 100 + 40, 20, 20))
    return movelist

def showPossibleMoves(win, board):
    moves = list(board.legal_moves)
    movelist = []
    for move in moves:
        movelist.append(move.uci())
    for move in movelist:
        pygame.draw.rect(win,(10, 200, 200, 128),((ord(move[2])-97) * 100 + 40, abs( (int(move[3])-8)) * 100 + 40, 20, 20))
    return movelist

def showOpponentDominance(win, board):
    board.push(chess.Move.null())
    moves = list(board.legal_moves)
    board.pop()
    movelist = []
    for move in moves:
        #ignorando pawns, já que a área de dominancia deles não é a mesma que os possíveis movimentos
        square = move.uci()[:2]
        piece = board.piece_type_at(chess.parse_square(square))
        if piece != 1:
            movelist.append(move.uci())

    pontaEsquerda = True if square[0] == 'a' else False
    pontaDireita  = True if square[0] == 'h' else False
    baixo         = True if square[1] == '1' else False
    cima          = True if square[1] == '8' else False

    if board.fen().split()[1] == 'w':
        #fazer as checagens diagonais dos pawns pretos indo de cima para baixo (8 -> 1)
        tabuleiro = board.fen().split()[0].split('/')

        

    for move in movelist:
        pygame.draw.rect(win,(255, 20, 20, 128) if board.fen().split()[1] == 'w' else (20, 255, 20, 128),((ord(move[2])-97) * 100 + 40, abs( (int(move[3])-8)) * 100 + 40, 20, 20))
    
    return movelist

tiles = []
for rows in range(8):
    color = "White" if rows%2 == 0 else "Black"
    for line in range(1, 9):
        tiles.append((color, str(chr(96+line) + str(rows+1))))
        color = "White" if color == "Black" else "Black"


mouseSolto = True
pecaSelecionada = False
possiveisMovimentos = []
movimento = True
while True:

    drawSquares(win, tiles)
    drawPieces(win, board)
    #showPossibleMovesForPosition(win, board, 'e5')
    #showPossibleMoves(win, board)
    showOpponentDominance(win, board)
    #print(board.legal_moves)
    if pecaSelecionada:
        possiveisMovimentos = showPossibleMovesForPosition(win, board, currentCoord)
        if not possiveisMovimentos:
            pecaSelecionada = False

    updateWindow()

    if pygame.mouse.get_pressed()[0]:
        if pecaSelecionada and mouseSolto:
            coord1, coord2 = pygame.mouse.get_pos()
            currentCoord = (chr(coord1//100 + 97) + str(abs(coord2//100-8)))
            for coord in possiveisMovimentos:
                if currentCoord in coord[2:]:
                    movimento = True
                    move = chess.Move.from_uci(coord[:2] + currentCoord)
                    board.push(move)
            
            mouseSolto = False
            pecaSelecionada = False
        elif mouseSolto:
            coord1, coord2 = pygame.mouse.get_pos()
            currentCoord = (chr(coord1//100 + 97) + str(abs(coord2//100-8)))
            #print(currentCoord)
            mouseSolto = False
            pecaSelecionada = True
    
    if not pygame.mouse.get_pressed()[0]:
        mouseSolto = True

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()