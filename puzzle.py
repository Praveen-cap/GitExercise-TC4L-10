import pygame
import random

class PuzzleGame:
    def __init__(self, image_path):

        pygame.init()

    
        self.WIN_WIDTH, self.WIN_HEIGHT = 700, 700
        self.win = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        pygame.display.set_caption('Time for Puzzle')


        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)

        
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.WIN_WIDTH, self.WIN_HEIGHT))


        self.TILE_SIZE = self.WIN_WIDTH // 4  
        self.ROWS, self.COLS = 4, 4

        
        # Initialize pygame
        pygame.init()

        # Window settings
        self.WIN_WIDTH, self.WIN_HEIGHT = 700, 700
        self.win = pygame.display.set_mode((self.WIN_WIDTH, self.WIN_HEIGHT))
        pygame.display.set_caption('Rotation Puzzle')

        # Colors
        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)

        # Load and resize the image
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.WIN_WIDTH, self.WIN_HEIGHT))

        # Puzzle settings
        self.TILE_SIZE = self.WIN_WIDTH // 4  # 4x4 puzzle
        self.ROWS, self.COLS = 4, 4

        # Initialize tiles and rotations
        self.tiles = []
        self.rotations = []
        self.create_tiles()


        

        # Randomly rotate each tile

        self.randomize_rotations()

    def create_tiles(self):
        """Splits the image into tiles and initializes rotations."""
        scale_factor = 2  # 2 because it's adjusted to half of the original size of the dragon picture
        tile_width = self.TILE_SIZE // scale_factor
        tile_height = self.TILE_SIZE // scale_factor

        for row in range(self.ROWS):
            row_tiles = []
            for col in range(self.COLS):
                tile = pygame.transform.scale(self.image.subsurface(col * self.TILE_SIZE, row * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE),(self.TILE_SIZE, self.TILE_SIZE))
                row_tiles.append(tile)
                self.rotations.append(0)  

        for row in range(self.ROWS):
            row_tiles = []
            for col in range(self.COLS):
                tile = self.image.subsurface(col * self.TILE_SIZE, row * self.TILE_SIZE, self.TILE_SIZE, self.TILE_SIZE)
                row_tiles.append(tile)
                self.rotations.append(0)  # No rotation initially

            self.tiles.append(row_tiles)

    def randomize_rotations(self):
        """Randomly rotates each tile."""
        for i in range(self.ROWS * self.COLS):
            self.rotations[i] = random.choice([0, 90, 180, 270])

    def rotate_tile(self, i):
        """Rotates a tile by 90 degrees."""
        self.rotations[i] = (self.rotations[i] + 90) % 360

    def is_solved(self):
        """Checks if the puzzle is solved (all tiles have rotation 0)."""
        return all(rotation == 0 for rotation in self.rotations)

    def draw_puzzle(self):
        """Draws the puzzle with the current tile rotations."""
        self.win.fill(self.WHITE)
        for i in range(self.ROWS * self.COLS):
            row, col = i // self.COLS, i % self.COLS
            rotated_tile = pygame.transform.rotate(self.tiles[row][col], self.rotations[i])
            self.win.blit(rotated_tile, (col * self.TILE_SIZE, row * self.TILE_SIZE))
        pygame.display.update()

    def draw_solved_message(self):
        """Displays a 'Puzzle Solved!' message when the puzzle is solved."""
        font = pygame.font.Font(None, 36)
        text = font.render("Puzzle Solved!", True, self.GREEN)
        text_rect = text.get_rect(center=(self.WIN_WIDTH // 2, self.WIN_HEIGHT // 2))
        self.win.blit(text, text_rect)
        pygame.display.update()

    def handle_mouse_click(self, pos):
        """Handles tile rotation based on mouse click position."""
        tile_index = (pos[1] // self.TILE_SIZE) * self.COLS + (pos[0] // self.TILE_SIZE)
        self.rotate_tile(tile_index)

    def main(self):
        """Main game loop."""
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

                # Rotate tile on mouse click if puzzle isn't solved
                if event.type == pygame.MOUSEBUTTONDOWN and not self.is_solved():
                    self.handle_mouse_click(event.pos)

            self.draw_puzzle()

            # If the puzzle is solved, display the message
            if self.is_solved():
                self.draw_solved_message()

        pygame.quit()


if __name__ == "__main__":

    game = PuzzleGame("dragon vettai ku whistle podu .jpg")  # Replace with your image path
    game.main()

    game = PuzzleGame('dragon vettai ku whistle podu .jpg')  # Replace with your image path
    game.main()

