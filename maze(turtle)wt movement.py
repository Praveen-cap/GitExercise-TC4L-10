import turtle
import pygame
import sys
import time
import os

os.chdir(r"C:\Users\acsia\Mini It Project\GitExercise-TC4L-10\MAZE 1234")

pygame.mixer.init()

# Load background music and sound effects (MP3 format)
pygame.mixer.music.load("background 3.mp3")
pygame.mixer.music.play(loops=-1)

fire_sound = pygame.mixer.Sound("fire.mp3")
life_sound = pygame.mixer.Sound("portal.mp3")
shield_sound = pygame.mixer.Sound("shield.mp3")
obstacle_sound = pygame.mixer.Sound("Enemy.mp3")
door_sound = pygame.mixer.Sound("yay.mp3")

# Setup the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("INFINITE MAZE")
wn.setup(900, 700)

# Register shapes
wn.register_shape("brick.gif")
wn.register_shape("bing3.gif")
wn.register_shape("trap ori.gif")
wn.register_shape("fire new2.gif")
wn.register_shape("life less.gif")
wn.register_shape("sheildd.gif")
wn.register_shape("doorr.gif")
wn.register_shape("character2.gif")
wn.register_shape("Monster 2.1.gif")
wn.register_shape("Monster 2.2.gif")
wn.register_shape("Monster 2.3.gif")
wn.register_shape("Monster 2.4.gif")
wn.register_shape("Monster 2.5.gif")
wn.register_shape("Monster 2.6.gif")
wn.register_shape("standing.gif")  
wn.register_shape("up.gif")  
wn.register_shape("down.gif")  
wn.register_shape("left.gif")  
wn.register_shape("right.gif")

# Set background image
wn.bgpic("bing3.gif")

