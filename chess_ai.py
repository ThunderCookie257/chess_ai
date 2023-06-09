import chess
import time
import json
# concepts implemented
# minimax
# alpha beta pruning
# capture move ordering
# transposition tables
# iterative deepening + principle variation move ordering
# grandmaster games opening book

# NEXT:
# endgame eval
# push pawns
# king towards center
# higher depth in endgame
# play as white or black

# number of positions to keep in memory before resetting
MAX_POS = 400000
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
# king_table[7 - int(square/8)][square - 8 * int(square/8)]
# Scoring:
# -10 = disadvantage
# -5 = slight disadvantage
# 0 = neutral
# 5 = slight advantage
# 10 = advantage
# 20 = should be played 
# king stays near edge of board
king_table = [[10 ,10 ,10 ,-5 ,-5 ,-5 ,30 ,10 ],
              [-15,-15,-15,-15,-15,-15,-15,-15],
              [-15,-15,-15,-15,-15,-15,-15,-15],
              [-15,-15,-15,-15,-15,-15,-15,-15],
              [-15,-15,-15,-15,-15,-15,-15,-15],
              [-15,-15,-15,-15,-15,-15,-15,-15],
              [-15,-15,-15,-15,-15,-15,-15,-15],
              [10 ,10 ,10 ,-5 ,-5 ,-5 ,30 ,10 ]]

endgame_king_table =    [[-10,-10,-10,-10,-10,-10,-10,-10],
                        [0  ,5  ,10 ,10 ,10 ,10 ,5  ,0  ],
                        [10 ,15 ,20 ,20 ,20 ,20 ,15 ,10 ],
                        [10 ,15 ,20 ,20 ,20 ,20 ,15 ,10 ],
                        [10 ,15 ,20 ,20 ,20 ,20 ,15 ,10 ],
                        [10 ,15 ,20 ,20 ,20 ,20 ,15 ,10 ],
                        [0  ,5  ,10 ,10 ,10 ,10 ,5  ,0  ],
                        [-10,-10,-10,-10,-10,-10,-10,-10]]


