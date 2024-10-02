import pygame
import os
import time
from pyvidplayer import Video

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen dimensions and setup
screen_w = 950
screen_h = 650
screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Infinity Maze")
font = pygame.font.Font("VT323-Regular.ttf", 40)

# Load images and sounds
image = pygame.image.load('Main_bckgrd.png')
menu_background = pygame.image.load('Menu_bckgd.png')
level_bckgrd = pygame.image.load("level bck.jpeg")

pygame.mixer.music.load('battle-of-the-dragons-8037.mp3')
pygame.mixer.music.play(-1)
button_sound = pygame.mixer.Sound('click_effect-86995.mp3')

# Initial settings
volume = 0.5
sound_effects_enabled = True
def set_volume(vol):
    pygame.mixer.music.set_volume(vol)
    button_sound.set_volume(vol)

set_volume(volume)

# Background function
def background_maze(image):
    size = pygame.transform.scale(image, (950, 650))
    screen.blit(size, (0, 0))

# Button class
class Button:
    def __init__(self, x, y, image, text_input=None):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_input = text_input
        if self.text_input:
            self.text = font.render(self.text_input, True, "black")
            self.text_rect = self.text.get_rect(center=(self.x, self.y))
        else:
            self.text = None
    
    def update(self):
        screen.blit(self.image, self.rect)
        if self.text:
            screen.blit(self.text, self.text_rect)

    def check_for_input(self, position):
        if self.rect.collidepoint(position):
            if sound_effects_enabled:
                button_sound.play()
            return True
        return False

    def change_color(self, position):
        if self.rect.collidepoint(position):
            if self.text:
                self.text = font.render(self.text_input, True, "blue")
        else:
            if self.text:
                self.text = font.render(self.text_input, True, "black")

# Button images and creation
button_surface = pygame.image.load("iButton.png")
button_surface = pygame.transform.scale(button_surface, (180, 70))

start_button = Button(475, 420, button_surface, "START")
exit_button = Button(475, 500, button_surface, "EXIT")
back_button = Button(475, 540, button_surface, "Back")

menu_button_surface = pygame.image.load("menu_button.png")
menu_button_surface = pygame.transform.scale(menu_button_surface, (40, 40)) 
menu_button = Button(screen_w - 50, 600, menu_button_surface)

# Level button creation
level_button_surface = pygame.transform.scale(button_surface, (200, 80))
level1_button = Button(475, 200, level_button_surface, "Level 1")
level2_button = Button(475, 300, level_button_surface, "Level 2")
level3_button = Button(475, 400, level_button_surface, "Level 3")
level4_button = Button(475, 500, level_button_surface, "Level 4")

# Slider and toggle setup
slider_bg_color = (50, 50, 50)
slider_border_color = (200, 200, 200)
slider_handle_color = (255, 100, 100)
slider_border_width = 2

