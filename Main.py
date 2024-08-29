import pygame
import button


pygame.init()

screen_w = 950
screen_h = 650

screen = pygame.display.set_mode((screen_w, screen_h))
pygame.display.set_caption("Main Menu")

game_paused = False


font = pygame.font.SysFont("arialblack", 40)
text_colour = (255, 255, 255)

resume_img = pygame.image.load("")

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img,(x, y))

run = True
while run:

    screen.fill((52, 78, 91))

    if game_paused == True:
        pass
    else:
        draw_text("Press SPACE to pause", font, text_colour, 220, 295)


    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
               game_paused = True 
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()
pygame.quit()   