import pygame
import sys

# Initialize Pygame
pygame.init()


SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Box Movement with Exit")


WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


box_width, box_height = 50, 50
box_x, box_y = SCREEN_WIDTH // 2, SCREEN_HEIGHT - box_height
velocity = 12


exit_width, exit_height = 60, 60
exit_x, exit_y = SCREEN_WIDTH - exit_width - 10, SCREEN_HEIGHT - exit_height - 10


clock = pygame.time.Clock()

def draw_game():
    # Clear the screen
    screen.fill(WHITE)

    # Draw the player box
    pygame.draw.rect(screen, RED, (box_x, box_y, box_width, box_height))

    # Draw the exit box
    pygame.draw.rect(screen, GREEN, (exit_x, exit_y, exit_width, exit_height))

    # Update the display
    pygame.display.update()

def check_collision():
    # Check if the player's box is within the bounds of the exit box
    if (box_x + box_width > exit_x and box_x < exit_x + exit_width) and \
       (box_y + box_height > exit_y and box_y < exit_y + exit_height):
        return True
    return False

# Main game loop
running = True
while running:
    clock.tick(30)  # Control the frame rate

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Get the keys pressed
    keys = pygame.key.get_pressed()

    # Movement: Left, Right, Up, and Down
    if keys[pygame.K_LEFT] and box_x > 0:
        box_x -= velocity
    if keys[pygame.K_RIGHT] and box_x < SCREEN_WIDTH - box_width:
        box_x += velocity
    if keys[pygame.K_UP] and box_y > 0:
        box_y -= velocity
    if keys[pygame.K_DOWN] and box_y < SCREEN_HEIGHT - box_height:
        box_y += velocity

    # Check if the player reached the exit box
    if check_collision():
        print("Congratulations! You've reached the exit!")
        running = False  # Stop the game loop

    # Redraw the game elements
    draw_game()

# After the loop ends, quit Pygame
pygame.quit()
sys.exit()
