
import chess
from evaluation2 import *
# Call the function to initialize tables and evaluate the board


# Initialize the chess board
board = chess.Board()
print("Initial board:")
print(board)
#print("Initial evaluation:", eval_board(board))
evaluate_board(board)
print("Initial evaluation:", evaluate_board(board))

# 1. e4
move = chess.Move.from_uci("e2e4")
#move = chess.Move.from_uci("b1c3")
if move in board.legal_moves:
    board.push(move)
else:
    print("Illegal move")

print("\nBoard after 1.e4:")
print(board)
#print("Evaluation after 1.e4:", eval_board(board))
print("Initial evaluation:", evaluate_board(board))
#evaluate_board(board)


# 1... e5
#move = chess.Move.from_uci("e7e5")
move = chess.Move.from_uci("g8f6")
if move in board.legal_moves:
    board.push(move)
else:
    print("Illegal move")

print("\nBoard after 1...e5:")
print(board)
#print("Evaluation after 1...e5:", eval_board(board))
print("Initial evaluation:", evaluate_board(board))

# 2. Nf3
move = chess.Move.from_uci("g1f3")
if move in board.legal_moves:
    board.push(move)
else:
    print("Illegal move")

print("\nBoard after 2.Nf3:")
print(board)
#print("Evaluation after 2.Nf3:", eval_board(board))
print("Initial evaluation:", evaluate_board(board))

# 2... Nc6
move = chess.Move.from_uci("b8c6")
if move in board.legal_moves:
    board.push(move)
else:
    print("Illegal move")

print("\nBoard after 2...Nc6:")
print(board)
#print("Evaluation after 2...Nc6:", eval_board(board))
print("Initial evaluation:", evaluate_board(board))

# 3. ba6
move = chess.Move.from_uci("f1a6")
if move in board.legal_moves:
    board.push(move)
else:
    print("Illegal move")

print("\nBoard after 3.Ba6 intentional blunder:")
print(board)
#print("Evaluation after 3.Bc4:", eval_board(board))
print("Initial evaluation:", evaluate_board(board))

# 3..... b7a6
move = chess.Move.from_uci("b7a6")
if move in board.legal_moves:
    board.push(move)
else:
    print("Illegal move")

print("\nBoard after 3.b7a6 :")
print(board)
#print("Evaluation after 3.Bc4:", eval_board(board))
print("Initial evaluation:", evaluate_board(board))


'''
# 4. Ba3
move = chess.Move.from_uci("f8a3")
if move in board.legal_moves:
    board.push(move)
else:
    print("Illegal move")

print("\nBoard after 3.Ba3 (Intentional blunder):")
print(board)
#print("Evaluation after 3.Ba3:", eval_board(board))
print("Initial evaluation:", evaluate_board(board))
'''