# Pen class for drawing walls
class Pen(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("brick.gif")
        self.penup()
        self.speed(0)

# Player class for controlling the player
class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("standing.gif")  # Start with the idle GIF
        self.penup()
        self.speed(0)
        self.goto(-320, 320)
        self.fire_power = 0
        self.life = 3  # Or any initial life you want
        self.shield = 0
        self.keys_collected = 0

    def move_up(self):
        new_x = self.xcor()
        new_y = self.ycor() + 32
        if (new_x, new_y) not in walls:
            self.shape("up.gif")  # Change to the up movement GIF
            self.goto(new_x, new_y)
            turtle.ontimer(self.stop, 300)  # Go back to idle after 300ms

    def move_down(self):
        new_x = self.xcor()
        new_y = self.ycor() - 32
        if (new_x, new_y) not in walls:
            self.shape("down.gif")  # Change to the down movement GIF
            self.goto(new_x, new_y)
            turtle.ontimer(self.stop, 300)

    def move_left(self):
        new_x = self.xcor() - 32
        new_y = self.ycor()
        if (new_x, new_y) not in walls:
            self.shape("left.gif")  # Change to the left movement GIF
            self.goto(new_x, new_y)
            turtle.ontimer(self.stop, 300)

    def move_right(self):
        new_x = self.xcor() + 32
        new_y = self.ycor()
        if (new_x, new_y) not in walls:
            self.shape("right.gif")  # Change to the right movement GIF
            self.goto(new_x, new_y)
            turtle.ontimer(self.stop, 300)

    def stop(self):
        self.shape("standing.gif")  # Revert to the idle GIF when not moving

    def update_status(self):
        status_pen.clear()
        status_pen.write(f"Fire: {self.fire_power} | Life: {self.life} | Shield: {self.shield} | Keys: {self.keys_collected}", align="center", font=("Courier", 16, "normal"))


# Monster class to animate the monster
class Monster(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.frames = ["Monster 2.1.gif", "Monster 2.2.gif", "Monster 2.3.gif", "Monster 2.4.gif", "Monster 2.5.gif", "Monster 2.6.gif"]
        self.frame_index = 0
        self.shape(self.frames[self.frame_index])
        self.penup()
        self.speed(0)
        self.goto(-135, -255)

    def animate(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.shape(self.frames[self.frame_index])
        turtle.ontimer(self.animate, 200)

# Door class to represent the exit
class Door(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("doorr.gif")
        self.penup()
        self.speed(0)
        self.goto(384, -384)

# PowerUp class for power-up items (Fire, Life Potion, Shield)
class PowerUp(turtle.Turtle):
    def __init__(self, shape, power_type):
        super().__init__()
        self.shape(shape)
        self.penup()
        self.speed(0)
        self.power_type = power_type

# Obstacle class
class Obstacle(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("trap ori.gif")
        self.penup()
        self.speed(0)

# Define the maze layout
level_2 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X  XXXF      OXXX          X",
    "X  XX   XXXXS XX  XX  XXXXX",
    "X   F  XXXXX     SXXX OXXX",
    "XS  XX  XXXO    XX     FXX",
    "XXX XXL XXXX  X   XXXX  XX",
    "XX  XX  X    XXX   XXX  XX",
    "XXXS  XXX  XXXXXX  XX  XXX",
    "XXX  O  F  XXXXXX    S   X",
    "XXX XXXXXXXX   XX   XXX X",
    "XXX LXXX   X  F   XX   XXX",
    "XXX   F     X  XXXXXX  OXX",
    "XXXXX  XXXXX XXXX     L XX",
    "XXXXX  XXX   FF F F     XX",
    "XXO  F  XX     XX   F  OXX",
    "XX  XXX  F  XXXXXO    XXXX",
    "X  XX  F   XXXXXX    XXXXX",
    "X  XXXXXO         F  XXCXX",
    "XX  XXF      LXXXXXX    XX",
    "XX  XX  XXXXXXXXXXX   SXXX",
    "XXS XX   YX  XXO      XXXX",
    "XX  XX  XX  XX  XXX  XXXXX",
    "XX  XX   XXXXX  XXX  XXXXX",
    "XXXO F   X   FF XXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXX"
]

# List to store wall coordinates
walls = []
obstacles = []
powerups = []
monster = Monster()
monster.animate()

# Function to open the combat window
# Function to open the combat window
def open_combat_window():
    pygame.init()
    combat_win = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Combat Game")

    bg_image = pygame.image.load("background.jpg")
    player_rect = pygame.Rect(100, 500, 60, 80)
    enemy_image = pygame.image.load("Monster 2.11.png")
    enemy_image = pygame.transform.scale(enemy_image, (300, 300))  # Assuming the image size is 300x300
# Manually adjust the rectangle size to fit better
    enemy_rect = pygame.Rect(500, 350, enemy_image.get_width(), enemy_image.get_height())  # Match rectangle size to image size


    bullets = []
    enemy_bullets = []
    clock = pygame.time.Clock()

    player_health = 100
    enemy_health = 100
    player_speed = 10
    gravity = 2
    jump_power = -20
    player_velocity_y = 0
    is_jumping = False

    monster_frames = [
        pygame.transform.scale(pygame.image.load("Monster 2.11.png"), (300, 300)),
        pygame.transform.scale(pygame.image.load("Monster 2.22.png"), (300, 300)),
        pygame.transform.scale(pygame.image.load("Monster 2.33.png"), (300, 300)),
        pygame.transform.scale(pygame.image.load("Monster 2.44.png"), (300, 300)),
        pygame.transform.scale(pygame.image.load("Monster 2.55.png"), (300, 300))
    ]
    monster_frame_index = 0
    monster_animation_speed = 200
    last_monster_animation_time = time.time()

    last_enemy_shot = time.time()
    enemy_shoot_interval = 3

    # Enemy chase speed
    enemy_speed = 3  # You can adjust this to control how fast the enemy chases

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bullet_rect = pygame.Rect(player_rect.right, player_rect.top + player_rect.height // 2 - 5, 15, 10)
                    bullets.append(bullet_rect)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed
        if keys[pygame.K_UP] and not is_jumping:
            is_jumping = True
            player_velocity_y = jump_power

        player_velocity_y += gravity
        player_rect.y += player_velocity_y
        if player_rect.y >= 500:
            player_rect.y = 500
            player_velocity_y = 0
            is_jumping = False
        if player_rect.x < 0:
            player_rect.x = 0
        if player_rect.x > 800 - player_rect.width:
            player_rect.x = 800 - player_rect.width

        # Enemy follows player
        if enemy_rect.x < player_rect.x:
            enemy_rect.x += enemy_speed  # Move right
        elif enemy_rect.x > player_rect.x:
            enemy_rect.x -= enemy_speed  # Move left

        if enemy_rect.y < player_rect.y:
            enemy_rect.y += enemy_speed  # Move down
        elif enemy_rect.y > player_rect.y:
            enemy_rect.y -= enemy_speed  # Move up

        # Prevent monster from going out of bounds
        if enemy_rect.left < 0:
            enemy_rect.left = 0
        if enemy_rect.right > 800:
            enemy_rect.right = 800
        if enemy_rect.top < 0:
            enemy_rect.top = 0
        if enemy_rect.bottom > 600:
            enemy_rect.bottom = 600

        # Check for attack
        if enemy_rect.colliderect(player_rect):
            player_health -= 1  # Reduce player health on attack
            print(f"Player hit! Health: {player_health}")
            if player_health <= 0:
                print("Player defeated!")
                pygame.quit()
                sys.exit()

        for bullet in bullets[:]:
            bullet.x += 15
            if bullet.x > 800:
                bullets.remove(bullet)
            if bullet.colliderect(enemy_rect):
                enemy_health -= 10
                bullets.remove(bullet)
                if enemy_health <= 0:
                    print("Enemy defeated!")
                    pygame.quit()
                    sys.exit()

        current_time = time.time()
        if current_time - last_enemy_shot >= enemy_shoot_interval:
            enemy_bullet = pygame.Rect(enemy_rect.left - 25, enemy_rect.top + enemy_rect.height // 2 - 5, 20, 10)
            enemy_bullets.append(enemy_bullet)
            last_enemy_shot = current_time

        for enemy_bullet in enemy_bullets:
            enemy_bullet.x -= 10
            if enemy_bullet.colliderect(player_rect):
                player_health -= 10
                enemy_bullets.remove(enemy_bullet)
                if player_health <= 0:
                    print("Player defeated!")
                    pygame.quit()
                    sys.exit()

        if current_time - last_monster_animation_time >= monster_animation_speed / 1000:
            monster_frame_index = (monster_frame_index + 1) % len(monster_frames)
            last_monster_animation_time = current_time

        combat_win.blit(pygame.transform.scale(bg_image, (800, 600)), (0, 0))
        pygame.draw.rect(combat_win, (0, 255, 0), player_rect)
        combat_win.blit(monster_frames[monster_frame_index], enemy_rect)

        for bullet in bullets:
            pygame.draw.rect(combat_win, (255, 255, 0), bullet)
        for enemy_bullet in enemy_bullets:
            pygame.draw.rect(combat_win, (0, 0, 255), enemy_bullet)

        player_health_bar_width = 200 * (player_health / 100)
        pygame.draw.rect(combat_win, (255, 0, 0), (50, 20, 200, 20))
        pygame.draw.rect(combat_win, (0, 255, 0), (50, 20, player_health_bar_width, 20))

        enemy_health_bar_width = 200 * (enemy_health / 100)
        pygame.draw.rect(combat_win, (255, 0, 0), (combat_win.get_width() - 250, 20, 200, 20))
        pygame.draw.rect(combat_win, (0, 255, 0), (combat_win.get_width() - 250, 20, enemy_health_bar_width, 20))

        pygame.display.update()
        clock.tick(30)



# Setup maze on the screen
def setup_maze(level):
    wn.tracer(0)
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -384 + (x * 32)
            screen_y = 384 - (y * 32)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.stamp()
                walls.append((screen_x, screen_y))
            elif character == "Y":
                door.goto(screen_x, screen_y)
            elif character == "O":
                obstacle = Obstacle()
                obstacle.goto(screen_x, screen_y)
                obstacles.append(obstacle)
            elif character == "F":
                powerup = PowerUp("fire new2.gif", "fire")
                powerup.goto(screen_x, screen_y)
                powerups.append(powerup)
            elif character == "S":
                powerup = PowerUp("sheildd.gif", "shield")
                powerup.goto(screen_x, screen_y)
                powerups.append(powerup)
            elif character == "L":
                powerup = PowerUp("life less.gif", "life")
                powerup.goto(screen_x, screen_y)
                powerups.append(powerup)

def check_for_collision():
    if player.distance(monster) < 24:  # Check if player is near the monster
        turtle.bye()  
        open_combat_window()  

def interact_obstacles():
    for obstacle in obstacles:
        if player.distance(obstacle) < 10:
            obstacle_sound.play()
            player.goto(-320, 320)
            print("You hit an obstacle! Try again.")

def collect_powerups():
    for powerup in powerups:
        if player.distance(powerup) < 10:
            powerup.hideturtle()
            powerups.remove(powerup)
            if powerup.power_type == "fire":
                player.fire_power += 1
                fire_sound.play()
            elif powerup.power_type == "shield":
                player.shield += 1
                shield_sound.play()
            elif powerup.power_type == "life":
                player.life += 1
                life_sound.play()
            player.update_status()
            print(f"{powerup.power_type.capitalize()} power-up collected!")

# Create instances of the classes
pen = Pen()
player = Player()
door = Door()

# Setup the maze with level 2 layout
setup_maze(level_2)

# Setup status display
status_pen = turtle.Turtle()
status_pen.speed(0)
status_pen.color("white")
status_pen.penup()
status_pen.hideturtle()
status_pen.goto(0, 350)
player.update_status()

# Keyboard bindings
wn.listen()
wn.onkey(player.move_left, "Left")
wn.onkey(player.move_right, "Right")
wn.onkey(player.move_up, "Up")
wn.onkey(player.move_down, "Down")

# Main game loop
while True:
    wn.update()
    interact_obstacles()
    collect_powerups()
    check_for_collision()  # Check for collision with the monster

    # Check for door entry
    if player.distance(door) < 20:
        door_sound.play()
        print("You reached the door and won!")
        break

wn.mainloop()