PIECE_VALUES = {
    "P": 100, "N": 320, "B": 330, "R": 500, "Q": 900, "K": 20000,
    "p": -100, "n": -320, "b": -330, "r": -500, "q": -900, "k": -20000,
}

PAWN_TABLE = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [5, 5, 10, 25, 25, 10, 5, 5],
    [0, 0, 0, 20, 20, 0, 0, 0],
    [5, -5, -10, 0, 0, -10, -5, 5],
    [5, 10, 10, -20, -20, 10, 10, 5],
    [0, 0, 0, 0, 0, 0, 0, 0],
]

KNIGHT_TABLE = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50],
]

def positional_bonus(piece, r, c):
    if piece == "P":
        return PAWN_TABLE[r][c]
    if piece == "p":
        return -PAWN_TABLE[7 - r][c]
    if piece == "N":
        return KNIGHT_TABLE[r][c]
    if piece == "n":
        return -KNIGHT_TABLE[7 - r][c]
    return 0

def evaluate(board):
    score = 0
    for r in range(8):
        for c in range(8):
            p = board[r][c]
            if p != ".":
                score += PIECE_VALUES[p]
                score += positional_bonus(p, r, c)
    return score