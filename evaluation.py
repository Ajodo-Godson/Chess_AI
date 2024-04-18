import chess


piece_value = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

p_white = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5, -10,  0,  0, -10, -5,  5,
    5, 10, 10, -20, -20, 10, 10,  5,
    0, 0, 0, 0, 0, 0, 0, 0
]
p_Black = list(reversed(p_white))

knightEval = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]

b_white = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]
b_Black = list(reversed(b_white))

r_white = [
    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]
r_Black = list(reversed(r_white))

queenEval = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

mg_kingEvalWhite = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]
mg_kingEvalBlack = list(reversed(mg_kingEvalWhite))

eg_kingEvalWhite = [
    -50,-40,-30,-20,-20,-30,-40,-50,
    -30,-20,-10,  0,  0,-10,-20,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 30, 40, 40, 30,-10,-30,
    -30,-10, 20, 30, 30, 20,-10,-30,
    -30,-30,  0,  0,  0,  0,-30,-30,
    -50,-30,-30,-30,-30,-30,-30,-50
]
eg_kingEvalEndGameBlack = list(reversed(eg_kingEvalWhite))

def check_end_game(board: chess.Board) -> bool:
    """
    - Both sides have no queens or
    - Every side which has a queen has additionally no other pieces or one minorpiece maximum.
    """
    white_queens = 0
    black_queens = 0
    white_minors = 0
    black_minors = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            if piece.piece_type == chess.QUEEN:
                if piece.color == chess.WHITE:
                    white_queens += 1
                else:
                    black_queens += 1
            elif piece.piece_type in [chess.BISHOP, chess.KNIGHT]:
                if piece.color == chess.WHITE:
                    white_minors += 1
                else:
                    black_minors += 1

    # Check conditions for both sides
    white_condition = white_queens == 0 or (white_queens == 1 and white_minors <= 1)
    black_condition = black_queens == 0 or (black_queens == 1 and black_minors <= 1)

    return white_condition and black_condition

def evaluate_piece(piece: chess.Piece, square: chess.Square, end_game: bool) -> int:
    """
    Evaluate a piece on a given square using the provided evaluation tables,
    adjusting for the phase of the game (end_game flag indicates if it is the endgame).
    """
    piece_type = piece.piece_type
    color = piece.color

    # Start with the base value of the piece
    base_value = piece_value[piece_type]

    # Positional value adjustment based on piece type and square
    positional_value = 0
    if piece_type == chess.PAWN:
        positional_value = p_white[square] if color == chess.WHITE else p_Black[square]
    elif piece_type == chess.KNIGHT:
        positional_value = knightEval[square]
    elif piece_type == chess.BISHOP:
        positional_value = b_white[square] if color == chess.WHITE else b_Black[square]
    elif piece_type == chess.ROOK:
        positional_value = r_white[square] if color == chess.WHITE else r_Black[square]
    elif piece_type == chess.QUEEN:
        positional_value = queenEval[square]
    elif piece_type == chess.KING:
        if end_game:
            positional_value = eg_kingEvalWhite[square] if color == chess.WHITE else eg_kingEvalEndGameBlack[square]
        else:
            positional_value = mg_kingEvalWhite[square] if color == chess.WHITE else mg_kingEvalBlack[square]

    return base_value + positional_value

def evaluate_mobility(board: chess.Board, color: chess.Color) -> int:
    """
    Evaluate the mobility of the pieces for the given color.
    """
    legal_moves = list(board.legal_moves)
    mobility = sum(1 for move in legal_moves if board.color_at(move.from_square) == color)
    return mobility



def evaluate_capture(board: chess.Board, move: chess.Move) -> float:
    """
    Evaluates the net material gain or loss from a capture, considering the piece values.
    """
    if board.is_en_passant(move):
        return piece_value[chess.PAWN]  # Value of the pawn in an en passant capture

    captured_piece = board.piece_at(move.to_square)
    if captured_piece is None:
        return 0  # No capture, no material gain

    attacker_piece = board.piece_at(move.from_square)
    if attacker_piece is None:
        raise ValueError("Expected an attacker piece at the move's start square.")

    # Calculate basic material advantage
    material_gain = piece_value[captured_piece.piece_type] - piece_value[attacker_piece.piece_type]
    return material_gain

def evaluate_positional_change(board: chess.Board, move: chess.Move, endgame: bool) -> float:
    """
    Evaluates the positional value change due to a move.
    """
    board.push(move)  # Make the move on the board
    moved_piece = board.piece_at(move.to_square)
    if moved_piece is None:
        board.pop()
        raise ValueError("Expected a piece at the new position after the move.")

    # Positional value at the new location
    new_position_value = evaluate_piece(moved_piece, move.to_square, endgame)
    # Positional value at the original location
    old_position_value = evaluate_piece(moved_piece, move.from_square, endgame)

    board.pop()  # Undo the move to restore the board state
    return new_position_value - old_position_value
def move_value(board: chess.Board, move: chess.Move, endgame: bool) -> float:
    board.push(move)  # Make the move on the board
    board.pop()  # Undo the move

    if move.promotion:
        promotion_bonus = 900 - piece_value[chess.PAWN]  # Assume promoting to queen
    else:
        promotion_bonus = 0

    capture_value = 0
    if board.is_capture(move):
        capture_value = evaluate_capture(board, move)

    position_change = evaluate_positional_change(board, move, endgame)

    total_move_value = capture_value + position_change + promotion_bonus

    # Adjust the sign based on which color is making the move (negative for black)
    if board.turn == chess.BLACK:
        total_move_value = -total_move_value

    return total_move_value



def evaluate_board(board: chess.Board) -> float:
    total_evaluation = 0
    end_game = check_end_game(board)

    mobility_weight = 0.1 if not end_game else 0.15
    white_mobility = evaluate_mobility(board, chess.WHITE)
    black_mobility = evaluate_mobility(board, chess.BLACK)
    mobility_score = mobility_weight * (white_mobility - black_mobility)

    if board.turn == chess.WHITE:
        total_evaluation += mobility_score
    else:
        total_evaluation -= mobility_score

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if not piece:
            continue
        piece_value_adjusted = evaluate_piece(piece, square, end_game)
        total_evaluation += piece_value_adjusted if piece.color == chess.WHITE else -piece_value_adjusted

    return total_evaluation