slider_rect = pygame.Rect(screen_w // 2 - 90, 113, 300, 20)
handle_rect = pygame.Rect(screen_w // 2 - 5, 113 - 10, 20, 40)

toggle_width, toggle_height = 80, 25
toggle_rect = pygame.Rect(screen_w // 2 - toggle_width // 2, 170, toggle_width, toggle_height)
toggle_on_image = pygame.image.load("on.png")
toggle_off_image = pygame.image.load("off.png")

# Rescale toggle images
toggle_on_image = pygame.transform.scale(toggle_on_image, (toggle_width, toggle_height))
toggle_off_image = pygame.transform.scale(toggle_off_image, (toggle_width, toggle_height))

# Game states
MAIN_MENU = "main_menu"
INTRO = "intro"
GAME = "game"
Menu = "Options"
QUIT = "quit"
LEVELS = "levels"
LEVEL_1 = "level_1"
LEVEL_2 = "level_2"
LEVEL_3 = "level_3"
LEVEL_4 = "level_4"

current_state = MAIN_MENU
previous_state = None
current_level = None

def intro():
    global video_played
    pygame.mixer.music.pause()
    VID = Video("Intro.mp4")
    VID.set_size((950, 650))
    VID.restart()
    skip_key = pygame.K_RIGHT  

    while VID.active:
        VID.draw(screen, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                VID.close()
                return QUIT
            if event.type == pygame.KEYDOWN:
                if event.key == skip_key:
                    VID.close()
                    pygame.mixer.music.unpause()
                    return LEVELS  

    pygame.mixer.music.unpause()
    video_played = True
    return LEVELS

def main_menu():
    screen.fill((52, 78, 91))
    background_maze(image)

    start_button.update()
    start_button.change_color(pygame.mouse.get_pos())

    exit_button.update()
    exit_button.change_color(pygame.mouse.get_pos())

    menu_button.update()
    menu_button.change_color(pygame.mouse.get_pos())

def menu():
    screen.fill((52, 78, 91))
    background_maze(menu_background)

    instruction_text = [
        "INSTRUCTIONS:",
        "Use Arrow Keys to move the player",
        "Press SPACE to jump",
        "Press Right Arrow to skip the video",
        "Objective: Defeat the monsters & escape the maze",
    ]
    for i, line in enumerate(instruction_text):
        text_surface = font.render(line, True, (255, 255, 0))
        screen.blit(text_surface, (screen_w // 2 - text_surface.get_width() // 2, 225 + i * 45))

    volume_label = font.render("Volume:", True, (255, 255, 255))
    screen.blit(volume_label, (250, 100))

    pygame.draw.rect(screen, slider_bg_color, slider_rect)
    pygame.draw.rect(screen, slider_border_color, slider_rect, slider_border_width)
    handle_rect.x = slider_rect.x + int(volume * (slider_rect.width - handle_rect.width))
    pygame.draw.rect(screen, slider_handle_color, handle_rect)

    toggle_image = toggle_on_image if sound_effects_enabled else toggle_off_image
    screen.blit(toggle_image, (toggle_rect.x, toggle_rect.y))

    toggle_text = "Sound ON :" if sound_effects_enabled else "Sound OFF :"
    text_surface = font.render(toggle_text, True, (255, 255, 255))
    screen.blit(text_surface, (250, 125 + toggle_height + 10))

    back_button.update()
    back_button.change_color(pygame.mouse.get_pos())

def levels_screen():
    screen.fill((52, 78, 91))
    background_maze(level_bckgrd)

    level1_button.update()
    level1_button.change_color(pygame.mouse.get_pos())

    level2_button.update()
    level2_button.change_color(pygame.mouse.get_pos())

    level3_button.update()
    level3_button.change_color(pygame.mouse.get_pos())

    level4_button.update()
    level4_button.change_color(pygame.mouse.get_pos())

    menu_button.update()
    menu_button.change_color(pygame.mouse.get_pos())

def handle_level_selection():
    global current_state, current_level
    if level1_button.check_for_input(pygame.mouse.get_pos()):
        current_level = LEVEL_1
        current_state = GAME
    if level2_button.check_for_input(pygame.mouse.get_pos()):
        current_level = LEVEL_2
        current_state = GAME
    if level3_button.check_for_input(pygame.mouse.get_pos()):
        current_level = LEVEL_3
        current_state = GAME
    if level4_button.check_for_input(pygame.mouse.get_pos()):
        current_level = LEVEL_4
        current_state = GAME
def game_screen():
    global current_level, current_state
    if current_level is None:
        return

    if current_level == LEVEL_1:
        import Maze1
        game_completed = Maze1.maze1_main()
        if game_completed:
            current_level = None
            current_state = LEVELS
            return True  # Return True to indicate that the level is completed

    if current_level == LEVEL_2:
        import maze2
        game_completed = maze2.maze2_main()
        if game_completed:
            current_level = None
            current_state = LEVELS
            return True  # Return True to indicate that the level is completed

    if current_level == LEVEL_3:
        import MAZE3
        game_completed = MAZE3.maze3_main()
        if game_completed:
            current_level = None
            current_state = LEVELS
            return True  # Return True to indicate that the level is completed

    if current_level == LEVEL_4:
        import Maze4
        game_completed = Maze4.maze4_main()
        if game_completed:
            current_level = None
            current_state = LEVELS
            return True  # Return True to indicate that the level is completed
    
    if game_completed:
        current_level = None
        current_state = LEVELS

    return GAME
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame. QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == MAIN_MENU:
                if start_button.check_for_input(pygame.mouse.get_pos()):
                    current_state = INTRO 
                if exit_button.check_for_input(pygame.mouse.get_pos()):
                    run = False
                if menu_button.check_for_input(pygame.mouse.get_pos()):
                    current_state = Menu
                    previous_state = MAIN_MENU

            elif current_state == LEVELS:
                handle_level_selection()
                if menu_button.check_for_input(pygame.mouse.get_pos()):
                    current_state = Menu
                    previous_state = LEVELS

            elif current_state == GAME:
                next_state = game_screen()
                if next_state == LEVELS:
                    current_state = LEVELS

            elif current_state == Menu:
                if back_button.check_for_input(pygame.mouse.get_pos()):
                    current_state = previous_state
                if slider_rect.collidepoint(pygame.mouse.get_pos()):
                    handle_rect.x = pygame.mouse.get_pos()[0] - handle_rect.width // 2
                    volume = (handle_rect.x - slider_rect.x) / (slider_rect.width - handle_rect.width)
                    set_volume(volume)
                if toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    sound_effects_enabled = not sound_effects_enabled
                    if sound_effects_enabled:
                        button_sound.play()

        elif event.type == pygame.MOUSEBUTTONUP:
            if current_state == Menu and slider_rect.collidepoint(pygame.mouse.get_pos()):
                handle_rect.x = pygame.mouse.get_pos()[0] - handle_rect.width // 2
                volume = (handle_rect.x - slider_rect.x) / (slider_rect.width - handle_rect.width)
                set_volume(volume)

    if current_state == MAIN_MENU:
        main_menu()
    elif current_state == INTRO:
        current_state = intro()
    elif current_state == LEVELS:
        levels_screen()
    elif current_state == GAME:
        if current_level is None:
            current_state = LEVELS
        else:
            game_screen()
    elif current_state == Menu:
        menu()

    pygame.display.update()

pygame.quit()