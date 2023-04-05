import chess

# once we analyze these many boards... dont go any deeper just finsh up
CAP = 1000
# board:
# BLACK
# 56 57 58 59 60 61 62 63   # H
# 48 49 50 51 52 53 54 55   # G
# 40 41 42 43 44 45 46 47   # F
# 32 33 34 35 36 37 38 39   # E
# 24 25 26 27 28 29 30 31   # D 
# 16 17 18 19 20 21 22 23   # C
# 8  9  10 11 12 13 14 15   # B
# 0  1  2  3  4  5  6  7    # A

# 1  2  3  4  5  6  7  8
# WHITE

# Scoring:
# -10 = disadvantage
# -5 = slight disadvantage
# 0 = neutral
# 5 = slight advantage
# 10 = advantage

# king stays near edge of board
king_table = [[10,10,10,-5,-5,-5,10,10],
              [-5,-5,-5,-5,-5,-5,-5,-5],
              [-5,-5,-5,-5,-5,-5,-5,-5],
              [-5,-5,-5,-5,-5,-5,-5,-5],
              [-5,-5,-5,-5,-5,-5,-5,-5],
              [-5,-5,-5,-5,-5,-5,-5,-5],
              [-5,-5,-5,-5,-5,-5,-5,-5],
              [10,10,10,-5,-5,-5,10,10]]

# queen is good whereever... depends on tactics
# slightly discourage home squares 
queen_table = [[0 ,0 ,0 ,-5,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,-5,0 ,0 ,0 ,0 ]]

# rooks on the second or seventh rank are good 
rook_table = [[0 ,-5,0 ,0 ,0 ,0 ,-5,0 ],
              [10,10,10,10,10,10,10,10],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [10,10,10,10,10,10,10,10],
              [0 ,-5,0 ,0 ,0 ,0 ,-5,0 ]]

# knights better towards the center
# disadvantage towards the sides
knight_table = [[-10,-5 ,-10,-10,-10,-10,-5 ,-10],
              [-10,0  ,0  ,0  ,0  ,0  ,0  ,-10],
              [-10,5  ,10 ,10 ,10 ,10 ,5  ,-10],
              [-10,5  ,10 ,10 ,10 ,10 ,5  ,-10],
              [-10,5  ,10 ,10 ,10 ,10 ,5  ,-10],
              [-10,5  ,10 ,10 ,10 ,10 ,5  ,-10],
              [-10,5  ,0  ,0  ,0  ,0  ,5  ,-10],
              [-10,-5 ,-10,-10,-10,-10,-5 ,-10]]

# bishops better along longer diagonals
# disadvanatge towards the sides
bishop_table =[[-5 ,-5 ,-5 ,-5 ,-5 ,-5 ,-5 ,-5 ],
              [-5 ,5  ,0  ,5  ,5  ,0  ,5  ,-5 ],
              [-5 ,0  ,0  ,5  ,5  ,0  ,0  ,-5 ],
              [-5 ,5  ,5  ,0  ,0  ,5  ,5  ,-5 ],
              [-5 ,5  ,5  ,0  ,0  ,5  ,5  ,-5 ],
              [-5 ,0  ,0  ,5  ,5  ,0  ,0  ,-5 ],
              [-5 ,0  ,0  ,5  ,5  ,0  ,0  ,-5 ],
              [-5 ,-5 ,-5 ,-5 ,-5 ,-5 ,-5 ,-5 ]]

# pawns good towards the center 
pawn_table = [[0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,5 ,0 ,-5,-5,0 ,5 ,0 ],
              [0 ,0 ,0 ,5 ,5 ,0 ,0 ,0 ],
              [0 ,0 ,10,10,10,10,0 ,0 ],
              [0 ,0 ,10,10,10,10,0 ,0 ],
              [0 ,0 ,0 ,5 ,5 ,0 ,0 ,0 ],
              [0 ,5 ,0 ,-5,-5,0 ,5 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ]]

# draw the board
def drawBoard(board):
   print(board)

# get player's move as an input
def getPlayerMove():
    move = input("Enter your move in UCI notation (e.g. e2e4): ")
    return chess.Move.from_uci(move)

# AI is playing black... will try to find the move that minimizes bestVal
def getAIMove(board):
    bestVal = float("inf")
    bestMove = ""
    depth = 5 # depth first dive in to this many sub boards... actual # of boards analyzed will be tempered by CAP
    alpha = float("-inf")
    beta = float("inf")
    visited = 0
    bestVal, bestMove, visited = minimax(board, depth, alpha, beta, False, visited) # ai is black
    print("My best move: " + str(bestMove))
    print("I visited: " + str(visited) + " boards.")
    print("The evaluation is now: " + str(bestVal / 100))
    return bestMove

