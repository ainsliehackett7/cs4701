import chess
from constants import PAWN_VALUE, KNIGHT_VALUE, BISHOP_VALUE, ROOK_VALUE, QUEEN_VALUE
from constants import PAWN_TABLE, KNIGHT_TABLE, BISHOP_TABLE
from constants import ROOK_TABLE, QUEEN_TABLE, KING_TABLE, DRAW_VALUE
from stockfish import Stockfish

# Configure the Stockfish engine
sf = Stockfish("stockfish/stockfish")

# Define piece values
piece_values = {
    chess.PAWN: PAWN_VALUE,
    chess.KNIGHT: KNIGHT_VALUE,
    chess.BISHOP: BISHOP_VALUE,
    chess.ROOK: ROOK_VALUE,
    chess.QUEEN: QUEEN_VALUE,
    chess.KING: 0
}

# MATERIAL COUNT EVALUATION
def material_count(board):
    score = 0
    for piece_type in piece_values:
        white_pieces = board.pieces(piece_type, chess.WHITE) # Might need to fix!!
        black_pieces = board.pieces(piece_type, chess.BLACK)
        score += piece_values[piece_type] * (len(white_pieces) - len(black_pieces))
    return score

# SQUARE CONTROL EVALUATION
def evaluate_square_control(board):
    weakening_values = dynamic_weakening(board)
    reinforcement_values = dynamic_reinforcement(board)
    combined_control_values = [w + r for w, r in zip(weakening_values, reinforcement_values)]
    control_score = sum(combined_control_values)
    return control_score

def dynamic_weakening(board):
    square_values = [0] * 64
    for square in chess.SQUARES:
        if board.is_attacked_by(chess.WHITE, square):
            square_values[square] -= 1  # Weakening by White attack
        if board.is_attacked_by(chess.BLACK, square):
            square_values[square] += 1  # Weakening by Black attack
    return square_values

def dynamic_reinforcement(board):
    square_reinforcement = [0] * 64
    for square in chess.SQUARES:
        white_defenders = board.attackers(chess.WHITE, square)
        black_defenders = board.attackers(chess.BLACK, square)
        square_reinforcement[square] += len(white_defenders) - len(black_defenders)
    return square_reinforcement

# PIECE POSITION EVALUATION
def piece_position_evaluation(board):
    control_score = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            row, col = divmod(square, 8)
            piece_type = piece.piece_type
            piece_color = piece.color

            if piece_type == chess.PAWN:
                piece_value = PAWN_TABLE[row][col]
            elif piece_type == chess.KNIGHT:
                piece_value = KNIGHT_TABLE[row][col]
            elif piece_type == chess.BISHOP:
                piece_value = BISHOP_TABLE[row][col]
            elif piece_type == chess.ROOK:
                piece_value = ROOK_TABLE[row][col]
            elif piece_type == chess.QUEEN:
                piece_value = QUEEN_TABLE[row][col]
            elif piece_type == chess.KING:
                piece_value = KING_TABLE[row][col]
            else:
                continue

            # Adjust the total control score based on the color of the piece
            if piece_color == chess.WHITE:
                control_score += piece_value
            else:
                control_score -= piece_value

    return control_score


# PAWN STRUCTURE EVALUATION
def count_doubled_pawns(board, color):
    doubled_pawns = 0
    for file in range(8):
        pawns_in_file = list(board.pieces(chess.PAWN, color)).count(file)
        if pawns_in_file > 1:
            doubled_pawns += (pawns_in_file - 1)
    return doubled_pawns

def count_isolated_pawns(board, color):
    isolated_pawns = 0
    for file in range(8):
        if not list(board.pieces(chess.PAWN, color)).count(file - 1) and not list(board.pieces(chess.PAWN, color)).count(file + 1):
            isolated_pawns += list(board.pieces(chess.PAWN, color)).count(file)
    return isolated_pawns

def pawn_structure_evaluation(board):
    white_doubled_pawns = count_doubled_pawns(board, chess.WHITE)
    black_doubled_pawns = count_doubled_pawns(board, chess.BLACK)
    white_isolated_pawns = count_isolated_pawns(board, chess.WHITE)
    black_isolated_pawns = count_isolated_pawns(board, chess.BLACK)

    # Assign penalties for doubled and isolated pawns
    doubled_pawn_penalty = -10
    isolated_pawn_penalty = -20

    evaluation = 0
    evaluation += (white_doubled_pawns - black_doubled_pawns) * doubled_pawn_penalty
    evaluation += (white_isolated_pawns - black_isolated_pawns) * isolated_pawn_penalty

    return evaluation

# KING SAFETY EVALUATION
def king_safety_evaluation(board):
    white_king_safety = evaluate_king_shield(board, chess.WHITE)
    black_king_safety = evaluate_king_shield(board, chess.BLACK)
    return white_king_safety - black_king_safety

def evaluate_king_shield(board, color):
    king_square = board.king(color)
    king_shield_penalty = 0
    pawn_shield_files = range(max(0, king_square % 8 - 1), min(8, king_square % 8 + 2))
    pawn_shield_ranks = [king_square // 8, king_square // 8 + (1 if color == chess.WHITE else -1)]
    pawn_shield_ranks = [r for r in pawn_shield_ranks if 0 <= r <= 7]
    for file in pawn_shield_files:
        for rank in pawn_shield_ranks:
            if not board.piece_at(chess.square(file, rank)) == chess.Piece(chess.PAWN, color):
                king_shield_penalty -= 1

    return king_shield_penalty

# EVALUATE BOARD
def evaluate_board(board, scheme='material_count'):
    if scheme == 'king_safety':
        evaluation = simple_evaluation(board)
        evaluation += king_safety_evaluation(board)
    elif scheme == 'piece_position':
        evaluation = simple_evaluation(board)
        evaluation += piece_position_evaluation(board)
    elif scheme == 'square_control':
        evaluation = simple_evaluation(board)
        evaluation += evaluate_square_control(board)
    elif scheme == 'pawn_structure':
        evaluation = simple_evaluation(board)
        evaluation += pawn_structure_evaluation(board)
    elif scheme == 'combined':
        evaluation = simple_evaluation(board)
        evaluation += king_safety_evaluation(board)
        evaluation += piece_position_evaluation(board)
        evaluation += evaluate_square_control(board)
        evaluation += pawn_structure_evaluation(board)
    else:
        evaluation = simple_evaluation(board)
        
    return evaluation

# SIMPLE EVAL -- MATERIAL COUNT

def simple_evaluation(board):
    if board.is_insufficient_material():
        return DRAW_VALUE

    wp = len(board.pieces(chess.PAWN, chess.WHITE))
    bp = len(board.pieces(chess.PAWN, chess.BLACK))

    wn = len(board.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(board.pieces(chess.KNIGHT, chess.BLACK))

    wb = len(board.pieces(chess.BISHOP, chess.WHITE))
    bb = len(board.pieces(chess.BISHOP, chess.BLACK))

    wr = len(board.pieces(chess.ROOK, chess.WHITE))
    br = len(board.pieces(chess.ROOK, chess.BLACK))

    wq = len(board.pieces(chess.QUEEN, chess.WHITE))
    bq = len(board.pieces(chess.QUEEN, chess.BLACK))

    value = (
        PAWN_VALUE * (wp - bp) +
        KNIGHT_VALUE * (wn - bn) +
        BISHOP_VALUE * (wb - bb) +
        ROOK_VALUE * (wr - br) +
        QUEEN_VALUE * (wq - bq)
    )

    if board.turn == chess.WHITE:
        return value
    return -value