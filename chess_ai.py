import chess

# once we analyze these many boards... dont go any deeper just finsh up
CAP = 1000

# board:
# BLACK
# 56 57 58 59 60 61 62 63
# 48 49 50 51 52 53 54 55
# 40 41 42 43 44 45 46 47
# 32 33 34 35 36 37 38 39
# 24 25 26 27 28 29 30 31
# 16 17 18 19 20 21 22 23
# 8  9  10 11 12 13 14 15
# 0  1  2  3  4  5  6  7
# WHITE

# notable squares for pieces --- each key represents a really good or really bad square -- mapped to its value
# knights/bishops/queens should be towards the center
# pawns should advance (center pawns should advance more)
# king should stay back early on
# king should stay middle later on
king_map = {}
queen_map = {}
rook_map = {}
knight_map = {}
bishop_map = {}
pawn_map = {}

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
   depth = 25 # depth first dive in to this many sub boards... actual # of boards analyzed will be tempered by CAP
   alpha = float("-inf")
   beta = float("inf")

   for move in board.legal_moves: # all possible moves for black... do the first layer here
       board.push(move)
       moveVal, positions_analyzed = minimax(board, depth -1 , alpha, beta, True, 0)
       if moveVal < bestVal:
           bestMove = move
           bestVal = moveVal
       board.pop()
   print("My best move: " + str(bestMove))
   print("I analyzed: " + str(positions_analyzed) + " boards.")
   print("The evaluation is now: " + str(bestVal))
   return bestMove

def minimax(board, depth, alpha, beta, maximizingPlayer, num_pos):
   
   # once we analyze 1000 boards... dont do any more recursion and just finish up
   if num_pos > CAP:
       num_pos = num_pos + 1
       return evaluate(board), num_pos

   if depth == 0 or board.is_game_over():
       num_pos = num_pos + 1
       return evaluate(board), num_pos
  
   if maximizingPlayer:
       maxEval = float("-inf")
       for move in list(board.legal_moves):
           board.push(move)
           eval, num_pos = minimax(board, depth -1, alpha, beta, False, num_pos)
           maxEval = max(eval, maxEval)
           alpha = max(alpha, maxEval)
           board.pop()
           if beta <= alpha:
               break
       return maxEval, num_pos
   else:
       minEval = float("inf")
       for move in list(board.legal_moves):
           board.push(move)
           eval, num_pos = minimax(board, depth -1, alpha, beta, True, num_pos)
           minEval = min(minEval, eval)
           beta = min(beta, minEval)
           board.pop()
           if beta <= alpha:
               break
       return minEval, num_pos

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
                white_score = white_score + staticValue(piece.symbol().lower())
                white_score = white_score + positionalEvaluation(piece.symbol().lower(), square)
            else:
                black_score = black_score + staticValue(piece.symbol().lower())
                black_score = black_score + positionalEvaluation(piece.symbol().lower(), square)

    return white_score - black_score


# value of piece by type
def staticValue(piece):
    if piece == "q":
        return 900
    if piece == "n":
        return 300
    if piece == "b":
        return 300
    if piece == "r":
        return 500
    if piece == "p":
        return 100
    return 0

# value of piece by where it is on the board 
# if square isnt explicitely mapped... return 0 -- doesn't matter if its on that square
def positionalEvaluation(piece, square):
    try:
        if piece == "k":
            return king_map[square]
        if piece == "q":
            return queen_map[square]
        if piece == "r":
            return queen_map[square]
        if piece == "n":
            return knight_map[square]
        if piece == "b":
            return bishop_map[square]
        if piece == "p":
            return pawn_map[square]
    except Exception as e:
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
