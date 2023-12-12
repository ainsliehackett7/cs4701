import chess


class ChessBoard(chess.Board):
    def __init__(self, fen=None):
        super().__init__(fen=fen)  # Call the constructor of the parent class

    def get_bitboard(self, piece_type, color):
        return int(self.board.pieces(piece_type, color))

    def generate_bitboards(self):
        bitboards = {}
        for color in [chess.WHITE, chess.BLACK]:
            for piece_type in [chess.PAWN, chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]:
                bitboards[(piece_type, color)] = self.get_bitboard(
                    piece_type, color)
        return bitboards

    def display(self):
        # Custom display logic
        print(self.board)


'''
    def push(self, move):
        self.board.push(move)

    def pop(self):
        self.board.pop()
    
    def turn(self):
        return self.board.turn

    def is_capture(self, move):
        return self.board.is_capture(move)

    def is_checkmate(self):
        return self.board.is_checkmate()
    
    def is_game_over(self):
        return self.board.is_game_over()

    def legal_moves(self):
        return self.board.legal_moves
    
    def pieces(self, piece_type, color):
        return self.board.pieces(piece_type, color)
    
    def copy(self):
        return ChessBoard(self.board.fen())

    def __str__(self):
        return str(self.board)

    # Additional methods as needed
'''
