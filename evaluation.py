import chess


piece_value = {
    chess.PAWN: 100,
    chess.KNIGHT: 320,
    chess.BISHOP: 330,
    chess.ROOK: 500,
    chess.QUEEN: 900,
    chess.KING: 20000
}

#-------------------------------------------------------------------------------------------------------------------#
#Middlegames Evaluation table
#-------------------------------------------------------------------------------------------------------------------#
# mg_whitepawn_table = [
#     0,   0,   0,   0,   0,   0,   0,   0,
#     178, 173, 158, 134, 147, 132, 165, 187,
#      94, 100,  85,  67,  56,  53,  82,  84,
#      32,  24,  13,   5,  -2,   4,  17,  17,
#      13,   9,  -3,  -7,  -7,  -8,   3,  -1,
#       4,   7,  -6,   1,   0,  -5,  -1,  -8,
#      13,   8,   8,  10,  13,   0,   2,  -7,
#       0,   0,   0,   0,   0,   0,   0,   0]
mg_whitepawn_table = [
    0,  0,  0,  0,  0,  0,  0,  0,
    50, 50, 50, 50, 50, 50, 50, 50,
    10, 10, 20, 30, 30, 20, 10, 10,
    5,  5, 10, 25, 25, 10,  5,  5,
    0,  0,  0, 20, 20,  0,  0,  0,
    5, -5, -10,  0,  0, -10, -5,  5,
    5, 10, 10, -20, -20, 10, 10,  5,
    0, 0, 0, 0, 0, 0, 0, 0
]

mg_blackpawn_table = list(reversed(mg_whitepawn_table))

# mg_whiteknight_table = [
#     -167, -89, -34, -49,  61, -97, -15, -107,
#      -73, -41,  72,  36,  23,  62,   7,  -17,
#      -47,  60,  37,  65,  84, 129,  73,   44,
#       -9,  17,  19,  53,  37,  69,  18,   22,
#      -13,   4,  16,  13,  28,  19,  21,   -8,
#      -23,  -9,  12,  10,  19,  17,  25,  -16,
#      -29, -53, -12,  -3,  -1,  18, -14,  -19,
#     -105, -21, -58, -33, -17, -28, -19,  -23
# ]
mg_whiteknight_table = [
    -50,-40,-30,-30,-30,-30,-40,-50,
    -40,-20,  0,  0,  0,  0,-20,-40,
    -30,  0, 10, 15, 15, 10,  0,-30,
    -30,  5, 15, 20, 20, 15,  5,-30,
    -30,  0, 15, 20, 20, 15,  0,-30,
    -30,  5, 10, 15, 15, 10,  5,-30,
    -40,-20,  0,  5,  5,  0,-20,-40,
    -50,-40,-30,-30,-30,-30,-40,-50,
]
mg_blackknight_table = list(reversed(mg_whiteknight_table))

# mg_whitebishop_table = [
#     -29,   4, -82, -37, -25, -42,   7,  -8,
#     -26,  16, -18, -13,  30,  59,  18, -47,
#     -16,  37,  43,  40,  35,  50,  37,  -2,
#      -4,   5,  19,  50,  37,  37,   7,  -2,
#      -6,  13,  13,  26,  34,  12,  10,   4,
#       0,  15,  15,  15,  14,  27,  18,  10,
#       4,  15,  16,   0,   7,  21,  33,   1,
#     -33,  -3, -14, -21, -13, -12, -39, -21,
# ]
mg_whitebishop_table = [
    -20,-10,-10,-10,-10,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5, 10, 10,  5,  0,-10,
    -10,  5,  5, 10, 10,  5,  5,-10,
    -10,  0, 10, 10, 10, 10,  0,-10,
    -10, 10, 10, 10, 10, 10, 10,-10,
    -10,  5,  0,  0,  0,  0,  5,-10,
    -20,-10,-10,-10,-10,-10,-10,-20,
]
mg_blackbishop_table = list(reversed(mg_whitebishop_table))