# queen is good whereever... depends on tactics 
queen_table = [[0 ,0 ,0 ,0,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
              [0 ,0 ,0 ,0,0 ,0 ,0 ,0 ]]

# rooks on the second or seventh rank are good 
white_rook_table = [[0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [10,20,20,30,30,20,20,10],
                    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [-5,-5,0 ,20,20,10,-5,-5]]

black_rook_table = [[-5,-5,0 ,20,20,10,-5,-5],
                    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [10,20,20,30,30,20,20,10],
                    [0 ,-5,0 ,0 ,0 ,0 ,-5,0 ]]

# knights better towards the center
# disadvantage towards the sides
knight_table = [[-10,-10,-10,-10,-10,-10,-10,-10],
              [-10,0  ,0  ,0  ,0  ,0  ,0  ,-10],
              [-10,5  ,20 ,10 ,10 ,20 ,5  ,-10],
              [-10,5  ,10 ,10 ,10 ,10 ,5  ,-10],
              [-10,5  ,10 ,10 ,10 ,10 ,5  ,-10],
              [-10,5  ,20 ,10 ,10 ,20 ,5  ,-10],
              [-10,5  ,0  ,0  ,0  ,0  ,5  ,-10],
              [-10,-10,-10,-10,-10,-10,-10,-10]]

# bishops better along longer diagonals
# disadvanatge towards the sides
bishop_table =[[-5 ,-5 ,-5 ,-5 ,-5 ,-5 ,-5 ,-5 ],
              [-5 ,10  ,0  ,10,10,0  ,10  ,-5 ],
              [-5 ,0  ,0  ,5  ,5  ,0  ,0  ,-5 ],
              [-5 ,5  ,20 ,0  ,0  ,20 ,5  ,-5 ],
              [-5 ,5  ,20 ,0  ,0  ,20 ,5  ,-5 ],
              [-5 ,0  ,0  ,5  ,5  ,0  ,0  ,-5 ],
              [-5 ,10  ,0  ,10,1 ,0  ,10  ,-5 ],
              [-5 ,-5 ,-5 ,-5 ,-5 ,-5 ,-5 ,-5 ]]

# pawns good towards the center 
white_pawn_table = [[0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [60,60,60,60,60,60,60,60],
                    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [0 ,0 ,20,0 ,0 ,20,0 ,0 ],
                    [0 ,0 ,10,30,30,10,0 ,0 ],
                    [0 ,0 ,0 ,5 ,5 ,0 ,0 ,0 ],
                    [0 ,5 ,0 ,-10,-10,0 ,5 ,0 ],
                    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ]]

black_pawn_table = [[0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [0 ,5 ,0 ,-10,-10,0 ,5 ,0 ],
                    [0 ,0 ,0 ,5 ,5 ,0 ,0 ,0 ],
                    [0 ,0 ,10,30,30,10,0 ,0 ],
                    [0 ,0 ,20,0 ,0 ,20,0 ,0 ],
                    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ],
                    [60,60,60,60,60,60,60,60],
                    [0 ,0 ,0 ,0 ,0 ,0 ,0 ,0 ]]

# draw the board
def drawBoard(board):
   print(board)

# get player's move as an input
def getPlayerMove():
    move = input("Enter your move in UCI notation (e.g. e2e4): ")
    try:
        return chess.Move.from_uci(move)
    except Exception as e:
        return None


def getLine(moves_list, prev_games):
    print("looking for existing line...")
    for game in prev_games:
        for i in range(len(moves_list)):
            if i >= len(game):
                break
            if moves_list[i] != game[i]: #lines dont match
                break
            if i == len(moves_list) -1:
                return game[i + 1]
    return None

# AI is playing black... will try to find the move that minimizes bestVal
def getAIMove(board, tpt, moves_list, prev_games):

    found_existing_line = getLine(moves_list, prev_games)
    if found_existing_line:
        print("...found this move from a line: " + str(found_existing_line))
        return found_existing_line
    print("...no existing line found in dataset")
    
    # this value needs to be passed down to the evaluation function
    # also used to set a higher depth when we're in an endgame 
    isEndgame = len(board.piece_map()) < 12 # we're in an endgame when most pieces are gone 

    bestVal = float("inf")
    bestMove = None
    alpha = float("-inf")
    beta = float("inf")
    visited = 0 # number of boards we visit
    tpt_uses = 0 # of times we used tpt table for an eval

    if len(tpt["moves"].keys()) > MAX_POS: # transposition table is too big -- reset it 
        tpt = {"moves": {}}

    curr_depth = 1
    max_depth = 5

    # higher depth during endgame 
    if isEndgame:
        max_depth = max_depth + 2
    
    curr_time = 0
    max_time = 10 # seconds
    while curr_time < max_time and curr_depth <= max_depth: # iterative deepening ... passing along the principle variation (best move)
        start = time.time()
        val, move, visited, tpt, tpt_uses = minimax(board, curr_depth, alpha, beta, False, visited, tpt, tpt_uses, bestMove, isEndgame) # ai is black
        end = time.time()
        print("Found: " + str(move) + " at depth: " + str(curr_depth) + " with eval: " + str(val/100))
        curr_time = curr_time + end - start
        curr_depth = curr_depth + 1
        # update best move at new depth:
        bestVal = val
        bestMove = move

    print("My best move: " + str(bestMove))
    print("I visited: " + str(visited) + " boards.")
    print("The evaluation is now: " + str(bestVal / 100))
    print("The transposition table has: " + str(len(tpt["moves"].keys())) + " positions.")
    print("The transposition table was used: " + str(tpt_uses) + " times.")
    print("I got to depth: " + str(curr_depth-1) + " in: " + str(curr_time) + " seconds!")
    return bestMove

def minimax(board, depth, alpha, beta, maximizingPlayer, visited, tpt, tpt_uses, bmove, isEndgame):

    if depth == 0 or board.is_game_over():
        eval = evaluate(board, isEndgame)
        return eval, None, visited, tpt, tpt_uses

    if maximizingPlayer:
        maxEval = float("-inf")
        moves = list(board.legal_moves)
        bestMove = moves[0]
        moves = orderMoves(moves, board) # sort moves to check better ones first 
        if bmove and bmove in list(board.legal_moves):
            moves.insert(0,bmove) # prinicpal variation -- best move from previous iteration gets evaluated first 
        for move in moves:
            board.push(move)

            str_board = str(board)
            if str_board in tpt["moves"].keys() and tpt["moves"][str_board][1] and tpt["moves"][str_board][2] >= depth:
                
                if tpt["moves"][str_board][0] > maxEval:
                    bestMove = move

                maxEval = max(tpt["moves"][str_board][0], maxEval)
                board.pop()
                tpt_uses = tpt_uses + 1
                visited = visited + 1
                continue

            eval, mv, visited, tpt, tpt_uses = minimax(board, depth -1, alpha, beta, False, visited, tpt, tpt_uses, bmove, isEndgame)

            if str_board not in tpt["moves"].keys():
                tpt["moves"][str_board] = [eval, maximizingPlayer, depth]
            elif tpt["moves"][str_board][2] < depth:
                tpt["moves"][str_board] = [eval, maximizingPlayer, depth]         
        

            if eval > maxEval:
                bestMove = move
            maxEval = max(eval, maxEval)
            alpha = max(alpha, maxEval)
            board.pop()
            visited = visited + 1
            if beta <= alpha:
                break
        return maxEval, bestMove, visited, tpt, tpt_uses
    else:
        minEval = float("inf")
        moves = list(board.legal_moves)
        bestMove = moves[0]
        moves = orderMoves(moves, board)
        if bmove and bmove in list(board.legal_moves):
            moves.insert(0,bmove) # prinicpal variation -- best move from previous iteration gets evaluated first 
        for move in moves:
            board.push(move)

            str_board = str(board)
            if str_board in tpt["moves"].keys() and not tpt["moves"][str_board][1] and tpt["moves"][str_board][2] >= depth:

                if tpt["moves"][str_board][0] < minEval:
                    bestMove = move
                
                minEval = min(tpt["moves"][str_board][0], minEval)
                board.pop()
                tpt_uses = tpt_uses + 1
                visited = visited + 1
                continue

            eval, mv, visited, tpt, tpt_uses = minimax(board, depth -1, alpha, beta, True, visited, tpt, tpt_uses, bmove, isEndgame)

            if str_board not in tpt["moves"].keys():
                tpt["moves"][str_board] = [eval, maximizingPlayer, depth]
            elif tpt["moves"][str_board][2] < depth:
                tpt["moves"][str_board] = [eval, maximizingPlayer, depth] 

            if eval < minEval:
                bestMove = move
            minEval = min(minEval, eval)
            beta = min(beta, minEval)
            board.pop()
            visited = visited + 1
            if beta <= alpha:
                break
        return minEval, bestMove, visited, tpt, tpt_uses

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
            captures_first.append({"move": move, "value" : -1000}) # do non capture moves 
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

def evaluate(board, isEndgame):
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
                white_score = white_score + positionalEvaluation(piece.symbol().lower(), square, True, isEndgame)
            else:
                black_score = black_score + getValue(piece.symbol().lower())
                black_score = black_score + positionalEvaluation(piece.symbol().lower(), square, False, isEndgame)

    return white_score - black_score + immediateCaptureScore(board)

# value of piece by where it is on the board 
# if square isnt explicitely mapped... return 0 -- doesn't matter if its on that square
def positionalEvaluation(piece, square, white, isEndgame):
    try:
        if piece == "k" and isEndgame:
            return endgame_king_table[7 - int(square/8)][square - 8 * int(square/8)]
        elif piece == "k" and not isEndgame:
            return king_table[7 - int(square/8)][square - 8 * int(square/8)]
        
        if piece == "q":
            return queen_table[7 - int(square/8)][square - 8 * int(square/8)]
        if piece == "r" and white:
            return white_rook_table[7 - int(square/8)][square - 8 * int(square/8)]
        if piece == "r" and not white:
            return black_rook_table[7 - int(square/8)][square - 8 * int(square/8)]
        if piece == "n":
            return knight_table[7 - int(square/8)][square - 8 * int(square/8)]
        if piece == "b":
            return bishop_table[7 - int(square/8)][square - 8 * int(square/8)]
        if piece == "p" and white:
            return white_pawn_table[7 - int(square/8)][square - 8 * int(square/8)]
        if piece == "p" and not white:
            return black_pawn_table[7 - int(square/8)][square - 8 * int(square/8)]
    except Exception as e:
        print(e)
        return 0
    return 0

# returns a score that reflects the value of immediate captures from the current position for UNDEFENDED PIECES
# need to only consider undefended pieces here as a safety mechanism to not hang anything 
# negative for black
def immediateCaptureScore(board):
    score = 0
    for move in board.legal_moves:
        starting = str(move)[0:2]
        ending = str(move)[2:4]
        starting_piece = board.piece_at(chess.parse_square(starting))
        ending_piece = board.piece_at(chess.parse_square(ending))
        if ending_piece: # capture
            value = 0
            # if board.is_attacked_by(not starting_piece.color, chess.parse_square(ending)): # opponent defends
            #     value = getValue(ending_piece.symbol()) - getValue(starting_piece.symbol()) # assume we lose our piece
            # else:
            value = getValue(ending_piece.symbol()) # undefened... we win a piece
            score = score + value
    
    if board.turn == chess.WHITE:
        return score
    return 0 - score


def getPrevGames():
    games = []
    with open("games.json", "r") as g:
        games_dict = json.load(g)
        games = games_dict["games"]

    return games

def play():
   board = chess.Board()
   playerTurn = True # player is white
   TPT = {"moves" : {}}

   prevGames = getPrevGames() # database of GM games
   moves_list = [] # moves played so far 

   while not board.is_game_over():
       drawBoard(board)
       if playerTurn:
           move = getPlayerMove()
           playerTurn = False
       else:
           move = getAIMove(board, TPT, moves_list, prevGames)
           playerTurn = True

       if type(move) == str:
           move = board.parse_san(move)
           move = move.uci()
           move = chess.Move.from_uci(move)

       if move in board.legal_moves:
            moves_list.append(str(board.san(move)))
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
