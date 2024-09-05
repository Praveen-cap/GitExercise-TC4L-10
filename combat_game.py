import pygame
import sys
from moviepy.editor import VideoFileClip

def combat_game():
    pygame.init()
    combat_win = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Combat Game")
    
    # Load background image
    bg_image = pygame.image.load("background.jpg")  # Replace with your background image file
    bg_image = pygame.transform.scale(bg_image, (800, 600))
    
    # Create player rectangle
    player_rect = pygame.Rect(100, 500, 50, 50)

    # Load and prepare the video
    video = VideoFileClip("monster-1fight.mp4")  # Replace with your video file
    video_frames = [pygame.image.frombuffer(frame.tobytes(), frame.shape[1::-1], "RGB") for frame in video.iter_frames()]

    # Main loop for combat window
    frame_index = 0
    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        # Draw the background and player rectangle
        combat_win.blit(bg_image, (0, 0))
        pygame.draw.rect(combat_win, (0, 255, 0), player_rect)  # Green player rectangle

        # Display the current video frame at the enemy's position
        enemy_rect = pygame.Rect(600, 500, 50, 50)
        combat_win.blit(pygame.transform.scale(video_frames[frame_index], enemy_rect.size), enemy_rect.topleft)

        # Update frame index and display the frame
        frame_index = (frame_index + 1) % len(video_frames)
        pygame.display.update()
        
        # Control the frame rate to sync with video
        clock.tick(30)  # Adjust to the video frame rate

# Run the combat game
if __name__ == "__main__":
    combat_game()
