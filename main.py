import random

import pyglet
from pyglet.gl import GL_QUADS
from pyglet.window import key

COLORS = [
    (255,   0,   0),  # RED       1
    (  0, 255,   0),  # GREEN     2
    (  0,   0, 255),  # BLUE      3
    (255, 255,   0),  # YELLOW    4
    (255,   0, 255),  # PURPLE    5
    (  0, 255, 255)   # CYAN      6
]


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

        self.tiles = [[random.randrange(0, len(COLORS)) for x in range(
            self.WIDTH)] for y in range(self.HEIGHT)]
        self.moves = 0

    def draw_rect(self, x: int, y: int, color: tuple):
        x0 = x * self.TILESIZE + self.OFFSET
        x1 = x0 + self.TILESIZE
        y0 = y * self.TILESIZE + 3 * self.OFFSET
        y1 = y0 + self.TILESIZE

        vertex_data = ('v2i', (x0, y0, x0, y1, x1, y1, x1, y0))
        color_data = ('c3B', color * 4)

        pyglet.graphics.draw(4, GL_QUADS, vertex_data, color_data)

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

        self.check_for_win(new_color)

    def check_for_win(self, color: int):
        for row in self.tiles:
            for tile in row:
                if tile != color:
                    break
            else:
                continue
            break
        else:
            self.end_game()

    def end_game(self):
        # TODO: Make end game screen
        print(f'Moves: {self.moves}')
        self.close()

    def run(self):
        pyglet.app.run()

    def on_draw(self):
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                self.draw_rect(x, y, COLORS[self.tiles[y][x]])

        self.draw_rect(0, -2, COLORS[0])
        self.draw_rect(2, -2, COLORS[1])
        self.draw_rect(4, -2, COLORS[2])
        self.draw_rect(6, -2, COLORS[3])
        self.draw_rect(8, -2, COLORS[4])
        self.draw_rect(10, -2, COLORS[5])

    def on_key_press(self, symbol, mod):
        if symbol == key.ESCAPE:
            self.close()
            return

        if 49 <= symbol <= 54:
            self.floodfill(symbol - 49)


def main():
    window = Window()
    window.run()


if __name__ == '__main__':
    main()
