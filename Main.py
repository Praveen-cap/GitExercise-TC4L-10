import pygame

pygame.init()
pygame.mixer.init()

screen_w = 950
screen_h = 650

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Infinity Maze")
font = pygame.font.Font("VT323-Regular.ttf", 40)

image = pygame.image.load('Infinity Maze.png')

pygame.mixer.music.load('cinematic.mp3')
pygame.mixer.music.play(-1)

button_sound = pygame.mixer.Sound('click_effect-86995.mp3')

def background_maze(image):
    size = pygame.transform.scale(image, (950, 650))
    screen.blit(size, (0, 0))


class button():
    def __init__(self, x, y, image, text_input):
        self.image = image
        self.x = x
        self.y = y
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.text_input = text_input
        self.text = font.render(self.text_input, True, "red")
        self.text_rect = self.text.get_rect(center=(self.x, self.y))
    
    def update(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkforinput(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            button_sound.play()
            return True
        return False

    def changecolour(self, position):
        if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
            self.text = font.render(self.text_input, True, "green")
        else:
            self.text = font.render(self.text_input, True, "red")

Button_surface = pygame.image.load("iButton.png")
Button_surface = pygame.transform.scale(Button_surface, (180, 70))

Start_Button = button(475, 420, Button_surface, "START")
Exit_Button = button(475, 500, Button_surface, "EXIT")    

MAIN_MENU = "main_menu"
GAME = "game"
QUIT = "quit"

current_state = MAIN_MENU

def main_menu():
    screen.fill((52,78, 91))
    background_maze(image)

    Start_Button.update()
    Start_Button.changecolour(pygame.mouse.get_pos())

    Exit_Button.update()
    Exit_Button.changecolour(pygame.mouse.get_pos())

def game_screen():
    screen.fill((52,78, 91))
    game_text = font.render("Game Screen", True, "white")
    screen.blit(game_text, (screen_w // 2 - game_text.get_width() // 2, screen_h // 2))

run = True
while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if current_state == MAIN_MENU:
                if Start_Button.checkforinput(pygame.mouse.get_pos()):
                    current_state = GAME
                if Exit_Button.checkforinput(pygame.mouse.get_pos()):
                    run = False

    if current_state == MAIN_MENU:
        main_menu()
    elif current_state == GAME:
        game_screen()

    pygame.display.update()
pygame.quit()
