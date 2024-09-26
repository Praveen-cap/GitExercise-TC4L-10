import pygame
import random
import time


class PuzzleGame:
    def __init__(self, image_path):
        self.screen_w = 950
        self.screen_h = 650
        self.win = pygame.display.set_mode((self.screen_w, self.screen_h))
        pygame.display.set_caption('Time for Puzzle')

        self.WHITE = (255, 255, 255)
        self.GREEN = (0, 255, 0)
        self.RED = (255, 0, 0)
        self.GRAY = (169, 169, 169)
        self.BLACK = (0, 0, 0)

        # Load and scale the image to fit within the puzzle grid dimensions
        print(f"Loading image: {image_path}")
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (self.screen_w, self.screen_h))

        self.ROWS, self.COLS = 4, 4
        self.TILE_SIZE_W = self.image.get_width() // self.COLS
        self.TILE_SIZE_H = self.image.get_height() // self.ROWS

        # Puzzle settings
        self.tiles = []
        self.rotations = []
        self.create_tiles()

        # Randomly rotate each tile
        self.randomize_rotations()

        # Timer settings
        self.time_limit = 20
        self.start_time = None
        self.paused_time = 0  # Track the total time spent paused
        self.running = True
        self.paused = False  # New variable to track pause state
        self.playing = False  # Track if the game has started

        # Button dimensions
        self.button_width = 120
        self.button_height = 50
        print("Puzzle initialized.")

    def create_tiles(self):
        print("Creating tiles...")
        for row in range(self.ROWS):
            row_tiles = []
            for col in range(self.COLS):
                tile = self.image.subsurface(
                    pygame.Rect(col * self.TILE_SIZE_W, row * self.TILE_SIZE_H, self.TILE_SIZE_W, self.TILE_SIZE_H)
                )
                row_tiles.append(tile)
                self.rotations.append(0)
            self.tiles.append(row_tiles)
        print("Tiles created.")

    def randomize_rotations(self):
        print("Randomizing tile rotations...")
        for i in range(self.ROWS * self.COLS):
            self.rotations[i] = random.choice([0, 90, 180, 270])
        print(f"Rotations after randomization: {self.rotations}")

    def rotate_tile(self, tile_index):
        print(f"Rotating tile {tile_index}")
        self.rotations[tile_index] = (self.rotations[tile_index] + 90) % 360

    def is_solved(self):
        solved = all(rotation == 0 for rotation in self.rotations)
        print(f"Puzzle solved: {solved}")
        return solved

    def draw_puzzle(self):
        self.win.fill(self.WHITE)
        for i in range(self.ROWS * self.COLS):
            row, col = i // self.COLS, i % self.COLS
            rotated_tile = pygame.transform.rotate(self.tiles[row][col], self.rotations[i])
            self.win.blit(rotated_tile, (col * self.TILE_SIZE_W, row * self.TILE_SIZE_H))

        # Display timer
        if self.playing:
            self.draw_timer()

        # Draw buttons
        if self.paused:
            self.draw_pause_menu()
        pygame.display.update()

    def draw_timer(self):
        font = pygame.font.Font(None, 36)
        elapsed_time = self.get_elapsed_time()
        time_left = max(0, self.time_limit - int(elapsed_time))
        color = self.RED if time_left <= 10 else self.GREEN
        timer_text = font.render(f"Time left: {time_left}s", True, color)
        self.win.blit(timer_text, (10, 10))

    def draw_solved_message(self):
        print("Displaying solved message.")
        font = pygame.font.Font(None, 36)
        text = font.render("Puzzle Solved!", True, self.GREEN)
        text_rect = text.get_rect(center=(self.screen_w // 2, self.screen_h // 2))
        self.win.blit(text, text_rect)
        pygame.display.update()

    def draw_time_up_message(self):
        print("Displaying time up message.")
        font = pygame.font.Font(None, 36)
        text = font.render("Time's Up! You lost.", True, self.RED)
        text_rect = text.get_rect(center=(self.screen_w // 2, self.screen_h // 2))
        self.win.blit(text, text_rect)
        pygame.display.update()

    def handle_mouse_click(self, pos):
        if self.playing and not self.paused:
            tile_index = (pos[1] // self.TILE_SIZE_H) * self.COLS + (pos[0] // self.TILE_SIZE_W)
            print(f"Tile clicked: {tile_index}")
            self.rotate_tile(tile_index)

    def blur_surface(self, surface):
        scale_down = pygame.transform.smoothscale(surface, (self.screen_w // 20, self.screen_h // 20))
        return pygame.transform.smoothscale(scale_down, (self.screen_w, self.screen_h))

    def draw_pause_menu(self):
        print("Drawing pause menu.")
        # Create a surface for the blurred background
        blur_surface = pygame.Surface((self.screen_w, self.screen_h))
        blur_surface.set_alpha(128)  # Semi-transparent
        blur_surface.fill(self.GRAY)
        self.win.blit(blur_surface, (0, 0))

        font = pygame.font.Font(None, 36)

        # Resume Button
        resume_text = font.render("Resume", True, self.WHITE)
        resume_button = pygame.Rect(self.screen_w // 2 - 60, self.screen_h // 2 - 40, 120, 50)
        pygame.draw.rect(self.win, self.GREEN, resume_button)
        self.win.blit(resume_text, resume_text.get_rect(center=resume_button.center))

        # Restart Button
        restart_text = font.render("Restart", True, self.WHITE)
        restart_button = pygame.Rect(self.screen_w // 2 - 60, self.screen_h // 2 + 10, 120, 50)
        pygame.draw.rect(self.win, self.GREEN, restart_button)
        self.win.blit(restart_text, restart_text.get_rect(center=restart_button.center))

        # Exit Button
        exit_text = font.render("Exit", True, self.WHITE)
        exit_button = pygame.Rect(self.screen_w // 2 - 60, self.screen_h // 2 + 60, 120, 50)
        pygame.draw.rect(self.win, self.GREEN, exit_button)
        self.win.blit(exit_text, exit_text.get_rect(center=exit_button.center))

        pygame.display.update()
        return resume_button, restart_button, exit_button

    def get_elapsed_time(self):
        """Returns the elapsed time excluding the paused duration."""
        if self.start_time is None:
            return 0
        if self.paused:
            return self.pause_start_time - self.start_time - self.paused_time
        else:
            return time.time() - self.start_time - self.paused_time

    def run(self):
        pygame.init()
        clock = pygame.time.Clock()

        # Start the timer
        self.start_time = time.time()
        self.playing = True
        print("Game started.")

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    print("Game quit.")

                elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                    self.paused = not self.paused  # Toggle pause when 'P' is pressed
                    print(f"Game paused: {self.paused}")
                    if self.paused:
                        self.pause_start_time = time.time()  # Save when pause started
                    else:
                        self.paused_time += time.time() - self.pause_start_time  # Add paused duration

                elif event.type == pygame.MOUSEBUTTONDOWN and self.paused:
                    pos = pygame.mouse.get_pos()
                    resume_button, restart_button, exit_button = self.draw_pause_menu()
                    pygame.display.update()  # Ensure buttons are shown during pause

                    if resume_button.collidepoint(pos):
                        print("Resuming game.")
                        self.paused = False
                        self.start_time = time.time() - self.paused_time  # Resume timer
                    elif restart_button.collidepoint(pos):
                        print("Restarting game.")
                        self.__init__('Main_Bckgrd.png')  # Restart the game with correct image path
                    elif exit_button.collidepoint(pos):
                        print("Exiting game.")
                        self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN and not self.paused:
                    pos = pygame.mouse.get_pos()
                    if self.playing:
                        self.handle_mouse_click(pos)

            if self.playing and not self.paused:
                if self.is_solved():
                    self.draw_solved_message()
                    pygame.time.delay(2000)
                    self.running = False
                    print("Puzzle solved, exiting game.")
                
                elapsed_time = self.get_elapsed_time()
                if elapsed_time >= self.time_limit:
                    self.draw_time_up_message()
                    pygame.time.delay(2000)
                    self.running = False
                    print("Time up, exiting game.")

            self.draw_puzzle()

            clock.tick(60)

        pygame.quit()
        print("Game closed.")