# mg_whiterook_table = [
#      32,  42,  32,  51, 63,  9,  31,  43,
#      27,  32,  58,  62, 80, 67,  26,  44,
#      -5,  19,  26,  36, 17, 45,  61,  16,
#     -24, -11,   7,  26, 24, 35,  -8, -20,
#     -36, -26, -12,  -1,  9, -7,   6, -23,
#     -45, -25, -16, -17,  3,  0,  -5, -33,
#     -44, -16, -20,  -9, -1, 11,  -6, -71,
#     -19, -13,   1,  17, 16,  7, -37, -26
#     ]
mg_whiterook_table = [

    0,  0,  0,  0,  0,  0,  0,  0,
    5, 10, 10, 10, 10, 10, 10,  5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    -5,  0,  0,  0,  0,  0,  0, -5,
    0,  0,  0,  5,  5,  0,  0,  0
]
mg_blackrook_table = list(reversed(mg_whiterook_table))

# mg_whitequeen_table = [
#     -28,   0,  29,  12,  59,  44,  43,  45,
#     -24, -39,  -5,   1, -16,  57,  28,  54,
#     -13, -17,   7,   8,  29,  56,  47,  57,
#     -27, -27, -16, -16,  -1,  17,  -2,   1,
#      -9, -26,  -9, -10,  -2,  -4,   3,  -3,
#     -14,   2, -11,  -2,  -5,   2,  14,   5,
#     -35,  -8,  11,   2,   8,  15,  -3,   1,
#      -1, -18,  -9,  10, -15, -25, -31, -50
# ]
mg_whitequeen_table = [
    -20,-10,-10, -5, -5,-10,-10,-20,
    -10,  0,  0,  0,  0,  0,  0,-10,
    -10,  0,  5,  5,  5,  5,  0,-10,
    -5,  0,  5,  5,  5,  5,  0, -5,
    0,  0,  5,  5,  5,  5,  0, -5,
    -10,  5,  5,  5,  5,  5,  0,-10,
    -10,  0,  5,  0,  0,  0,  0,-10,
    -20,-10,-10, -5, -5,-10,-10,-20
]

mg_blackqueen_table = list(reversed(mg_whitequeen_table))


# mg_whiteking_table = [
#     -65,  23,  16, -15, -56, -34,   2,  13,
#      29,  -1, -20,  -7,  -8,  -4, -38, -29,
#      -9,  24,   2, -16, -20,   6,  22, -22,
#     -17, -20, -12, -27, -30, -25, -14, -36,
#     -49,  -1, -27, -39, -46, -44, -33, -51,
#     -14, -14, -22, -46, -44, -30, -15, -27,
#       1,   7,  -8, -64, -43, -16,   9,   8,
#     -15,  36,  12, -54,   8, -28,  24,  14,
# ]
mg_whiteking_table = [
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -30,-40,-40,-50,-50,-40,-40,-30,
    -20,-30,-30,-40,-40,-30,-30,-20,
    -10,-20,-20,-20,-20,-20,-20,-10,
    20, 20,  0,  0,  0,  0, 20, 20,
    20, 30, 10,  0,  0, 10, 30, 20
]
mg_blackking_table = list(reversed(mg_whiteking_table))

#-------------------------------------------------------------------------------------------------------------------#
#Endgames Evaluation Table
#-------------------------------------------------------------------------------------------------------------------#
eg_whitepawn_table = [
      0,   0,   0,   0,   0,   0,   0,   0,
    178, 173, 158, 134, 147, 132, 165, 187,
     94, 100,  85,  67,  56,  53,  82,  84,
     32,  24,  13,   5,  -2,   4,  17,  17,
     13,   9,  -3,  -7,  -7,  -8,   3,  -1,
      4,   7,  -6,   1,   0,  -5,  -1,  -8,
     13,   8,   8,  10,  13,   0,   2,  -7,
      0,   0,   0,   0,   0,   0,   0,   0
]
eg_blackpawn_table = list(reversed(eg_whitepawn_table))

eg_whiteknight_table = [
    -58, -38, -13, -28, -31, -27, -63, -99,
    -25,  -8, -25,  -2,  -9, -25, -24, -52,
    -24, -20,  10,   9,  -1,  -9, -19, -41,
    -17,   3,  22,  22,  22,  11,   8, -18,
    -18,  -6,  16,  25,  16,  17,   4, -18,
    -23,  -3,  -1,  15,  10,  -3, -20, -22,
    -42, -20, -10,  -5,  -2, -20, -23, -44,
    -29, -51, -23, -15, -22, -18, -50, -64 
]
eg_blackknight_table = list(reversed(eg_whiteknight_table))

