import pygame
import random
import time

class PuzzleGame:
    def __init__(self, image_path):
        pygame.init()

        self.WIN_WIDTH, self.WIN_HEIGHT = 700, 700
        self.win = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        pygame.display.set_caption('Time for Puzzle')

        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)

        self.solved = False

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.WIN_WIDTH, self.WIN_HEIGHT))

        self.TILE_SIZE = self.WIN_WIDTH // 4
        self.ROWS, self.COLS = 4, 4

        # Puzzle settings
        self.tiles = []
        self.rotations = []
        self.create_tiles()

        # Randomly rotate each tile
        self.randomize_rotations()

        # Timer settings
        self.time_limit = 20 
        self.start_time = time.time()

    def create_tiles(self):
        if self.image.get_width() < self.WIN_WIDTH or self.image.get_height() < self.WIN_HEIGHT:
            print("Error: Image is too small to create tiles.")
            return

        for row in range(self.ROWS):
            row_tiles = []
            for col in range(self.COLS):
                tile = self.image.subsurface(col * self.TILE_SIZE, row * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                row_tiles.append(tile)
                self.rotations.append(0)  # No rotation initially

            self.tiles.append(row_tiles)

    def randomize_rotations(self):
        for i in range(self.ROWS * self.COLS):
            if self.rotations[i] == 0:
                self.rotations[i] = random.choice([0, 90, 180, 270])

    def rotate_tile(self, i):
        self.rotations[i] = (self.rotations[i] + 90) % 360

    def is_solved(self):
        return all(rotation == 0 for rotation in self.rotations)

    def draw_puzzle(self):
        self.win.fill(self.WHITE)
        for i in range(self.ROWS * self.COLS):
            row, col = i // self.COLS, i % self.COLS
            rotated_tile = pygame.transform.rotate(self.tiles[row][col], self.rotations[i])
            rect = rotated_tile.get_rect(center=(col * self.TILE_SIZE + self.TILE_SIZE // 2, row * self.TILE_SIZE + self.TILE_SIZE // 2))
            self.win.blit(rotated_tile, rect)

        # Display timer
        self.draw_timer()

        pygame.display.update()

    def draw_timer(self):
        font = pygame.font.Font(None, 36)
        elapsed_time = time.time() - self.start_time
        time_left = max(0, self.time_limit - int(elapsed_time))  # Prevent negative time display
        color = self.RED if time_left <= 10 else self.GREEN  # Red for last 10 seconds
        timer_text = font.render(f"Time left: {time_left}s", True, color)
        self.win.blit(timer_text, (10, 10))

    def draw_solved_message(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Puzzle Solved!", True, self.GREEN)
        text_rect = text.get_rect(center=(self.WIN_WIDTH // 2, self.WIN_HEIGHT // 2))
        self.win.blit(text, text_rect)
        pygame.display.update()

    def draw_time_up_message(self):
        font = pygame.font.Font(None, 36)
        text = font.render("Time's Up! You lost.", True, self.RED)
        text_rect = text.get_rect(center=(self.WIN_WIDTH // 2, self.WIN_HEIGHT // 2))
        self.win.blit(text, text_rect)
        pygame.display.update()

    def handle_mouse_click(self, pos):
        tile_index = (pos[1] // self.TILE_SIZE) * self.COLS + (pos[0] // self.TILE_SIZE)
        self.rotate_tile(tile_index)

    def main(self):
        run = True
        clock = pygame.time.Clock()
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                if event.type == pygame.MOUSEBUTTONDOWN and not self.is_solved():
                    self.handle_mouse_click(event.pos)
                    self.draw_puzzle()

            self.draw_puzzle()

            # If the puzzle is solved, display the solved message and quit
            if self.is_solved():
                self.draw_solved_message()
                pygame.time.wait(1000)
                self.solved = True  # Set solved to True
                run = False

            if time.time() - self.start_time >= self.time_limit:
                self.draw_time_up_message()
                pygame.time.wait(2000)
                run = False

            clock.tick(60)
        
        pygame.quit()

    def was_solved(self):
        return self.solved

if __name__ == "__main__":
    game = PuzzleGame("dragon.jpg")  # Replace with the actual image path
    game.main()