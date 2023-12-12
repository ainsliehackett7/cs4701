import chess
from constants import PAWN_VALUE, KNIGHT_VALUE, BISHOP_VALUE, ROOK_VALUE, QUEEN_VALUE
from constants import PAWN_TABLE, KNIGHT_TABLE, BISHOP_TABLE, WHITE_SQUARES_MASK, BLACK_SQUARES_MASK
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

# MATERIAL VALUE EVALUATION
def material_value(board):
    return PAWN_VALUE * (board.piece_type_count(chess.PAWN, chess.WHITE) - board.piece_type_count(chess.PAWN, chess.BLACK)) + \
              KNIGHT_VALUE * (board.piece_type_count(chess.KNIGHT, chess.WHITE) - board.piece_type_count(chess.KNIGHT, chess.BLACK)) + \
                BISHOP_VALUE * (board.piece_type_count(chess.BISHOP, chess.WHITE) - board.piece_type_count(chess.BISHOP, chess.BLACK)) + \
                    ROOK_VALUE * (board.piece_type_count(chess.ROOK, chess.WHITE) - board.piece_type_count(chess.ROOK, chess.BLACK)) + \
                        QUEEN_VALUE * (board.piece_type_count(chess.QUEEN, chess.WHITE) - board.piece_type_count(chess.QUEEN, chess.BLACK))

# SQUARE CONTROL EVALUATION
def evaluate_square_control(board):
    weakening_values = dynamic_weakening(board)
    reinforcement_values = dynamic_reinforcement(board)
    combined_control_values = [w + r for w, r in zip(weakening_values, reinforcement_values)]
    return combined_control_values

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
    total_eval = 0

    for square in chess.SQUARES:
        piece = board.piece_at(square)
        if piece:
            piece_type = piece.piece_type
            piece_color = piece.color
            row, col = divmod(square, 8)

            # Determine the piece's base value and its position value from the table
            if piece_type == chess.PAWN:
                piece_value = PAWN_TABLE[row][col]
            elif piece_type == chess.KNIGHT:
                piece_value = KNIGHT_TABLE[row][col]
            elif piece_type == chess.BISHOP:
                piece_value = BISHOP_TABLE[row][col]
                # Apply mask if you want to differentiate between white and black square bishops
                if piece_color == chess.WHITE and not (WHITE_SQUARES_MASK & (1 << square)):
                    piece_value = 0
                elif piece_color == chess.BLACK and not (BLACK_SQUARES_MASK & (1 << square)):
                    piece_value = 0
            elif piece_type == chess.ROOK:
                piece_value = ROOK_TABLE[row][col]
            elif piece_type == chess.QUEEN:
                piece_value = QUEEN_TABLE[row][col]
            elif piece_type == chess.KING:
                piece_value = KING_TABLE[row][col]

            # Adjust the total evaluation based on the color of the piece
            if piece_color == chess.WHITE:
                total_eval += piece_value
            else:
                total_eval -= piece_value

    return total_eval

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

    # Define ranges to check for pawns around the king
    pawn_shield_files = range(max(0, king_square % 8 - 1), min(8, king_square % 8 + 2))
    pawn_shield_ranks = [king_square // 8, king_square // 8 + (1 if color == chess.WHITE else -1)]

    # Evaluate the pawn shield
    for file in pawn_shield_files:
        for rank in pawn_shield_ranks:
            if not board.piece_at(chess.square(file, rank)) == chess.Piece(chess.PAWN, color):
                king_shield_penalty -= 5  # Penalty for missing pawn shield

    return king_shield_penalty

# EVALUATE BOARD
def evaluate_board(board, scheme='material_count'):
    
    return simple_evaluation(board)
    '''
    total_evaluation = 0
    total_evaluation += material_count(board)
    total_evaluation += piece_position_evaluation(board)
    # Add other evaluation functions as they are implemented
    return total_evaluation
    '''

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