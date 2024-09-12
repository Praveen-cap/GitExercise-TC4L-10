import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLOCK_SIZE = 20

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Set up display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Maze Game')

# Clock
clock = pygame.time.Clock()

# Maze generation
def generate_maze():
    maze = [[random.choice([0, 1]) for _ in range(SCREEN_WIDTH // BLOCK_SIZE)] for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    maze[0][0] = 0  # Start
    maze[-1][-1] = 0  # End
    return maze

# Draw maze
def draw_maze(maze):
    for y in range(len(maze)):
        for x in range(len(maze[y])):
            color = WHITE if maze[y][x] == 0 else BLACK
            pygame.draw.rect(screen, color, pygame.Rect(x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Draw power-ups
def draw_power_ups(power_ups):
    for px, py in power_ups:
        pygame.draw.rect(screen, GREEN, pygame.Rect(px * BLOCK_SIZE, py * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Draw player
def draw_player(px, py):
    pygame.draw.rect(screen, BLUE, pygame.Rect(px * BLOCK_SIZE, py * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Draw door
def draw_door(dx, dy):
    pygame.draw.rect(screen, RED, pygame.Rect(dx * BLOCK_SIZE, dy * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))

# Main game loop
def main():
    maze = generate_maze()
    player_x, player_y = 1, 1
    door_x, door_y = len(maze[0]) - 2, len(maze) - 2
    power_ups = [(random.randint(1, len(maze[0])-2), random.randint(1, len(maze)-2)) for _ in range(5)]
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= 1
        if keys[pygame.K_RIGHT] and player_x < len(maze[0]) - 1:
            player_x += 1
        if keys[pygame.K_UP] and player_y > 0:
            player_y -= 1
        if keys[pygame.K_DOWN] and player_y < len(maze) - 1:
            player_y += 1

        # Check for collisions
        if maze[player_y][player_x] == 1:
            # If collision, reset position
            player_x, player_y = 1, 1
        if (player_x, player_y) in power_ups:
            power_ups.remove((player_x, player_y))
        if player_x == door_x and player_y == door_y:
            print("You reached the door! Game Over!")
            running = False

        # Fill screen with white
        screen.fill(WHITE)

        # Draw maze, player, power-ups, and door
        draw_maze(maze)
        draw_power_ups(power_ups)
        draw_player(player_x, player_y)
        draw_door(door_x, door_y)

        # Update display
        pygame.display.flip()

        # Limit frames per second
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
