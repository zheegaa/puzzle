import pygame
import os
from random import shuffle


class Puzzle:
    def __init__(self):
        pygame.init()

        self.header_height = 50
        self.screen_height = 600
        self.screen_width = 600

        self.tile_height = self.screen_height / 5
        self.tile_width = self.screen_width / 5

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.header_height + self.screen_height)
        )
        pygame.display.set_caption("Puzzle")
        self.game_font = pygame.font.SysFont("Arial", 24)
        self.clock = pygame.time.Clock()
        self.running = True
        self.solved = False
        self.move_count = 0

        self.solution = self.get_solution()
        self.tiles = self.new_game()

        self.loop()

    def __str__(self) -> str:
        return "A puzzle game"

    def load_tiles(self) -> list:
        """Loads image as square tiles."""
        tiles = [
            {"index": i, "tile": pygame.image.load(os.path.join("images", "dog", tile))}
            for i, tile in enumerate(os.listdir("images/dog"))
        ]
        return tiles

    def get_solution(self) -> list:
        """Generates solution configuration."""
        tiles = self.load_tiles()
        # remove bottom right tile
        tiles.pop(-1)
        # add empty tile to top left
        tiles.insert(24, {"index": 24, "tile": "empty"})
        # convert to 2d array
        tiles = [tiles[i : i + 5] for i in range(0, 25, 5)]
        return tiles

    def new_game(self) -> list:
        """Generates new game configuration."""
        tiles = self.load_tiles()
        # remove bottom right tile
        tiles.pop(-1)
        # shuffle tiles
        shuffle(tiles)
        # add empty tile to top left
        tiles.insert(0, {"index": 24, "tile": "empty"})
        # convert to 2d array
        tiles = [tiles[i : i + 5] for i in range(0, 25, 5)]
        return tiles

    def empty_tile(self) -> tuple: # type: ignore
        """Locates coordinates of empty tile."""
        for row in self.tiles:
            for tile in row:
                if tile["tile"] == "empty":
                    return row.index(tile), self.tiles.index(row)

    def loop(self) -> None:
        """Main loop."""
        while self.running:
            self.events()
            if self.solved is False:
                self.screen.fill((0, 0, 0))
                self.draw_tiles()
                self.draw_lines()
                self.move_count_text()
                if [tile["index"] for row in self.tiles for tile in row] == [tile["index"] for row in self.solution for tile in row]:
                    self.solved = True
            if self.solved:
                self.victory_text()
            pygame.display.flip()
            self.clock.tick(60)

    def events(self) -> None:
        """Checks for input events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                x = event.pos[0]
                y = event.pos[1]
                self.click(x, y)

    def draw_tiles(self) -> None:
        """Draws the tiles."""
        for i in range(5):
            for j in range(5):
                # if tile is empty
                if self.tiles[j][i]["tile"] == "empty":
                    continue
                self.screen.blit(
                    self.tiles[j][i]["tile"],
                    (i * self.tile_width, self.header_height + j * self.tile_height),
                )

    def draw_lines(self) -> None:
        """Draws the grid lines."""
        for i in range(5):
            pygame.draw.line(
                self.screen,
                (0, 0, 0, 1),
                (i * self.screen_width / 5, self.header_height),
                (i * self.screen_width / 5, self.header_height + self.screen_height),
                1,
            )
            pygame.draw.line(
                self.screen,
                (0, 0, 0, 1),
                (0, self.header_height + i * self.screen_height / 5),
                (self.screen_width, self.header_height + i * self.screen_height / 5),
                1,
            )

    def click(self, x: int, y: int) -> None:
        """Moves tile to empty tile."""
        empty_i, empty_j = self.empty_tile()
        tile_i, tile_j = self.get_tile_indices(x, y)
        if self.is_moveable(tile_i, tile_j):
            # set empty tile to tile that was clicked on
            self.tiles[empty_j][empty_i] = self.tiles[tile_j][tile_i]
            # set moved tile to empty
            self.tiles[tile_j][tile_i] = {"index": 24, "tile": "empty"}
            self.move_count += 1

    def get_coords(self, i: int, j: int) -> tuple:
        """Converts (i, j) tile indices to (x, y) coordinates."""
        return i * self.tile_height, j * self.tile_width

    def get_tile_indices(self, x: int, y: int) -> tuple:
        """Converts (x, y) coordinates to (i, j) tile indices."""
        return int(x // (self.tile_width)), int((y-self.header_height) // self.tile_height)

    def is_moveable(self, i: int, j: int) -> bool:
        """Determines if tile is moveable."""
        empty_i, empty_j = self.empty_tile()
        if i + 1 == empty_i and j == empty_j:
            return True
        elif i - 1 == empty_i and j == empty_j:
            return True
        elif i == empty_i and j + 1 == empty_j:
            return True
        elif i == empty_i and j - 1 == empty_j:
            return True
        else:
            return False

    def move_count_text(self) -> None:
        text_move_count = self.game_font.render(f"Moves: {self.move_count}", True, (0, 125, 255))
        self.screen.blit(text_move_count, (450, 12))

    def victory_text(self) -> None:
        text = self.game_font.render("You solved the puzzle!", True, (0, 125, 255))
        self.screen.blit(text, (180, 12))


if __name__ == "__main__":
    Puzzle()
