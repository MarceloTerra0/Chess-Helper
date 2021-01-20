#lowercase = black


import pygame
import chess
from stockfish import Stockfish

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

stockfish = Stockfish(os.path.join("stockfish", "stockfish_20090216_x64"), parameters={"Skill Level": 1})
#stockfish = Stockfish(parameters={"Skill Level": 1})
stockfish.set_fen_position(board.fen())
#print(stockfish.get_best_move())

def updateWindow():
    pygame.display.update()

def drawSquares(win, tiles):
    for tile in tiles:
        selected = False
        pygame.draw.rect(win,(151, 168, 118) if selected else (186, 189, 182) if tile[0] == "Black" else (238, 238, 236), 
        ((ord(tile[1][0])-97) * 100, (int(tile[1][1])-1) * 100, 100, 100) )

def drawPieces(win, board):
    tabuleiro = board.fen().split()[0].split('/')
    for rows,row in enumerate(tabuleiro):
        column = 0
        for piece in row:
            try:
                num = int(piece)
                column+=num
            except:
                
                if piece == 'r':
                    win.blit(br, (column *100, rows*100))
                if piece == 'n':
                    win.blit(bn, (column *100, rows*100))
                if piece == 'b':
                    win.blit(bb, (column *100, rows*100))
                if piece == 'q':
                    win.blit(bq, (column *100, rows*100))
                if piece == 'k':
                    win.blit(bk, (column *100, rows*100))
                if piece == 'p':
                    win.blit(bp, (column *100, rows*100))

                if piece == 'R':
                    win.blit(wr, (column *100, rows*100))
                if piece == 'N':
                    win.blit(wn, (column *100, rows*100))
                if piece == 'B':
                    win.blit(wb, (column *100, rows*100))
                if piece == 'Q':
                    win.blit(wq, (column *100, rows*100))
                if piece == 'K':
                    win.blit(wk, (column *100, rows*100))
                if piece == 'P':
                    win.blit(wp, (column *100, rows*100))

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

def showOpponentPawnDominance(win, board):
    tabuleiro = board.fen().split()[0].split('/')
    for rows,row in enumerate(tabuleiro):
        column = 0
        for piece in row:
            try:
                num = int(piece)
                column+=num
            except:
                if piece == 'p':
                    #fazer as checagens diagonais dos pawns pretos indo de cima para baixo (8 -> 1)
                    if rows + 1 < 8:
                        if column - 1>=0:
                            pygame.draw.rect(win, (255, 20, 20, 128), ((column - 1) * 100 + 40, (rows + 1) * 100 + 40, 20, 20))
                        if column + 1 < 8:
                            pygame.draw.rect(win, (255, 20, 20, 128), ((column + 1) * 100 + 40, (rows + 1) * 100 + 40, 20, 20))
                column +=1

