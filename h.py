import pygame
from pyvidplayer import Video

pygame.init()
pygame.mixer.init()

screen_w = 950
screen_h = 650

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Infinity Maze")
font = pygame.font.Font("VT323-Regular.ttf", 40)

image = pygame.image.load('Main_bckgrd.png')
menu_background = pygame.image.load('Menu_bckgd.png')

pygame.mixer.music.load('battle-of-the-dragons-8037.mp3')
pygame.mixer.music.play(-1)

button_sound = pygame.mixer.Sound('click_effect-86995.mp3')

volume = 0.5
sound_effects_enabled = True

def set_volume(vol):
    pygame.mixer.music.set_volume(vol)
    button_sound.set_volume(vol)

set_volume(volume)

def background_maze(image):
    size = pygame.transform.scale(image, (950, 650))
    screen.blit(size, (0, 0))

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

button_surface = pygame.image.load("iButton.png")
button_surface = pygame.transform.scale(button_surface, (180, 70))

start_button = Button(475, 420, button_surface, "START")
exit_button = Button(475, 500, button_surface, "EXIT")
back_button = Button(475, 540, button_surface, "Back")

exit_button_inthegame = Button(250, 550, button_surface, "EXIT")
restart_game = Button(700, 550, button_surface, "RESTART")
resume_game  = Button(475, 550, button_surface, "RESUME")

menu_button_surface = pygame.image.load("menu_button.png")
menu_button_surface = pygame.transform.scale(menu_button_surface, (40, 40)) 
menu_button = Button(screen_w - 50, 600, menu_button_surface)

slider_bg_color = (50, 50, 50)
slider_border_color = (200, 200, 200)
slider_handle_color = (255, 100, 100)
slider_border_width = 2

slider_rect = pygame.Rect(screen_w // 2 - 90, 113, 300, 20)
handle_rect = pygame.Rect(screen_w // 2 - 5, 113 - 10, 20, 40)

toggle_width, toggle_height = 80, 25
toggle_rect = pygame.Rect(screen_w // 2 - toggle_width // 2, 170, toggle_width, toggle_height)
toggle_border_color = (200, 200, 200)
toggle_on_color = (0, 255, 0)
toggle_off_color = (255, 0, 0)
toggle_handle_color = (255, 255, 255)

# Load images for toggle ON and OFF states
toggle_on_image = pygame.image.load("on.png")  # Replace with the actual image path
toggle_off_image = pygame.image.load("off.png")  # Replace with the actual image path

# Rescale the images to fit the toggle size
toggle_on_image = pygame.transform.scale(toggle_on_image, (toggle_width, toggle_height))
toggle_off_image = pygame.transform.scale(toggle_off_image, (toggle_width, toggle_height))

MAIN_MENU = "main_menu"
INTRO = "intro"
GAME = "game"
Menu = "Options"
inthegame = "menu_inthegame"
QUIT = "quit"

current_state = MAIN_MENU
video_played = False 

def intro():
    global video_played

    pygame.mixer.music.pause()

    VID = Video("StoryTelling.mp4")
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
                    return GAME  # Skip to the game screen

    # Resume the game music
    pygame.mixer.music.unpause()

    video_played = True
    return GAME

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

    # Draw the toggle image based on the sound effect status
    toggle_image = toggle_on_image if sound_effects_enabled else toggle_off_image
    screen.blit(toggle_image, (toggle_rect.x, toggle_rect.y))

    toggle_text = "Sound ON :" if sound_effects_enabled else "Sound OFF :"
    text_surface = font.render(toggle_text, True, (255, 255, 255))
    screen.blit(text_surface, (250, 125 + toggle_height + 10))

    back_button.update()
    back_button.change_color(pygame.mouse.get_pos())

def menu_inthegame():
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

    # Draw the toggle image based on the sound effect status
    toggle_image = toggle_on_image if sound_effects_enabled else toggle_off_image
    screen.blit(toggle_image, (toggle_rect.x, toggle_rect.y))

    toggle_text = "Sound ON :" if sound_effects_enabled else "Sound OFF :"
    text_surface = font.render(toggle_text, True, (255, 255, 255))
    screen.blit(text_surface, (250, 125 + toggle_height + 10))

    exit_button_inthegame.update()
    exit_button_inthegame.change_color(pygame.mouse.get_pos())

    restart_game.update()
    restart_game.change_color(pygame.mouse.get_pos())

    resume_game.update()
    resume_game.change_color(pygame.mouse.get_pos())

def game_screen():
    screen.fill((52, 78, 91))
    game_text = font.render("Game Screen", True, "white")
    screen.blit(game_text, (screen_w // 2 - game_text.get_width() // 2, screen_h // 2))

    menu_button.update()
    menu_button.change_color(pygame.mouse.get_pos())

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == MAIN_MENU:
                if start_button.check_for_input(pygame.mouse.get_pos()):
                    current_state = INTRO if not video_played else GAME
                if exit_button.check_for_input(pygame.mouse.get_pos()):
                    run = False
                if menu_button.check_for_input(pygame.mouse.get_pos()):
                    current_state = Menu
            elif current_state == GAME:
                if menu_button.check_for_input(pygame.mouse.get_pos()):
                    current_state = inthegame
            elif current_state == Menu:
                if back_button.check_for_input(pygame.mouse.get_pos()):
                    current_state = MAIN_MENU
                if slider_rect.collidepoint(pygame.mouse.get_pos()):
                    handle_rect.x = pygame.mouse.get_pos()[0] - handle_rect.width // 2
                    volume = (handle_rect.x - slider_rect.x) / (slider_rect.width - handle_rect.width)
                    set_volume(volume)
                if toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    sound_effects_enabled = not sound_effects_enabled
                    if sound_effects_enabled:
                        button_sound.play()  # Play the sound when the toggle is clicked
            elif current_state == inthegame:
                if slider_rect.collidepoint(pygame.mouse.get_pos()):
                    handle_rect.x = pygame.mouse.get_pos()[0] - handle_rect.width // 2
                    volume = (handle_rect.x - slider_rect.x) / (slider_rect.width - handle_rect.width)
                    set_volume(volume)
                if toggle_rect.collidepoint(pygame.mouse.get_pos()):
                    sound_effects_enabled = not sound_effects_enabled
                    if sound_effects_enabled:
                        button_sound.play()
                if exit_button_inthegame.check_for_input(pygame.mouse.get_pos()):
                    run = False
                if resume_game.check_for_input(pygame.mouse.get_pos()):
                    current_state = GAME
                if restart_game.check_for_input(pygame.mouse.get_pos()):
                    current_state = MAIN_MENU  # Restart the game to the main menu
            else:
                pass

        elif event.type == pygame.MOUSEBUTTONUP:
            if current_state == Menu and slider_rect.collidepoint(pygame.mouse.get_pos()):
                handle_rect.x = pygame.mouse.get_pos()[0] - handle_rect.width // 2
                volume = (handle_rect.x - slider_rect.x) / (slider_rect.width - handle_rect.width)
                set_volume(volume)

    if current_state == MAIN_MENU:
        main_menu()
    elif current_state == INTRO:
        current_state = intro()
    elif current_state == GAME:
        game_screen()
    elif current_state == Menu:
        menu()
    elif current_state == inthegame:
        menu_inthegame()

    pygame.display.update()

pygame.quit() 