from typing import Dict, List, Any
import chess
import time
import chess.polyglot
import os, random
from evaluation import mvv_lva, check_end_game, evaluate_board
# Global definition of debug_info
debug_info = {"nodes": 0, "white_time": 0, "black_time":0, "book_move": None}

MATE_SCORE = 1000000007
MATE_THRESHOLD = 999000000
class ZOBRIST:
    def __init__(self):
        self.zobrist_table = self.init_zobrist_table()

    def init_zobrist_table(self):
        zobrist = []
        for _ in range(64):  # For each square on the chessboard
            row = []
            for _ in range(12):  # For each piece type and color (6 pieces * 2 colors)
                row.append(random.randrange(2**64))
            zobrist.append(row)
        return zobrist

    def zobrist_hash(self, board):
        hash_val = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece:
                piece_index = piece.piece_type - 1 + (6 if piece.color == chess.BLACK else 0)
                hash_val ^= self.zobrist_table[square][piece_index]
        return hash_val
    
ai_instance = ZOBRIST()
memo = {}
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
    return sorted(board.legal_moves, key=lambda move: mvv_lva(board, move, end_game),
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

# def quiescence_search(board: chess.Board, alpha: float, beta: float):
#     stand_pat = evaluate_board(board)
#     if stand_pat >= beta:
#         return beta
#     if alpha < stand_pat:
#         alpha = stand_pat

#     for move in board.legal_moves:
#         if board.is_capture(move) or board.gives_check(move):  # Limit to captures and checks
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
        value = alpha_beta(ai_instance, depth-1, board, -float("inf"), float("inf"), not maximize)
        board.pop()
        
        if (maximize and value > best_move) or (not maximize and value < best_move):
            best_move = value
            best_move_found = move

    return best_move_found

def alpha_beta(ai_instance, depth: int, board: chess.Board, alpha: float, beta: float, is_maximising_player: bool) -> float:
    global debug_info
    debug_info['nodes'] += 1  # Increment node counter

    # Generate the Zobrist hash key for the current board state
    zobrist_key = ai_instance.zobrist_hash(board)

    # Memoization: Check if the current board state has been evaluated before
    if (zobrist_key, depth, is_maximising_player) in memo:
        return memo[(zobrist_key, depth, is_maximising_player)]

    if depth == 0 or board.is_game_over():
        eval_value = evaluate_board(board)
        memo[(zobrist_key, depth, is_maximising_player)] = eval_value
        return eval_value

    if board.is_checkmate():
        return -MATE_SCORE if is_maximising_player else MATE_SCORE

    optimal_value = -float('inf') if is_maximising_player else float('inf')
    for move in get_ordered_moves(board):
        board.push(move)
        current_value = alpha_beta(ai_instance, depth - 1, board, alpha, beta, not is_maximising_player)
        board.pop()

        if is_maximising_player:
            optimal_value = max(optimal_value, current_value)
            alpha = max(alpha, optimal_value)
        else:
            optimal_value = min(optimal_value, current_value)
            beta = min(beta, optimal_value)

        if beta <= alpha:
            break

    memo[(zobrist_key, depth, is_maximising_player)] = optimal_value
    return optimal_value

