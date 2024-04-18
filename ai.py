from typing import Dict, List, Any
import chess
import time
import chess.polyglot
import os
#from evaluation import move_value, check_end_game, evaluate_board
from evaluation2 import *
# Global definition of debug_info
debug_info = {"nodes": 0, "white_time": 0, "black_time":0, "book_move": None}


MATE_SCORE = 1000000000
MATE_THRESHOLD = 999000000

def next_move(depth: int, board: chess.Board, debug=True, book_path='Resources/gm2600.bin') -> chess.Move:
    """
    Determine the next best move, including using opening book moves if available.
    """
    debug_info.clear()
    debug_info["nodes"] = 0
    t0 = time.time()
    if debug:
        print("Book path exists:", os.path.exists(book_path))
    
    # Try to use a book move
    try:
        with chess.polyglot.open_reader(book_path) as reader:
            book_moves = reader.findall(board)
            if book_moves:
                book_move = max(book_moves, key=lambda entry: entry.weight).move
                
                debug_info["book_move"] = str(book_move)
                if debug:
                    print(f"Book move found: {book_move}")
                return book_move
    except Exception as e:
        if debug:
            print(f"Error reading the book: {str(e)}")
    
    # If no book move, use minimax
    if debug:
        print("No book move found, calculating via minimax...")
    move = minimax_root(depth, board)
    debug_info["time"] = time.time() - t0
    if debug:
        print(f"Search info: {debug_info}")
    return move

def get_ordered_moves(board: chess.Board) -> List[chess.Move]:
    """
    Get legal moves ordered by heuristic value to improve minimax efficiency.
    """
    end_game = check_end_game(board)
    return sorted(board.legal_moves, key=lambda move: move_value(board, move, end_game),
                  reverse=board.turn == chess.WHITE)

# def quiescence_search(board, alpha, beta):
#     stand_pat = evaluate_board(board)
#     if stand_pat >= beta:
#         return beta
#     if alpha < stand_pat:
#         alpha = stand_pat
    
#     for move in board.legal_moves:
#         if board.is_capture(move):
#             board.push(move)
#             score = -quiescence_search(board, -beta, -alpha)
#             board.pop()

#             if score >= beta:
#                 return beta
#             if score > alpha:
#                 alpha = score
#     return alpha

def minimax_root(depth: int, board: chess.Board) -> chess.Move:
    """
    Root of the minimax algorithm to explore move possibilities.
    """
    maximize = board.turn == chess.WHITE
    best_move = -float("inf") if maximize else float("inf")
    best_move_found = None

    for move in get_ordered_moves(board):
        board.push(move)
        value = alpha_beta(depth - 1, board, -float("inf"), float("inf"), not maximize)
        board.pop()
        
        if (maximize and value > best_move) or (not maximize and value < best_move):
            best_move = value
            best_move_found = move

    return best_move_found

def alpha_beta(depth: int, board: chess.Board, alpha: float, beta: float, is_maximising_player: bool) -> float:
    """
    The minimax algorithm with alpha-beta pruning.
    """
    global debug_info
    debug_info['nodes'] += 1  # Increment node counter
    if depth == 0:
        return evaluate_board(board)
    if board.is_checkmate():
        return -MATE_SCORE if is_maximising_player else MATE_SCORE
    elif board.is_game_over():
        return 0

    optimal_value = -float("inf") if is_maximising_player else float("inf")
    for move in get_ordered_moves(board):
        board.push(move)
        current_value = alpha_beta(depth - 1, board, alpha, beta, not is_maximising_player)
        board.pop()
        if is_maximising_player:
            optimal_value = max(optimal_value, current_value)
            alpha = max(alpha, optimal_value)
        else:
            optimal_value = min(optimal_value, current_value)
            beta = min(beta, optimal_value)
        if beta <= alpha:
            break
    return optimal_value
