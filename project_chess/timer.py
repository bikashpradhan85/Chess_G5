import time

class GameClock:
    def __init__(self, white_seconds=600, black_seconds=600):
        self.remaining = {
            "white": float(white_seconds),
            "black": float(black_seconds),
        }
        self.active_color = "white"
        self.last_tick = time.time()

    def switch_turn(self, color):
        self.active_color = color
        self.last_tick = time.time()

    def update(self):
        now = time.time()
        elapsed = now - self.last_tick
        self.remaining[self.active_color] -= elapsed
        self.last_tick = now

    def winner_on_time(self):
        if self.remaining["white"] <= 0:
            return "black"
        if self.remaining["black"] <= 0:
            return "white"
        return None

    def format_time(self, color):
        total = max(0, int(self.remaining[color]))
        m = total // 60
        s = total % 60
        return f"{m:02d}:{s:02d}"