eg_whitebishop_table = [
    -14, -21, -11,  -8, -7,  -9, -17, -24,
     -8,  -4,   7, -12, -3, -13,  -4, -14,
      2,  -8,   0,  -1, -2,   6,   0,   4,
     -3,   9,  12,   9, 14,  10,   3,   2,
     -6,   3,  13,  19,  7,  10,  -3,  -9,
    -12,  -3,   8,  10, 13,   3,  -7, -15,
    -14, -18,  -7,  -1,  4,  -9, -15, -27,
    -23,  -9, -23,  -5, -9, -16,  -5, -17
]
eg_blackbishop_table = list(reversed(eg_whitebishop_table))

eg_whiterook_table = [
    13, 10, 18, 15, 12,  12,   8,   5,
    11, 13, 13, 11, -3,   3,   8,   3,
     7,  7,  7,  5,  4,  -3,  -5,  -3,
     4,  3, 13,  1,  2,   1,  -1,   2,
     3,  5,  8,  4, -5,  -6,  -8, -11,
    -4,  0, -5, -1, -7, -12,  -8, -16,
    -6, -6,  0,  2, -9,  -9, -11,  -3,
    -9,  2,  3, -1, -5, -13,   4, -20,
]
eg_blackrook_table = list(reversed(eg_whiterook_table))

eg_whitequeen_table = [
     -9,  22,  22,  27,  27,  19,  10,  20,
    -17,  20,  32,  41,  58,  25,  30,   0,
    -20,   6,   9,  49,  47,  35,  19,   9,
      3,  22,  24,  45,  57,  40,  57,  36,
    -18,  28,  19,  47,  31,  34,  39,  23,
    -16, -27,  15,   6,   9,  17,  10,   5,
    -22, -23, -30, -16, -16, -23, -36, -32,
    -33, -28, -22, -43,  -5, -32, -20, -41
]
eg_blackqueen_table = list(reversed(eg_whitequeen_table))


eg_whiteking_table = [
    -74, -35, -18, -18, -11,  15,   4, -17,
    -12,  17,  14,  17,  17,  38,  23,  11,
     10,  17,  23,  15,  20,  45,  44,  13,
     -8,  22,  24,  27,  26,  33,  26,   3,
    -18,  -4,  21,  24,  27,  23,   9, -11,
    -19,  -3,  11,  21,  23,  16,   7,  -9,
    -27, -11,   4,  13,  14,   4,  -5, -17,
    -53, -34, -21, -11, -28, -14, -24, -43
]
eg_blackking_table = list(reversed(eg_whiteking_table))

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
        if end_game:
            positional_value = eg_whitepawn_table[square] if color == chess.WHITE else eg_blackpawn_table[square]
        else:
            positional_value = mg_whitepawn_table[square] if color == chess.WHITE else mg_blackpawn_table[square]
        
    elif piece_type == chess.KNIGHT:
        if end_game:
            positional_value = eg_whiteknight_table[square] if color == chess.WHITE else eg_blackknight_table[square]
        else:
            positional_value = mg_whiteknight_table[square] if color == chess.WHITE else mg_blackknight_table[square]
        
    elif piece_type == chess.BISHOP:
        if end_game:
            positional_value = eg_whitebishop_table[square] if color == chess.WHITE else eg_blackbishop_table[square]
        else:
            positional_value = mg_whitebishop_table[square] if color == chess.WHITE else mg_blackbishop_table[square]
        
    elif piece_type == chess.ROOK:
        if end_game:
            positional_value = eg_whiterook_table[square] if color == chess.WHITE else eg_blackrook_table[square]
        else:
            positional_value = mg_whiterook_table[square] if color == chess.WHITE else mg_blackrook_table[square]
        
    elif piece_type == chess.QUEEN:
        if end_game:
            positional_value = eg_whitequeen_table[square] if color == chess.WHITE else eg_blackqueen_table[square]
        else:
            positional_value = mg_whitequeen_table[square] if color == chess.WHITE else mg_blackqueen_table[square]
        #positional_value = queenEval[square]
    elif piece_type == chess.KING:
        if end_game:
            positional_value = eg_whiteking_table[square] if color == chess.WHITE else eg_blackking_table[square]
        else:
            positional_value = mg_whiteking_table[square] if color == chess.WHITE else mg_blackking_table[square]
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




