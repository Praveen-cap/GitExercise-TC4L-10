import turtle
import random
from PIL import Image
import pygame  # Added for the puzzle window
import math
import sys

# Initialize Pygame for puzzle window handling
pygame.init()

# Setup the main game window
win = turtle.Screen()
win.bgpic("sword_bg.gif")
win.title("Infinite Maze")
win.setup(700, 700)
win.register_shape("wall.img.gif")
win.register_shape("door.maze.gif")
win.register_shape("trap.gif")

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("wall.img.gif")
        self.color("white")
        self.penup()
        self.speed(0)

class MovingBrick(turtle.Turtle):
    def __init__(self, start_pos, move_distance):
        turtle.Turtle.__init__(self)
        self.shape("wall.img.gif")
        self.color("white")
        self.penup()
        self.speed(1)
        self.start_pos = start_pos
        self.move_distance = move_distance
        self.direction = 1  # 1 means moving up, -1 means moving down
        self.goto(start_pos)

    def move(self):
        self.clear()

        # moving vertically
        new_y = self.ycor() + (self.move_distance * self.direction)
        self.goto(self.xcor(), new_y)
        self.direction *= -1  # Reverse the direction for the next move

        # return to its position
        self.stamp()

        # ensuring the player is in position after collision
        if self.distance(player) < 12:
            player.hit_by_wall()

        win.ontimer(self.move, 1000)

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.lives = 3

    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            self.check_position()

    def go_down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            self.check_position()

    def go_left(self):
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            self.check_position()

    def go_right(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            self.check_position()

    def check_position(self):
        if (self.xcor(), self.ycor()) == door_position:
            print("You've reached the door! Game Over.")
            turtle.bye()

        # ensure hits the trap
        if (self.xcor(), self.ycor()) in traps:
            self.hit_by_wall()

        # Puzzle trigger (this triggers the puzzle when the player reaches a specific position)
        if (self.xcor(), self.ycor()) == (some_trigger_position_x, some_trigger_position_y):
            trigger_puzzle()  # Open the puzzle window

    def hit_by_wall(self):
        self.lives -= 1
        print(f"You hit a wall! Lives left: {self.lives}")

        if self.lives > 0:
            self.goto(start_position)
        else:
            print("Game Over! You lost all your lives.")
            turtle.bye()

# Puzzle Handling in Pygame
def create_puzzle_pieces(image_path, rows=3, cols=3):
    img = Image.open(image_path)
    width, height = img.size
    tile_width = width // cols
    tile_height = height // rows
    puzzle_pieces = []

    for row in range(rows):
        for col in range(cols):
            box = (col * tile_width, row * tile_height, (col + 1) * tile_width, (row + 1) * tile_height)
            piece = img.crop(box)
            puzzle_pieces.append(piece)

    return puzzle_pieces

def scramble_pieces(pieces):
    random.shuffle(pieces)
    return pieces

def show_puzzle_window(pieces, rows=3, cols=3):
    # Create a new Pygame window for the puzzle
    puzzle_window_size = 600
    puzzle_window = pygame.display.set_mode((puzzle_window_size, puzzle_window_size))
    pygame.display.set_caption("Solve the Puzzle")

    piece_width = puzzle_window_size // cols
    piece_height = puzzle_window_size // rows

    # Create a surface for each puzzle piece
    piece_surfaces = []
    for piece in pieces:
        mode = piece.mode
        size = piece.size
        data = piece.tobytes()
        pygame_image = pygame.image.fromstring(data, size, mode)
        piece_surfaces.append(pygame.transform.scale(pygame_image, (piece_width, piece_height)))

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Fill the puzzle window with a color (white)
        puzzle_window.fill((255, 255, 255))

        # Draw the scrambled pieces on the puzzle window
        for i, surface in enumerate(piece_surfaces):
            row = i // cols
            col = i % cols
            x = col * piece_width
            y = row * piece_height
            puzzle_window.blit(surface, (x, y))

        pygame.display.update()

    pygame.quit()
    sys.exit()

def trigger_puzzle():
    pieces = create_puzzle_pieces("dragon vettai ku whistle podu .jpg", 3, 3)
    scrambled_pieces = scramble_pieces(pieces)
    show_puzzle_window(scrambled_pieces)

# Maze setup and game logic
levels = [""]

level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP XXXXXXX          XXXXX",
    "X  XXXXXXX  XXXXXX  XXXXX",
    "X       XX  XXXXXX  XXXXX",
    "X       XX  XXX        XX",
    "X XXXX  XX  XXX        XX",
    "XMXXXX  XX  XXXXXX  XXXXX",
    "XXXXXX  XX    XXXX  XXXXX",
    "X  XXX   M    XXXX  XXXXX",
    "X  XXX TXXXXXXXXXXXXXXXXX",
    "X         XXXXXXXXXXXXXXX",
    "X                XXXXXXXX",
    "XXXXXXXXXXTTT    XXXXX  X",
    "XXXXXXXXXXXXX   TXXXXX  X",
    "XXX  XXXXXXXX     T     X",
    "XXX                     X",
    "XXX          XXXXXXXXXXXX",
    "XXXXXXXXXX   XXXXXXXXXXXX",
    "XXXXXXXXXX              X",
    "XX    XXXXTTT           X",
    "XX    XXXXXXXXXXXX  TXXXX",
    "X             XXXX   XXXX",      
    "X                M   XXXX",
    "XXXXXXXXXXXXXX  XX   XXXX",
    "XXXXXXXXXXXXXXXXXXXX  MXX",
    "XXXXXXXXXXXXXXXXXXXXXT  D"
]
# P=player
# D=door
# T=traps
# M=brick movement

levels.append(level_1)

def setup_maze(level):
    global door_position
    global start_position

    win.tracer(0)

    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]

            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("wall.img.gif")
                pen.stamp()
                walls.append((screen_x, screen_y))

            if character == "P":
                player.goto(screen_x, screen_y)
                start_position = (screen_x, screen_y)

            if character == "D":
                pen.goto(screen_x, screen_y)
                pen.shape("door.maze.gif")
                pen.stamp()
                door_position = (screen_x, screen_y)
                
            if character == "T":
                pen.goto(screen_x, screen_y)
                pen.shape("trap.gif")
                pen.stamp()
                traps.append((screen_x, screen_y))
                
            if character == "M":
                moving_brick = MovingBrick((screen_x, screen_y), 24)
                moving_bricks.append(moving_brick)
                moving_brick.stamp()  
                moving_brick.move()

    win.tracer(1)

pen = Pen()
player = Player()

walls = []
traps = []
moving_bricks = []
door_position = None
start_position = None

turtle.done()