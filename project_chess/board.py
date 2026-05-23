from copy import deepcopy

def initial_board():
    return [
        ["r", "n", "b", "q", "k", "b", "n", "r"],
        ["p", "p", "p", "p", "p", "p", "p", "p"],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        [".", ".", ".", ".", ".", ".", ".", "."],
        ["P", "P", "P", "P", "P", "P", "P", "P"],
        ["R", "N", "B", "Q", "K", "B", "N", "R"],
    ]

def initial_state():
    return {
        "board": initial_board(),
        "castling": {
            "white": {"K": True, "Q": True},
            "black": {"K": True, "Q": True},
        },
        "en_passant": None,
    }

def inside(r, c):
    return 0 <= r < 8 and 0 <= c < 8

def piece_color(piece):
    if piece == ".":
        return None
    return "white" if piece.isupper() else "black"

def opponent(color):
    return "black" if color == "white" else "white"

def clone_state(state):
    return {
        "board": deepcopy(state["board"]),
        "castling": deepcopy(state["castling"]),
        "en_passant": state["en_passant"],
    }

def find_king(board, color):
    target = "K" if color == "white" else "k"
    for r in range(8):
        for c in range(8):
            if board[r][c] == target:
                return r, c
    return None

def apply_promotion(state, square, choice_piece):
    r, c = square
    board = state["board"]
    piece = board[r][c]
    if piece == ".":
        return state
    board[r][c] = choice_piece.upper() if piece.isupper() else choice_piece.lower()
    return state

def make_move(state, move, promotion_piece=None):
    sr, sc, er, ec = move
    new_state = clone_state(state)
    board = new_state["board"]
    castling = new_state["castling"]

    piece = board[sr][sc]
    target = board[er][ec]
    color = piece_color(piece)

    # captured rook affects castling rights
    if target == "R":
        if (er, ec) == (7, 0):
            castling["white"]["Q"] = False
        elif (er, ec) == (7, 7):
            castling["white"]["K"] = False
    elif target == "r":
        if (er, ec) == (0, 0):
            castling["black"]["Q"] = False
        elif (er, ec) == (0, 7):
            castling["black"]["K"] = False

    # en passant capture
    if piece.upper() == "P" and state["en_passant"] == (er, ec) and target == "." and sc != ec:
        captured_r = er + 1 if color == "white" else er - 1
        board[captured_r][ec] = "."

    # move piece
    board[er][ec] = piece
    board[sr][sc] = "."

    # king moved -> no castling
    if piece == "K":
        castling["white"]["K"] = False
        castling["white"]["Q"] = False
        if sr == 7 and sc == 4:
            if ec == 6:
                board[7][5] = board[7][7]
                board[7][7] = "."
            elif ec == 2:
                board[7][3] = board[7][0]
                board[7][0] = "."
    elif piece == "k":
        castling["black"]["K"] = False
        castling["black"]["Q"] = False
        if sr == 0 and sc == 4:
            if ec == 6:
                board[0][5] = board[0][7]
                board[0][7] = "."
            elif ec == 2:
                board[0][3] = board[0][0]
                board[0][0] = "."

    # rook moved from start
    if piece == "R":
        if (sr, sc) == (7, 0):
            castling["white"]["Q"] = False
        elif (sr, sc) == (7, 7):
            castling["white"]["K"] = False
    elif piece == "r":
        if (sr, sc) == (0, 0):
            castling["black"]["Q"] = False
        elif (sr, sc) == (0, 7):
            castling["black"]["K"] = False

    # en passant target after double push
    if piece == "P" and sr == 6 and er == 4:
        new_state["en_passant"] = (5, sc)
    elif piece == "p" and sr == 1 and er == 3:
        new_state["en_passant"] = (2, sc)
    else:
        new_state["en_passant"] = None

    # promotion
    if piece == "P" and er == 0:
        if promotion_piece is not None:
            board[er][ec] = promotion_piece.upper()
        else:
            board[er][ec] = "P"
    elif piece == "p" and er == 7:
        if promotion_piece is not None:
            board[er][ec] = promotion_piece.lower()
        else:
            board[er][ec] = "p"

    return new_state