def showOpponentPiecesDominance(win, board):
    showOpponentPawnDominance(win, board)

    b = []
    for item in board.__str__().split('\n'):
        string = ''
        for letter in item:
            if letter != ' ':
                    string+=letter
        b.append(string)

    #protegido/ameaçado
    for rows, row in enumerate(b):
        for column in range(8):
            
            if row[column] == 'r':   
                #esquerda
                contador = column
                while contador > 0:
                    if row[contador-1] == '.':
                        contador -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contador * 100 + 40, rows * 100 + 40, 20, 20))
                    else:
                        contador -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contador * 100 + 40, rows * 100 + 40, 20, 20))
                        break
                #direita
                contador = column
                while contador < 7:
                    if row[contador+1] == '.':
                        contador +=1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contador * 100 + 40, rows * 100 + 40, 20, 20))
                    else:
                        contador +=1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contador * 100 + 40, rows * 100 + 40, 20, 20))
                        break
                #em cima
                contador = rows
                while contador > 0:
                    if b[contador-1][column] == '.':
                        contador -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (column * 100 + 40, contador * 100 + 40, 20, 20))
                    else:
                        contador -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (column * 100 + 40, contador * 100 + 40, 20, 20))
                        break
                #em baixo
                contador = rows
                while contador < 7:
                    if b[contador+1][column] == '.':
                        contador += 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (column * 100 + 40, contador * 100 + 40, 20, 20))
                    else:
                        contador += 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (column * 100 + 40, contador * 100 + 40, 20, 20))
                        break
            
            if row[column] == 'n':
                #esquerda cima - cima
                if column >= 1 and rows >= 2:
                    pygame.draw.rect(win, (255, 20, 20, 128), ((column - 1) * 100 + 40, (rows - 2) * 100 + 40, 20, 20))
                #esquerda cima - baixo
                if column >= 2 and rows >= 1:
                    pygame.draw.rect(win, (255, 20, 20, 128), ((column - 2) * 100 + 40, (rows - 1) * 100 + 40, 20, 20))

                #esquerda cima - cima
                if column >= 1 and rows <= 5:
                    pygame.draw.rect(win, (255, 20, 20, 128), ((column - 1) * 100 + 40, (rows + 2) * 100 + 40, 20, 20))
                #esquerda cima - baixo
                if column >= 2 and rows <= 6:
                    pygame.draw.rect(win, (255, 20, 20, 128), ((column - 2) * 100 + 40, (rows + 1) * 100 + 40, 20, 20))

                #direita cima - cima
                if column <= 6 and rows >= 2:
                    pygame.draw.rect(win, (255, 20, 20, 128), ((column + 1) * 100 + 40, (rows - 2) * 100 + 40, 20, 20))
                #direita cima - baixo
                if column <= 5 and rows >= 1:
                    pygame.draw.rect(win, (255, 20, 20, 128), ((column + 2) * 100 + 40, (rows - 1) * 100 + 40, 20, 20))

                #direita baixo - cima
                if column <= 6 and rows <= 5:
                    pygame.draw.rect(win, (255, 20, 20, 128), ((column + 1) * 100 + 40, (rows + 2) * 100 + 40, 20, 20))
                #direita baixo - baixo
                if column <= 5 and rows <= 6:
                    pygame.draw.rect(win, (255, 20, 20, 128), ((column + 2) * 100 + 40, (rows + 1) * 100 + 40, 20, 20))
            
            if row[column] == 'b': 
                #NE
                contadorCol = column
                contadorRow = rows
                while contadorCol > 0 and contadorRow > 0:
                    if b[contadorRow-1][contadorCol-1] == '.':
                        contadorRow -= 1
                        contadorCol -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                    else:
                        contadorRow -= 1
                        contadorCol -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                        break
                
                #SW
                contadorCol = column
                contadorRow = rows
                while contadorCol > 0 and contadorRow < 7:
                    if b[contadorRow+1][contadorCol-1] == '.':
                        
                        contadorRow += 1
                        contadorCol -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                    else:
                        contadorRow += 1
                        contadorCol -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                        break
                
                #NW
                contadorCol = column
                contadorRow = rows
                while contadorCol < 7 and contadorRow > 0:
                    if b[contadorRow-1][contadorCol+1] == '.':
                        contadorRow -= 1
                        contadorCol += 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                    else:
                        contadorRow -= 1
                        contadorCol += 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                        break
                #SE
                contadorCol = column
                contadorRow = rows
                while contadorCol < 7 and contadorRow < 7:
                    if b[contadorRow+1][contadorCol+1] == '.':
                        contadorRow += 1
                        contadorCol += 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                    else:
                        contadorRow += 1
                        contadorCol += 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                        break
                 
            if row[column] == 'q':
                #NE
                contadorCol = column
                contadorRow = rows
                while contadorCol > 0 and contadorRow > 0:
                    if b[contadorRow-1][contadorCol-1] == '.':
                        contadorRow -= 1
                        contadorCol -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                    else:
                        contadorRow -= 1
                        contadorCol -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                        break
                
                #SW
                contadorCol = column
                contadorRow = rows
                while contadorCol > 0 and contadorRow < 7:
                    if b[contadorRow+1][contadorCol-1] == '.':
                        
                        contadorRow += 1
                        contadorCol -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                    else:
                        contadorRow += 1
                        contadorCol -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                        break
                
                #NW
                contadorCol = column
                contadorRow = rows
                while contadorCol < 7 and contadorRow > 0:
                    if b[contadorRow-1][contadorCol+1] == '.':
                        contadorRow -= 1
                        contadorCol += 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                    else:
                        contadorRow -= 1
                        contadorCol += 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                        break
                #SE
                contadorCol = column
                contadorRow = rows
                while contadorCol < 7 and contadorRow < 7:
                    if b[contadorRow+1][contadorCol+1] == '.':
                        contadorRow += 1
                        contadorCol += 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                    else:
                        contadorRow += 1
                        contadorCol += 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contadorCol * 100 + 40, contadorRow * 100 + 40, 20, 20))
                        break

                #esquerda
                contador = column
                while contador > 0:
                    if row[contador-1] == '.':
                        contador -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contador * 100 + 40, rows * 100 + 40, 20, 20))
                    else:
                        contador -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contador * 100 + 40, rows * 100 + 40, 20, 20))
                        break
                #direita
                contador = column
                while contador < 7:
                    if row[contador+1] == '.':
                        contador +=1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contador * 100 + 40, rows * 100 + 40, 20, 20))
                    else:
                        contador +=1
                        pygame.draw.rect(win, (255, 20, 20, 128), (contador * 100 + 40, rows * 100 + 40, 20, 20))
                        break
                #em cima
                contador = rows
                while contador > 0:
                    if b[contador-1][column] == '.':
                        contador -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (column * 100 + 40, contador * 100 + 40, 20, 20))
                    else:
                        contador -= 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (column * 100 + 40, contador * 100 + 40, 20, 20))
                        break
                #em baixo
                contador = rows
                while contador < 7:
                    if b[contador+1][column] == '.':
                        contador += 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (column * 100 + 40, contador * 100 + 40, 20, 20))
                    else:
                        contador += 1
                        pygame.draw.rect(win, (255, 20, 20, 128), (column * 100 + 40, contador * 100 + 40, 20, 20))
                        break
            
            if row[column] == 'k':
                #N
                if rows > 0:
                    pygame.draw.rect(win, (255, 20, 20, 128), (column * 100 + 40, (rows - 1) * 100 + 40, 20, 20))
                #E
                if column < 7:
                    pygame.draw.rect(win, (255, 20, 20, 128), ((column + 1) * 100 + 40, rows * 100 + 40, 20, 20))
                #W
                if column > 0:
                    pygame.draw.rect(win, (255, 20, 20, 128), ((column - 1) * 100 + 40, rows * 100 + 40, 20, 20))
                #S
                if rows < 7:
                    pygame.draw.rect(win, (255, 20, 20, 128), (column * 100 + 40, (rows + 1) * 100 + 40, 20, 20))
                if rows > 0 and column > 0:
                    pygame.draw.rect(win, (255, 20, 20, 128), ((column - 1) * 100 + 40, (rows - 1) * 100 + 40, 20, 20))
                if rows > 0 and column < 7:
                    pygame.draw.rect(win, (255, 20, 20, 128), ((column - 1) * 100 + 40, (rows + 1) * 100 + 40, 20, 20))
                if rows < 7 and column > 0:
                    pygame.draw.rect(win, (255, 20, 20, 128), ((column + 1) * 100 + 40, (rows - 1) * 100 + 40, 20, 20))
                if rows < 7 and column < 7:
                    pygame.draw.rect(win, (255, 20, 20, 128), ((column + 1) * 100 + 40, (rows + 1) * 100 + 40, 20, 20))
            
def showOpponentDominance(win, board):
    showOpponentPiecesDominance(win, board)

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
    if board.fen().split()[1] == 'b':
        stockfish.set_fen_position(board.fen())
        print(stockfish.get_best_move())
        board.push(chess.Move.from_uci(stockfish.get_best_move()))
        #board.push(chess.Move.from_uci('0000'))
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