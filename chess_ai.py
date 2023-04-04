import chess
# draw the board
def drawBoard(board):
   print(board)

# get player's move as an input
def getPlayerMove():
    move = input("Enter your move in UCI notation (e.g. e2e4): ")
    return chess.Move.from_uci(move)

# AI is playing black... will try to find the move that minimizes bestVal
def getAIMove(board):
   bestVal = 1000000
   bestMove = ""
   depth = 3
   alpha = -1000000000
   beta = 1000000000

   for move in board.legal_moves: # all possible moves for black
       board.push(move)
       moveVal, positions_analyzed = minimax(board, depth, alpha, beta, True, 0)
       if moveVal < bestVal:
           bestMove = move
           bestVal = moveVal
       board.pop()
   print("My best move: " + str(bestMove))
   print("I analyzed: " + str(positions_analyzed) + " boards.")
   print("The evaluation is now: " + str(bestVal))
   return bestMove

def minimax(board, depth, alpha, beta, maximizingPlayer, num_pos):
   
   if depth == 0 or board.is_game_over():
       num_pos = num_pos + 1
       return evaluate(board), num_pos
  
   if maximizingPlayer:
       maxEval = -1000000000
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
       minEval = 10000000000
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
       return 100000
   if board.result() == "0-1": # black wins
       return -100000
   if board.is_game_over(): # draw
       return 0
   
   for square in chess.SQUARES:
       piece = board.piece_at(square)
       if piece is not None:
           if piece.symbol() == "K":
               pass
           if piece.symbol() == "Q":
               white_score = white_score + 9
           if piece.symbol() == "N":
               white_score = white_score + 3
           if piece.symbol() == "B":
               white_score = white_score + 3
           if piece.symbol() == "R":
               white_score = white_score + 5
           if piece.symbol() == "P":
               white_score = white_score + 1
           if piece.symbol() == "k":
               pass
           if piece.symbol() == "q":
               black_score = black_score + 9
           if piece.symbol() == "n":
               black_score = black_score + 3
           if piece.symbol() == "b":
               black_score = black_score + 3
           if piece.symbol() == "r":
               black_score = black_score + 5
           if piece.symbol() == "p":
               black_score = black_score + 1

   return white_score - black_score

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
