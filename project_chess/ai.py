from pieces import all_legal_moves, in_check, is_checkmate, is_stalemate
from board import make_move
from evaluation import evaluate

MATE_SCORE = 1000000

def promotion_piece_for_move(state, move):
    sr, sc, er, ec = move
    piece = state["board"][sr][sc]
    if piece == "P" and er == 0:
        return "Q"
    if piece == "p" and er == 7:
        return "q"
    return None

def move_order_score(state, move):
    board = state["board"]
    sr, sc, er, ec = move
    piece = board[sr][sc]
    target = board[er][ec]

    score = 0

    # captures first
    if target != ".":
        victim = abs(evaluate([[target]])) if False else 0
        piece_values = {
            "P": 100, "N": 320, "B": 330, "R": 500, "Q": 900, "K": 20000,
            "p": 100, "n": 320, "b": 330, "r": 500, "q": 900, "k": 20000,
        }
        score += 10 * piece_values.get(target, 0) - piece_values.get(piece, 0)

    # promotions
    if piece in ("P", "p") and (er == 0 or er == 7):
        score += 800

    # checks
    promo = promotion_piece_for_move(state, move)
    new_state = make_move(state, move, promotion_piece=promo)
    enemy = "black" if piece.isupper() else "white"
    if in_check(new_state, enemy):
        score += 200

    return score

def board_key(state, side_to_move):
    board = state["board"]
    board_part = "/".join("".join(row) for row in board)
    castling = state["castling"]
    ep = state["en_passant"]
    return (
        board_part,
        side_to_move,
        castling["white"]["K"], castling["white"]["Q"],
        castling["black"]["K"], castling["black"]["Q"],
        ep
    )

def negamax(state, depth, alpha, beta, color_sign, side_to_move, tt):
    key = (board_key(state, side_to_move), depth, alpha, beta, color_sign)

    if depth == 0:
        return color_sign * evaluate(state["board"]), None

    if is_checkmate(state, side_to_move):
        return (-MATE_SCORE + (5 - depth)) * color_sign, None

    if is_stalemate(state, side_to_move):
        return 0, None

    if key in tt:
        return tt[key]

    moves = all_legal_moves(state, side_to_move)
    if not moves:
        return color_sign * evaluate(state["board"]), None

    moves.sort(key=lambda m: move_order_score(state, m), reverse=True)

    best_score = -10**18
    best_move = None
    next_side = "black" if side_to_move == "white" else "white"

    for move in moves:
        promo = promotion_piece_for_move(state, move)
        child = make_move(state, move, promotion_piece=promo)
        score, _ = negamax(child, depth - 1, -beta, -alpha, -color_sign, next_side, tt)
        score = -score

        if score > best_score:
            best_score = score
            best_move = move

        alpha = max(alpha, score)
        if alpha >= beta:
            break

    tt[key] = (best_score, best_move)
    return best_score, best_move

def choose_best_move(state, side_to_move, max_depth=4):
    tt = {}
    best_move = None
    best_score = -10**18

    for depth in range(1, max_depth + 1):
        score, move = negamax(state, depth, -10**18, 10**18, 1 if side_to_move == "white" else -1, side_to_move, tt)
        if move is not None:
            best_move = move
            best_score = score

    return best_score, best_move