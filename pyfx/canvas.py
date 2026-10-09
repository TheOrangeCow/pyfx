from dataclasses import dataclass


@dataclass
class Frame:
    width: int
    height: int
    fill: str = " "

    def __post_init__(self):
        if len(self.fill) != 1:
            raise ValueError("fill must be exactly one character")
        self._grid = [
            [self.fill for _ in range(self.width)] for _ in range(self.height)
        ]

    def text(self, x, y, value):
        if 0 <= y < self.height:
            for i, char in enumerate(str(value)):
                xx = x + i
                if 0 <= xx < self.width:
                    self._grid[y][xx] = char
        return self

    def point(self, x, y, char="*"):
        if len(char) != 1:
            raise ValueError("char must be exactly one character")
        if 0 <= x < self.width and 0 <= y < self.height:
            self._grid[y][x] = char
        return self

    def line(self, x1, y1, x2, y2, char="*"):
        dx, dy = abs(x2 - x1), abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        while True:
            self.point(x1, y1, char)
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        return self

    def rectangle(self, x, y, width, height, char="#", filled=False):
        if width <= 0 or height <= 0:
            return self
        for yy in range(y, y + height):
            for xx in range(x, x + width):
                if filled or yy in (y, y + height - 1) or xx in (x, x + width - 1):
                    self.point(xx, yy, char)
        return self

    def render(self):
        return "\n".join("".join(row) for row in self._grid)

    def show(self):
        print(self.render())


Canvas = Frame
