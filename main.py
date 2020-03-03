import random

import pyglet
from pyglet.gl import GL_QUADS
from pyglet.window import key

COLORS = [
    (255, 0, 0),    # RED       1
    (0, 255, 0),    # GREEN     2
    (0, 0, 255),    # BLUE      3
    (255, 255, 0),  # YELLOW    4
    (255, 0, 255),  # PURPLE    5
    (0, 255, 255)   # CYAN      6
]


class Board:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height

        self.tiles = [[self.rand_color() for x in range(self.width)]
                      for y in range(self.height)]
        self.moves = 0

    def rand_color(self) -> int:
        return random.randrange(0, len(COLORS))

    def floodfill(self, new_color: int):
        prev_color = self.tiles[0][0]
        if prev_color == new_color:
            return

        self.moves += 1

        def change_color(tiles, x, y, old, new):
            inside_grid = 0 <= y < len(tiles) and 0 <= x < len(tiles[y])

            if inside_grid and tiles[y][x] == old:
                tiles[y][x] = new
                change_color(tiles, x, y+1, old, new)
                change_color(tiles, x+1, y, old, new)
                change_color(tiles, x, y-1, old, new)
                change_color(tiles, x-1, y, old, new)

        change_color(self.tiles, 0, 0, prev_color, new_color)

    def check_for_win(self, color: int) -> bool:
        for row in self.tiles:
            for tile in row:
                if tile != color:
                    return False
        return True


class Window(pyglet.window.Window):
    TILESIZE = 50
    WIDTH = 11
    HEIGHT = 11
    OFFSET = TILESIZE

    def __init__(self):
        super().__init__(
            width=self.WIDTH * self.TILESIZE + 2 * self.OFFSET,
            height=self.HEIGHT * self.TILESIZE + 4 * self.OFFSET,
            caption='Flood It'
        )
        self.board = Board(self.WIDTH, self.HEIGHT)
        self.moves_label = pyglet.text.Label(f"Moves: {self.board.moves}",
                                             x=self.TILESIZE * 0.25,
                                             y=self.height - self.TILESIZE * 0.5,
                                             anchor_y='center')

    def draw_rect(self, x: int, y: int, color: tuple):
        x0 = x * self.TILESIZE + self.OFFSET
        x1 = x0 + self.TILESIZE
        y0 = y * self.TILESIZE + 3 * self.OFFSET
        y1 = y0 + self.TILESIZE

        vertex_data = ('v2i', (x0, y0, x0, y1, x1, y1, x1, y0))
        color_data = ('c3B', color * 4)

        pyglet.graphics.draw(4, GL_QUADS, vertex_data, color_data)

    def run(self):
        pyglet.app.run()

    def on_draw(self):
        self.clear()

        for y, row in enumerate(self.board.tiles):
            for x, tile in enumerate(row):
                self.draw_rect(x, y, COLORS[tile])

        self.draw_rect(0, -2, COLORS[0])
        self.draw_rect(2, -2, COLORS[1])
        self.draw_rect(4, -2, COLORS[2])
        self.draw_rect(6, -2, COLORS[3])
        self.draw_rect(8, -2, COLORS[4])
        self.draw_rect(10, -2, COLORS[5])

        self.moves_label.text = f'Moves: {self.board.moves}'
        self.moves_label.draw()

    def on_key_press(self, symbol, mod):
        if symbol == key.ESCAPE:
            self.close()
            return

        if symbol < 49 or symbol > 54:
            return

        color_index = symbol - 49
        self.board.floodfill(color_index)
        won_game = self.board.check_for_win(color_index)
        if won_game:
            self.win_game()

    def win_game(self):
        print(f'Congrats, you won in {self.board.moves} moves!')
        self.close()


def main():
    window = Window()
    window.run()


if __name__ == '__main__':
    main()
