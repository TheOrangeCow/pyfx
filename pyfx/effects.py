import random
import shutil
import sys
import time

RESET = "\033[0m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"
CLEAR = "\033[2J\033[H"

def _supports_color():
    return sys.stdout.isatty() and "NO_COLOR" not in __import__("os").environ

def _color(text, code, enabled=True):
    return f"\033[{code}m{text}{RESET}" if enabled else text

def clear():
    print(CLEAR, end="", flush=True)

def _dimensions():
    size = shutil.get_terminal_size((80, 24))
    return max(20, size.columns), max(8, size.lines - 1)

def _animate(draw, fps=20, frames=None):
    color = _supports_color()
    delay = 1 / max(1, fps)
    i = 0
    print(HIDE_CURSOR, end="", flush=True)
    try:
        while frames is None or i < frames:
            width, height = _dimensions()
            output = draw(width, height, i, color)
            print("\033[H" + output, end="", flush=True)
            i += 1
            time.sleep(delay)
    except KeyboardInterrupt:
        pass
    finally:
        print(SHOW_CURSOR + RESET, end="", flush=True)
        print()

def fire(fps=18, frames=None, intensity=1.0):
    """Show an animated ASCII fire effect. Ctrl+C stops the animation."""
    heat = []
    chars = " .,:;irsXA253hMHGS#9B&@"
    palette = [31, 91, 33, 93, 97]
    def draw(w, h, frame, color):
        nonlocal heat
        if len(heat) != h or any(len(row) != w for row in heat):
            heat = [[0.0] * w for _ in range(h)]
        for x in range(w):
            heat[h-1][x] = random.random() * intensity
        for y in range(h-2, -1, -1):
            for x in range(w):
                below = heat[y+1][x]
                left = heat[y+1][(x-1) % w]
                right = heat[y+1][(x+1) % w]
                below2 = heat[min(h-1, y+2)][x]
                heat[y][x] = max(0, min(1, (below + left + right + below2) / 4.05 - random.random() * 0.07))
        rows = []
        for row in heat:
            line = ""
            for value in row:
                idx = min(len(chars)-1, int(value * (len(chars)-1)))
                code = palette[min(len(palette)-1, int(value * len(palette)))]
                line += _color(chars[idx], code, color)
            rows.append(line)
        return "\n".join(rows)
    _animate(draw, fps, frames)

def matrix(fps=20, frames=None, density=0.045):
    """Show falling green Matrix-style characters. Ctrl+C stops the animation."""
    streams = {}
    alphabet = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ#$%&+-<>"
    def draw(w, h, frame, color):
        for x in range(w):
            if x not in streams and random.random() < density:
                streams[x] = random.randint(-h, 0)
        grid = [[" "] * w for _ in range(h)]
        for x in list(streams):
            y = streams[x]
            if y < h:
                if y >= 0:
                    grid[y][x] = random.choice(alphabet)
                if y - random.randint(5, 15) >= 0 and y - random.randint(5, 15) < h:
                    grid[max(0, y - 8)][x] = random.choice(alphabet)
            streams[x] += 1
            if streams[x] > h + random.randint(2, 12):
                del streams[x]
        rows = []
        for row in grid:
            line = ""
            for ch in row:
                line += _color(ch, "92" if ch != " " else "32", color)
            rows.append(line)
        return "\n".join(rows)
    _animate(draw, fps, frames)

def stars(fps=18, frames=None, count=100):
    """Show a twinkling starfield with a simple depth illusion."""
    points = []
    def draw(w, h, frame, color):
        nonlocal points
        if not points:
            points = [[random.randrange(w), random.randrange(h), random.choice([1, 2, 3])] for _ in range(count)]
        grid = [[" "] * w for _ in range(h)]
        for p in points:
            p[0] -= p[2] - 1
            if p[0] < 0:
                p[:] = [w-1, random.randrange(h), random.choice([1, 2, 3])]
            if 0 <= p[1] < h:
                grid[p[1]][p[0]] = "." if p[2] == 1 else ("+" if p[2] == 2 else "*")
        rows = []
        for row in grid:
            rows.append("".join(_color(ch, "97" if ch == "*" else "90", color) for ch in row))
        return "\n".join(rows)
    _animate(draw, fps, frames)

def rain(fps=20, frames=None, density=0.035):
    """Show animated rainfall."""
    drops = []
    def draw(w, h, frame, color):
        for x in range(w):
            if random.random() < density:
                drops.append([x, 0, random.randint(2, max(2, h // 3))])
        grid = [[" "] * w for _ in range(h)]
        alive = []
        for x, y, length in drops:
            for offset in range(length):
                yy = y - offset
                if 0 <= yy < h:
                    grid[yy][x] = "|" if offset else "'"
            y += 1
            if y - length < h:
                alive.append([x, y, length])
        drops = alive
        rows = []
        for row in grid:
            rows.append("".join(_color(ch, "94", color) for ch in row))
        return "\n".join(rows)
    _animate(draw, fps, frames)

def confetti(fps=24, frames=None, count=100):
    """Show colorful falling confetti."""
    pieces = []
    codes = [31, 32, 33, 34, 35, 36, 91, 92, 93, 95, 96]
    def draw(w, h, frame, color):
        nonlocal pieces
        while len(pieces) < count:
            pieces.append([random.randrange(w), random.randrange(-h, 0), random.choice(["*", "+", ".", "o"]), random.choice(codes), random.choice([-1, 0, 1])])
        grid = [[" "] * w for _ in range(h)]
        alive = []
        for x, y, ch, code, drift in pieces:
            x = (x + drift) % w
            y += 1
            if y < h:
                grid[y][x] = _color(ch, code, color)
                alive.append([x, y, ch, code, drift])
        pieces = alive
        return "\n".join("".join(row) for row in grid)
    _animate(draw, fps, frames)

def explosion(fps=24, frames=24, particles=90):
    """Play a one-shot expanding particle explosion."""
    points = []
    def draw(w, h, frame, color):
        nonlocal points
        cx, cy = w // 2, h // 2
        if not points:
            for _ in range(particles):
                angle = random.random() * 6.28318
                speed = random.uniform(0.2, 1.0)
                points.append([cx, cy, __import__("math").cos(angle) * speed, __import__("math").sin(angle) * speed, random.choice([31, 33, 91, 93, 97])])
        grid = [[" "] * w for _ in range(h)]
        for p in points:
            x = int(p[0] + p[2] * frame * 1.3)
            y = int(p[1] + p[3] * frame * 0.6)
            if 0 <= x < w and 0 <= y < h:
                grid[y][x] = _color(random.choice(["*", "+", ".", "x"]), p[4], color)
        return "\n".join("".join(row) for row in grid)
    _animate(draw, fps, frames)

def run(effect="stars", **kwargs):
    """Run an effect by name, e.g. run('matrix', fps=25)."""
    effects = {"fire": fire, "matrix": matrix, "stars": stars, "rain": rain, "confetti": confetti, "explosion": explosion}
    try:
        fn = effects[effect.lower()]
    except (KeyError, AttributeError):
        raise ValueError(f"Unknown effect {effect!r}. Choose from: {', '.join(effects)}")
    return fn(**kwargs)

