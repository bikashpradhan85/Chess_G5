import os
import time
import pygame

from settings import *

from board import (
    initial_state,
    piece_color,
    make_move,
    apply_promotion
)

from pieces import (
    legal_moves_for_piece,
    all_legal_moves,
    is_checkmate,
    is_stalemate,
    in_check
)

from ai import (
    choose_best_move,
    promotion_piece_for_move
)

from timer import GameClock
from evaluation import evaluate


def get_square_from_mouse(pos):

    x, y = pos

    if 0 <= x < BOARD_PX and 0 <= y < BOARD_PX:
        return y // TILE_SIZE, x // TILE_SIZE

    return None


def load_piece_images():

    piece_images = {}

    names = [
        "wK", "wQ", "wR", "wB", "wN", "wP",
        "bK", "bQ", "bR", "bB", "bN", "bP"
    ]

    for name in names:

        path = os.path.join(
            "assets",
            f"{name}.png"
        )

        image = pygame.image.load(path).convert_alpha()

        image = pygame.transform.smoothscale(
            image,
            (
                TILE_SIZE - 10,
                TILE_SIZE - 10
            )
        )

        piece_images[name] = image

    return piece_images


def piece_key(piece):

    prefix = "w" if piece.isupper() else "b"

    return prefix + piece.upper()


