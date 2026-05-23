from board import inside, piece_color, opponent, find_king, make_move

KNIGHT_DIRS = [
    (-2, -1), (-2, 1),
    (-1, -2), (-1, 2),
    (1, -2), (1, 2),
    (2, -1), (2, 1)
]

KING_DIRS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1), (1, 0),  (1, 1)
]

def is_square_attacked(board, r, c, by_color):
    if by_color == "white":
        pawn = "P"
        pawn_checks = [(r + 1, c - 1), (r + 1, c + 1)]
    else:
        pawn = "p"
        pawn_checks = [(r - 1, c - 1), (r - 1, c + 1)]

    for pr, pc in pawn_checks:
        if inside(pr, pc) and board[pr][pc] == pawn:
            return True

    knight = "N" if by_color == "white" else "n"
    for dr, dc in KNIGHT_DIRS:
        nr, nc = r + dr, c + dc
        if inside(nr, nc) and board[nr][nc] == knight:
            return True

    king = "K" if by_color == "white" else "k"
    for dr, dc in KING_DIRS:
        nr, nc = r + dr, c + dc
        if inside(nr, nc) and board[nr][nc] == king:
            return True

    bishop_like = {"B", "b", "Q", "q"}
    rook_like = {"R", "r", "Q", "q"}

    for dr, dc in [(-1, -1), (-1, 1), (1, -1), (1, 1)]:
        nr, nc = r + dr, c + dc
        while inside(nr, nc):
            p = board[nr][nc]
            if p != ".":
                if piece_color(p) == by_color and p in bishop_like:
                    return True
                break
            nr += dr
            nc += dc

    for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        while inside(nr, nc):
            p = board[nr][nc]
            if p != ".":
                if piece_color(p) == by_color and p in rook_like:
                    return True
                break
            nr += dr
            nc += dc

    return False

def in_check(state, color):
    board = state["board"]
    king_pos = find_king(board, color)
    if king_pos is None:
        return True
    kr, kc = king_pos
    return is_square_attacked(board, kr, kc, opponent(color))

def pseudo_moves_for_piece(state, r, c):
    board = state["board"]
    piece = board[r][c]
    if piece == ".":
        return []

    color = piece_color(piece)
    moves = []

    if piece in ("P", "p"):
        direction = -1 if piece == "P" else 1
        start_row = 6 if piece == "P" else 1

        one_r = r + direction
        if inside(one_r, c) and board[one_r][c] == ".":
            moves.append((r, c, one_r, c))

            two_r = r + 2 * direction
            if r == start_row and inside(two_r, c) and board[two_r][c] == ".":
                moves.append((r, c, two_r, c))

        for dc in (-1, 1):
            nr, nc = r + direction, c + dc
            if inside(nr, nc):
                target = board[nr][nc]
                if target != "." and piece_color(target) != color:
                    moves.append((r, c, nr, nc))

        ep = state["en_passant"]
        if ep is not None:
            er, ec = ep
            if er == r + direction and abs(ec - c) == 1:
                moves.append((r, c, er, ec))

    elif piece.upper() in ("R", "B", "Q"):
        directions = []
        if piece.upper() in ("R", "Q"):
            directions += [(-1, 0), (1, 0), (0, -1), (0, 1)]
        if piece.upper() in ("B", "Q"):
            directions += [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            while inside(nr, nc):
                target = board[nr][nc]
                if target == ".":
                    moves.append((r, c, nr, nc))
                else:
                    if piece_color(target) != color:
                        moves.append((r, c, nr, nc))
                    break
                nr += dr
                nc += dc

    elif piece.upper() == "N":
        for dr, dc in KNIGHT_DIRS:
            nr, nc = r + dr, c + dc
            if inside(nr, nc):
                target = board[nr][nc]
                if target == "." or piece_color(target) != color:
                    moves.append((r, c, nr, nc))

    elif piece.upper() == "K":
        for dr, dc in KING_DIRS:
            nr, nc = r + dr, c + dc
            if inside(nr, nc):
                target = board[nr][nc]
                if target == "." or piece_color(target) != color:
                    moves.append((r, c, nr, nc))

        if not in_check(state, color):
            castling = state["castling"][color]
            enemy = opponent(color)

            if color == "white" and (r, c) == (7, 4):
                if castling["K"] and board[7][5] == "." and board[7][6] == "." and board[7][7] == "R":
                    if not is_square_attacked(board, 7, 5, enemy) and not is_square_attacked(board, 7, 6, enemy):
                        moves.append((7, 4, 7, 6))
                if castling["Q"] and board[7][3] == "." and board[7][2] == "." and board[7][1] == "." and board[7][0] == "R":
                    if not is_square_attacked(board, 7, 3, enemy) and not is_square_attacked(board, 7, 2, enemy):
                        moves.append((7, 4, 7, 2))

            if color == "black" and (r, c) == (0, 4):
                if castling["K"] and board[0][5] == "." and board[0][6] == "." and board[0][7] == "r":
                    if not is_square_attacked(board, 0, 5, enemy) and not is_square_attacked(board, 0, 6, enemy):
                        moves.append((0, 4, 0, 6))
                if castling["Q"] and board[0][3] == "." and board[0][2] == "." and board[0][1] == "." and board[0][0] == "r":
                    if not is_square_attacked(board, 0, 3, enemy) and not is_square_attacked(board, 0, 2, enemy):
                        moves.append((0, 4, 0, 2))

    return moves

def legal_moves_for_piece(state, r, c):
    board = state["board"]
    piece = board[r][c]
    if piece == ".":
        return []

    color = piece_color(piece)
    legal = []

    for move in pseudo_moves_for_piece(state, r, c):
        sr, sc, er, ec = move

        # For promotion squares, test all promotion outcomes and keep move if any is legal
        if piece in ("P", "p") and (er == 0 or er == 7):
            legal_for_promo = False
            for promo in ("Q", "R", "B", "N"):
                test_state = make_move(state, move, promotion_piece=promo)
                if not in_check(test_state, color):
                    legal_for_promo = True
                    break
            if legal_for_promo:
                legal.append(move)
        else:
            test_state = make_move(state, move, promotion_piece="Q")
            if not in_check(test_state, color):
                legal.append(move)

    return legal

def all_legal_moves(state, color):
    board = state["board"]
    moves = []
    for r in range(8):
        for c in range(8):
            if piece_color(board[r][c]) == color:
                moves.extend(legal_moves_for_piece(state, r, c))
    return moves

def is_checkmate(state, color):
    return in_check(state, color) and len(all_legal_moves(state, color)) == 0

def is_stalemate(state, color):
    return (not in_check(state, color)) and len(all_legal_moves(state, color)) == 0