def minimax(board, depth, alpha, beta, maximizingPlayer, visited):
    # once we analyze CAP boards -- dont go any further in depth 
    #if num_pos > CAP:
    #   num_pos = num_pos + 1
    #   return evaluate(board), num_pos

    if depth == 0 or board.is_game_over():
        return evaluate(board), None, visited

    if maximizingPlayer:
        maxEval = float("-inf")
        bestMove = moves[0]
        moves = list(board.legal_moves)
        moves = orderMoves(moves, board) # sort moves to check better ones first 
        for move in moves:
            board.push(move)
            eval, mv, visited = minimax(board, depth -1, alpha, beta, False, visited)
            if eval > maxEval:
                bestMove = move
            maxEval = max(eval, maxEval)
            alpha = max(alpha, maxEval)
            board.pop()
            visited = visited + 1
            if beta <= alpha:
                break
        return maxEval, bestMove, visited
    else:
        minEval = float("inf")
        bestMove = moves[0]
        moves = list(board.legal_moves)
        moves = orderMoves(moves, board)
        for move in moves:
            board.push(move)
            eval, mv, visited = minimax(board, depth -1, alpha, beta, True, visited)
            if eval < minEval:
                bestMove = move
            minEval = min(minEval, eval)
            beta = min(beta, minEval)
            board.pop()
            visited = visited + 1
            if beta <= alpha:
                break
        return minEval, bestMove, visited


# sort the moves by value of captures...
# if square is defended -- assume we will lose our capturing piece
# if square is not defended -- value is value of captured piece
# non-capture moves have value of -1000
# observation while testing different values:
#   should always do non-captures last... since theres so many of them its far better to go through all captures first 
# reduces boards analyzed significantly!
def orderMoves(moves, board):
    ordered = []
    captures_first = []
    for move in moves:
        starting = str(move)[0:2]
        ending = str(move)[2:4]
        starting_piece = board.piece_at(chess.parse_square(starting))
        ending_piece = board.piece_at(chess.parse_square(ending))

        if ending_piece: # capture
            value = 0
            if board.is_attacked_by(not starting_piece.color, chess.parse_square(ending)): # opponent defends
                value = getValue(ending_piece.symbol()) - getValue(starting_piece.symbol()) # assume we lose our piece
            else:
                value = getValue(ending_piece.symbol()) # undefened... we win a piece
            captures_first.append({"move" : move, "value":value})
        else:
            captures_first.append({"move": move, "value" : -1000}) # do non capture moves last 
    captures_first = sorted(captures_first, key=lambda x: x["value"], reverse=True)
    for move in captures_first:
        ordered.append(move["move"])
    return ordered

# value of piece
def getValue(piece):
    piece = piece.lower()
    if piece == "k":
        return 0
    if piece == "q":
        return 900
    if piece == "r":
        return 500
    if piece == "n" or piece == "b":
        return 300
    return 100 # pawn

def evaluate(board):
    white_score = 0
    black_score = 0
    if board.result() == "1-0": # white wins
        return float("inf")
    if board.result() == "0-1": # black wins
        return float("-inf")
    if board.is_game_over(): # draw
        return 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece is not None:
            if piece.symbol() == piece.symbol().upper():
                white_score = white_score + getValue(piece.symbol().lower())
                white_score = white_score + positionalEvaluation(piece.symbol().lower(), square)
            else:
                black_score = black_score + getValue(piece.symbol().lower())
                black_score = black_score + positionalEvaluation(piece.symbol().lower(), square)

    return white_score - black_score

# value of piece by where it is on the board 
# if square isnt explicitely mapped... return 0 -- doesn't matter if its on that square
def positionalEvaluation(piece, square):
    try:
        if piece == "k":
            return king_table[7 - int(square/8)][square - 8 * int(square/8)]
        if piece == "q":
            return queen_table[7 - int(square/8)][square - 8 * int(square/8)]
        if piece == "r":
            return rook_table[7 - int(square/8)][square - 8 * int(square/8)]
        if piece == "n":
            return knight_table[7 - int(square/8)][square - 8 * int(square/8)]
        if piece == "b":
            return bishop_table[7 - int(square/8)][square - 8 * int(square/8)]
        if piece == "p":
            return pawn_table[7 - int(square/8)][square - 8 * int(square/8)]
    except Exception as e:
        return 0
    return 0

# value of piece by position

def play():
   board = chess.Board()
   playerTurn = True # player is white

   while not board.is_game_over():
       drawBoard(board)
       if playerTurn:
           move = getPlayerMove()
           playerTurn = False
       else:
           move = getAIMove(board)
           playerTurn = True


       if move in board.legal_moves:
           board.push(move)
       else:
           print("Illegal move. Please try again.")
           playerTurn = True

   # end condition
   drawBoard(board)
   result = board.result()
   if result == "1-0":
       print("White wins!")
   elif result == "0-1":
       print("Black wins!")
   else:
       print("Draw!")

if __name__ == "__main__":
   play()