def draw_eval_bar(screen, score):

    bar_x = BOARD_PX
    bar_h = BOARD_PX

    pygame.draw.rect(
        screen,
        (35, 35, 35),
        pygame.Rect(
            bar_x,
            0,
            EVAL_BAR_WIDTH,
            bar_h
        )
    )

    clamped = max(
        -3000,
        min(3000, score)
    )

    ratio = (clamped + 3000) / 6000

    white_h = int(bar_h * ratio)

    pygame.draw.rect(
        screen,
        WHITE,
        pygame.Rect(
            bar_x,
            bar_h - white_h,
            EVAL_BAR_WIDTH,
            white_h
        )
    )

    pygame.draw.rect(
        screen,
        BLACK,
        pygame.Rect(
            bar_x,
            0,
            EVAL_BAR_WIDTH,
            bar_h - white_h
        )
    )

    pygame.draw.line(
        screen,
        RED,
        (bar_x, bar_h // 2),
        (bar_x + EVAL_BAR_WIDTH, bar_h // 2),
        2
    )

    font = pygame.font.SysFont(
        "arial",
        16,
        bold=True
    )

    text = font.render(
        f"{score / 100:.1f}",
        True,
        GOLD
    )

    screen.blit(
        text,
        (
            bar_x + 5,
            10
        )
    )


def draw_board(
    screen,
    state,
    piece_images,
    selected=None,
    legal_moves=None,
    small_font=None,
    game_clock=None,
    message=""
):

    board = state["board"]

    for r in range(8):

        for c in range(8):

            color = (
                LIGHT
                if (r + c) % 2 == 0
                else DARK
            )

            pygame.draw.rect(
                screen,
                color,
                pygame.Rect(
                    c * TILE_SIZE,
                    r * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )
            )

    draw_eval_bar(
        screen,
        evaluate(board)
    )

    # selected square
    if selected:

        sr, sc = selected

        pygame.draw.rect(
            screen,
            BLUE,
            pygame.Rect(
                sc * TILE_SIZE,
                sr * TILE_SIZE,
                TILE_SIZE,
                TILE_SIZE
            ),
            4
        )

    # legal moves
    if legal_moves:

        for _, _, er, ec in legal_moves:

            center = (
                ec * TILE_SIZE + TILE_SIZE // 2,
                er * TILE_SIZE + TILE_SIZE // 2
            )

            pygame.draw.circle(
                screen,
                GREEN,
                center,
                10
            )

    # draw pieces
    for r in range(8):

        for c in range(8):

            piece = board[r][c]

            if piece != ".":

                image = piece_images[
                    piece_key(piece)
                ]

                rect = image.get_rect(
                    center=(
                        c * TILE_SIZE + TILE_SIZE // 2,
                        r * TILE_SIZE + TILE_SIZE // 2
                    )
                )

                screen.blit(
                    image,
                    rect
                )

    # bottom panel
    pygame.draw.rect(
        screen,
        (20, 20, 20),
        pygame.Rect(
            0,
            BOARD_PX,
            WIDTH,
            HEIGHT - BOARD_PX
        )
    )

    white_time = game_clock.format_time(
        "white"
    )

    black_time = game_clock.format_time(
        "black"
    )

    t1 = small_font.render(
        f"White: {white_time}",
        True,
        WHITE
    )

    t2 = small_font.render(
        f"Black: {black_time}",
        True,
        WHITE
    )

    msg = small_font.render(
        message,
        True,
        GOLD
    )

    screen.blit(
        t1,
        (20, BOARD_PX + 10)
    )

    screen.blit(
        t2,
        (250, BOARD_PX + 10)
    )

    screen.blit(
        msg,
        (20, BOARD_PX + 50)
    )


def draw_promotion_menu(screen):

    overlay = pygame.Surface(
        (BOARD_PX, BOARD_PX),
        pygame.SRCALPHA
    )

    overlay.fill(
        (0, 0, 0, 180)
    )

    screen.blit(
        overlay,
        (0, 0)
    )

    panel = pygame.Rect(
        120,
        250,
        400,
        150
    )

    pygame.draw.rect(
        screen,
        (245, 245, 245),
        panel,
        border_radius=12
    )

    pygame.draw.rect(
        screen,
        (40, 40, 40),
        panel,
        2,
        border_radius=12
    )

    font = pygame.font.SysFont(
        "arial",
        28,
        bold=True
    )

    label = font.render(
        "Choose promotion piece",
        True,
        BLACK
    )

    screen.blit(
        label,
        (panel.x + 60, panel.y + 15)
    )

    pieces = ["Q", "R", "B", "N"]

    buttons = {}

    colors = [
        BLUE,
        GREEN,
        RED,
        GOLD
    ]

    for i, p in enumerate(pieces):

        rect = pygame.Rect(
            150 + i * 90,
            300,
            70,
            70
        )

        buttons[p] = rect

        pygame.draw.rect(
            screen,
            colors[i],
            rect,
            border_radius=10
        )

        txt = font.render(
            p,
            True,
            WHITE
        )

        screen.blit(
            txt,
            txt.get_rect(center=rect.center)
        )

    return buttons


def ai_move(state, game_clock):

    legal = all_legal_moves(
        state,
        "black"
    )

    if not legal:
        return state, None

    start = time.time()

    score, best_move = choose_best_move(
        state,
        "black",
        max_depth=4
    )

    elapsed = time.time() - start

    game_clock.remaining["black"] -= elapsed

    if best_move is None:
        best_move = legal[0]

    promo = promotion_piece_for_move(
        state,
        best_move
    )

    new_state = make_move(
        state,
        best_move,
        promotion_piece=promo
    )

    return new_state, best_move


def main():

    pygame.init()

    screen = pygame.display.set_mode(
        (WIDTH, HEIGHT)
    )

    pygame.display.set_caption(
        "Simplified Chess Engine"
    )

    clock = pygame.time.Clock()

    state = initial_state()

    piece_images = load_piece_images()

    game_clock = GameClock(
        600,
        600
    )

    small_font = pygame.font.SysFont(
        "arial",
        24
    )

    selected = None
    legal_moves = []

    turn = "white"

    running = True
    game_over = False

    message = "White to move"

    promotion_pending = False
    promotion_square = None
    promotion_state_after_move = None

    while running:

        clock.tick(60)

        if not game_over:
            game_clock.update()

        timeout_winner = game_clock.winner_on_time()

        if timeout_winner:

            game_over = True

            message = f"{timeout_winner.title()} wins on time!"

        # AI MOVE
        if (
            not game_over
            and not promotion_pending
            and turn == "black"
        ):

            state, best_move = ai_move(
                state,
                game_clock
            )

            if best_move is None:

                if is_checkmate(
                    state,
                    "black"
                ):

                    game_over = True

                    message = "White wins by checkmate!"

                elif is_stalemate(
                    state,
                    "black"
                ):

                    game_over = True

                    message = "Stalemate!"

            else:

                turn = "white"

                game_clock.switch_turn(
                    "white"
                )

                if is_checkmate(
                    state,
                    "white"
                ):

                    game_over = True

                    message = "Black wins by checkmate!"

                elif is_stalemate(
                    state,
                    "white"
                ):

                    game_over = True

                    message = "Stalemate!"

                else:

                    message = "White to move"

        # EVENTS
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if game_over:
                continue

            # promotion
            if promotion_pending:

                if (
                    event.type == pygame.MOUSEBUTTONDOWN
                    and event.button == 1
                ):

                    buttons = draw_promotion_menu(
                        screen
                    )

                    for label, rect in buttons.items():

                        if rect.collidepoint(
                            event.pos
                        ):

                            state = apply_promotion(
                                promotion_state_after_move,
                                promotion_square,
                                label
                            )

                            promotion_pending = False

                            promotion_square = None

                            promotion_state_after_move = None

                            turn = "black"

                            game_clock.switch_turn(
                                "black"
                            )

                            message = "Black thinking..."

                continue

            # HUMAN MOVE
            if (
                turn == "white"
                and event.type == pygame.MOUSEBUTTONDOWN
                and event.button == 1
            ):

                sq = get_square_from_mouse(
                    event.pos
                )

                if sq is None:
                    continue

                r, c = sq

                piece = state["board"][r][c]

                if selected is None:

                    if (
                        piece != "."
                        and piece_color(piece) == "white"
                    ):

                        selected = (r, c)

                        legal_moves = legal_moves_for_piece(
                            state,
                            r,
                            c
                        )

                else:

                    move = (
                        selected[0],
                        selected[1],
                        r,
                        c
                    )

                    if move in legal_moves:

                        moving_piece = state["board"][
                            selected[0]
                        ][selected[1]]

                        # promotion
                        if (
                            moving_piece == "P"
                            and r == 0
                        ):

                            promotion_state_after_move = make_move(
                                state,
                                move,
                                promotion_piece=None
                            )

                            promotion_pending = True

                            promotion_square = (r, c)

                            selected = None
                            legal_moves = []

                            message = "Choose promotion"

                        else:

                            state = make_move(
                                state,
                                move,
                                promotion_piece=None
                            )

                            selected = None
                            legal_moves = []

                            turn = "black"

                            game_clock.switch_turn(
                                "black"
                            )

                            message = "Black thinking..."

                    else:

                        if (
                            piece != "."
                            and piece_color(piece) == "white"
                        ):

                            selected = (r, c)

                            legal_moves = legal_moves_for_piece(
                                state,
                                r,
                                c
                            )

                        else:

                            selected = None
                            legal_moves = []

        status = message

        if (
            not game_over
            and not promotion_pending
            and in_check(state, turn)
        ):

            status = f"{turn.title()} is in check!"

        draw_board(
            screen,
            state,
            piece_images,
            selected,
            legal_moves,
            small_font,
            game_clock,
            status
        )

        if promotion_pending:
            draw_promotion_menu(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()