import pygame
import random
import sys

pygame.init()

WIDTH, HEIGHT = 950, 650

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Game")

ROWS, COLS = 17, 25
TILE_WIDTH = WIDTH // COLS
TILE_HEIGHT = HEIGHT // ROWS

WALL_THICKNESS = min(TILE_WIDTH, TILE_HEIGHT) // 4

# Load the wall image and scale it to fit the tile size
wall_image = pygame.image.load('wall.png')  # Replace 'wall.png' with your image file name
wall_image = pygame.transform.scale(wall_image, (TILE_WIDTH - 2 * WALL_THICKNESS, TILE_HEIGHT - 2 * WALL_THICKNESS))

# Function to create a maze using DFS with backtracking
def generate_maze(rows, cols):
    maze = [[1 for _ in range(cols)] for _ in range(rows)]
    start_x, start_y = 0, 0
    maze[start_y][start_x] = 0

    def carve_passages(cx, cy):
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for direction in directions:
            nx, ny = cx + direction[0] * 2, cy + direction[1] * 2
            if 0 <= ny < rows and 0 <= nx < cols and maze[ny][nx] == 1:
                maze[cy + direction[1]][cx + direction[0]] = 0
                maze[ny][nx] = 0
                carve_passages(nx, ny)

    carve_passages(start_x, start_y)

    return maze

# Generate a random maze
maze = generate_maze(ROWS, COLS)

# Function to draw the maze
def draw_maze():
    for y, row in enumerate(maze):
        for x, tile in enumerate(row):
            rect = pygame.Rect(x * TILE_WIDTH + WALL_THICKNESS, y * TILE_HEIGHT + WALL_THICKNESS, TILE_WIDTH - 2 * WALL_THICKNESS, TILE_HEIGHT - 2 * WALL_THICKNESS)
            if tile == 1:
                # Draw the wall image instead of a black rectangle
                screen.blit(wall_image, rect)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill(WHITE)
    
    draw_maze()

    pygame.display.flip()
