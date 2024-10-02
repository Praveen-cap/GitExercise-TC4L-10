import turtle
import pygame
import time
import os
import sys
import math
from turtle import Turtle
pygame.mixer.init()

os.chdir(r"C:\Users\user\mini it\GitExercise-TC4L-10")

# Load background music and sound effects (MP3 format)
pygame.mixer.music.load("background 3.mp3")  # Background music
pygame.mixer.music.play(loops=-5)  # Play the background music on a loop

fire_sound = pygame.mixer.Sound("fire.mp3")  # Sound for fire power-up
life_sound = pygame.mixer.Sound("portal.mp3") #life sound # Sound for life power-up
shield_sound = pygame.mixer.Sound("shield.mp3") #sheild # Sound for shield power-up
obstacle_sound = pygame.mixer.Sound("Enemy.mp3")  # Sound for collisions
door_sound = pygame.mixer.Sound("yay.mp3")
impact_sound = pygame.mixer.Sound("impact.mp3")

wn = turtle.Screen()
pen=turtle.Turtle()


# Setup the screen 
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("INFINITE MAZE")
#wn.setup(900, 700)
wn.setup(width=1.0, height=1.0, startx=None, starty=None)


# Register shapes
wn.register_shape("brick.gif")
wn.register_shape("bing3.gif")
wn.register_shape("trap ori.gif")
wn.register_shape("fire new2.gif")
wn.register_shape("life less.gif")
wn.register_shape("sheildd.gif")
wn.register_shape ("doorr.gif")
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
wn.register_shape("heart (1).gif")

# Set background image 
wn.bgpic("maze2jungle.gif")

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
        self.shape("standing.gif")
        self.penup()
        self.speed(0)
        self.goto(-320, 320)  # Starting position inside the maze
        self.fire_power = 0
        self.life = 1
        self.shield = 0

    # Movement methods
    def move_up(self):
        new_x = self.xcor()
        new_y = self.ycor() + 32
        if (new_x, new_y) not in walls:
            self.shape("up.gif")  # Change to the up movement GIF
            self.goto(new_x, new_y)
            turtle.ontimer(self.stop, 300)

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
        self.shape("standing.gif")
    
    # Update status
    def update_status(self):
        status_pen.clear()
        status_pen.write(f"Fire: {self.fire_power} | Life: {self.life} | Shield: {self.shield}", align="center", font=("Courier", 16, "normal"))

class Monster(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.frames = ["Monster 2.1.gif", "Monster 2.2.gif", "Monster 2.3.gif ", "Monster 2.4.gif ", "Monster 2 .5.gif", "Monster 2.6.gif"]
        self.frame_index = 0
        self .shape(self .frames[self.frame_index])
        self.penup()
        self.speed(0)
        self.goto(-135, -255 )

    def animate (self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.shape(self.frames[self.frame_index])
        turtle.ontimer(self.animate, 200)

def hit_by_wall(self):
    self.lives -= 1
    print(f"You hit a wall! Lives left: {self.lives}")

    if self.lives > 0:
        self.goto(-320, 320)
    else:
            print("Game Over! You lost all your lives.")
            turtle.bye()


class MovingBrick(turtle.Turtle):
    def __init__(self, start_pos, move_distance, player):
        turtle.Turtle.__init__(self)
        self.shape("brick.gif")
        self.color("white")
        self.penup()
        self.speed(0)
        self.start_pos = start_pos
        self.move_distance = 32 #move_distance / 2
        self.direction = 1  # 1 means moving up, -1 means moving down
        self.goto(start_pos)
        self.stamp()
        self.player= player 
        self.move_timer =0

    def move(self):
      self.clear()
      new_y = self.ycor() + (self.move_distance * self.direction)
      self.goto(self.xcor(), new_y)
      self.direction *= -1  # Reverse the direction for the next move
      self.stamp()

      if new_y > self.start_pos[1] + self.move_distance:
        self.direction = -1
      elif new_y < self.start_pos[1] - self.move_distance:
        self.direction = 1 

        self.move_timer = 0  # Reset the move timer

    def update(self):
        self.move_timer += 1
        if self.move_timer >= 10:  # Move every 10 frames
            self.move()
            self.move_timer = 0

# Door class to represent the exit
class Door(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("doorr.gif")
        self.penup()
        self.speed(0)
        self.goto(384, -384)  # Position adjusted to fit in the maze

# PowerUp class for power-up items (Fire, Life Potion, Shield)
class PowerUp(turtle.Turtle):
    def __init__(self, shape, power_type, x, y):
        super().__init__()
        self.shape(shape)
        self.penup()
        self.speed(0)
        self.power_type = power_type
        self.goto(x, y)
        self.original_x = x
        self.original_y = y

# Obstacle class
class Obstacle(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("trap ori.gif")
        self.penup()
        self.speed(0)

class Heart(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("heart (1).gif")  # Heart image
        self.penup()
        self.hideturtle()  # Hide this main instance to avoid displaying an unwanted heart
        self.speed(0)
        self.hearts = 5  # Total number of hearts
        self.positions = [(-700, 270 - (i * 40)) for i in range(5)]  # Positions for hearts , 40 units apart vertically starting at (-700,270)
        self.heart_objects = []
        self.create_hearts()

    def create_hearts(self):
        for pos in self.positions: #loop thru each position in the list
            heart = turtle.Turtle()
            heart.hideturtle()
            heart.shape("heart (1).gif")
            heart.penup()
            heart.speed(0)
            heart.goto(pos) #move to correct position
            self.heart_objects.append(heart)
        self.update_display()
 
    def update_display(self):
        for i in range(len(self.heart_objects)):
            if i < self.hearts: ## If the index is less than the number of hearts
                self.heart_objects[i].showturtle()
            else:
                self.heart_objects[i].hideturtle()

    def decrease_heart(self):
        if self.hearts > 0:
            self.hearts -= 1
            self.update_display()
            print(f"Heart lost! Remaining hearts: {self.hearts}")
            if self.hearts == 0:
                print("Game Over!")
                pygame.mixer.music.stop()
                turtle.bye()  # Close the game window
wn.update()

# Define the maze layout
level_2 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X  XXXF       XXXF       X ",
    "X  MXX  MXXXXS XX  XX  XXX",
    "X   F  XXXXM     SXXX OXXX",
    "XS  XX  XXXO XX     FX   X",
    "XXX XXL XXXX  X   XXXX  XX",
    "XX  XX  MX    XXX  MXXX  X",
    "XXXSM XXX   XXXXX  XX  XXX",
    "XXX  O  F  XXXXXX   MS   X",
    "XXXXXXXXXMMXX   XX   XXX X",
    "XXX LXXX   MX  F   X  M XXX",
    "XXX   F    MX  XXXXXX  OXX",
    "XXXXX  XXXXX XXXX   M L XX",
    "XXXXX  XXX   FM F F     XX",
    "XXO  F  XX     XX   F  OXX",
    "XX  XXX  F MXXXXXO    XXXX",
    "X  XX  F   XXXXXX    XXXXX",
    "X  XXXXXO       M F  XXCXX",
    "XX  XXF      LXXXXXX    XX",
    "XX  XX MXXXXXXXXXXX   SXXX",
    "XXS XX M YX  XXO      XXXX",
    "XX  XX  XX  XX  XXX  XXXXX",
    "XX  XX   XXXXX  XXX  XXXXX",
    "XXXO F MMX   FF XXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXX"
]

# List to store wall coordinates
walls = []
obstacles = []
powerups = []
keys = []
treasures = []
teleport_holes = []
moving_bricks = []
monster = Monster()
monster.animate()

# Setup maze on the screen
def setup_maze(level):
    global door_position
    global start_position

    wn.tracer(0)  # Turn off screen updates
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -384 + (x * 32) #converts grid coordinates into pixe;
            screen_y = 384 - (y * 32)
            
            if character == "X":  # Wall
                pen.goto(screen_x, screen_y)
                pen.stamp()
                walls.append((screen_x, screen_y))
            elif character == "Y":  # Door
                door.goto(screen_x, screen_y)
            elif character == "O":  # Obstacle
                obstacle = Obstacle()
                obstacle.goto(screen_x, screen_y)
                obstacles.append(obstacle)
            elif character == "M":
                moving_brick = MovingBrick((screen_x, screen_y), 24, player)
                moving_bricks.append(moving_brick)  
                moving_brick.move()
            elif character == "F":  # Fire PowerUp
                powerup = PowerUp("fire new2.gif", "fire", screen_x, screen_y)
                powerups.append(powerup)
            elif character == "S":  # Shield PowerUp
                powerup = PowerUp("sheildd.gif", "shield", screen_x, screen_y)
                powerups.append(powerup)
            elif character == "L":  # Life Potion PowerUp
                powerup = PowerUp("life less.gif", "life", screen_x, screen_y)
                powerups.append(powerup)
    wn.update()  # Update the screen with all the drawings at once


def check_for_collision():
    if player.distance(monster) < 24:  # Check if player is near the monster
        turtle.bye()  
        open_combat_window(player.fire_power, player.life, player.shield) 
# Function to open the combat window
def open_combat_window(player_fire_power, player_life, player_shield):
    pygame.init()
    combat_win = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Combat Game")

    bg_image = pygame.image.load("background.jpg")  
    player_rect = pygame.Rect(700, 300, 60, 80)
    enemy_rect = pygame.Rect(700, 250, 40, 80 )  

    monster_frames = [ 
        pygame .transform.scale(pygame.image.load("Monster 2.11.png"), (250, 250)),
        pygame.transform.scale(pygame.image.load("Monster 2.22.png"), (250, 250)),
        pygame.transform.scale(pygame.image.load("Monster 2.33.png"), (250, 250)),
        pygame.transform.scale(pygame.image.load("Monster 2.44.png"), (250, 250)),
        pygame.transform.scale(pygame.image.load("Monster 2.55.png"), (250, 250))
    ]
    monster_frame_index = 0
    monster_animation_speed = 100
    last_monster_animation_time = time.time() 

    bullets = []
    enemy_bullets = []
    clock = pygame.time.Clock()   

    player_health = 100  # Assuming 100 health per life
    enemy_health = 100
    player_speed = 10
    gravity = 2
    jump_power = - 20
    double_jump_power = -15
    player_velocity_y = 0
    is_jumping = False
    has_double_jumped = False

    last_enemy_shot = time.time()
    enemy_shoot_interval = 3

    # Enemy chase speed
    enemy_speed = 2.5 # You can adjust this to control how fast the enemy chases

    # Load player standing image
    player_standing = pygame.image.load("standing2.png")
    player_standing = pygame.transform.scale(player_standing, (100, 120))  # Adjust the size as needed
    player_image = pygame.transform.scale(player_standing, (100, 120))  # Adjust the size as needed
    player_standing_inverted = pygame .transform.flip(player_standing, True, False)
    player_rect = pygame.Rect(100, 300, 100, 120)  # Adjust the size as needed 

    # Load player running spritesheet
    player_running = pygame.image.load("running.png")
    frame_width = player_running.get_width() // 5
    frame_height = player_running.get_height()
    player_running_frame_index = 0
    player_running_animation_speed = 200
    last_player_running_animation_time = time.time()

    # Load player shooting spritesheet
    player_shooting = pygame.image .load("shoot.png")
    shooting_frame_width = player_shooting.get_width() // 3
    shooting_frame_height = player_shooting.get_height()
    player_shooting_frame_index = 0
    player_shooting_animation_speed = 200
    last_player_shooting_animation_time = time.time()
    shooting_animation_playing = False

    # Load fireball image 
    fireball_image = pygame.image.load("fireball.png")
    fireball_image = pygame.transform.scale(fireball_image, (70, 70))

    # Load enemy bullet image
    enemy_bullet_image = pygame.image.load("bluefireball.png")
    enemy_bullet_image = pygame.transform.scale(enemy_bullet_image, (70, 70))

    font = pygame.font.Font(None, 24)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    dx = enemy_rect.x - player_rect.x
                    dy = enemy_rect.y - player_rect.y
                    angle = math.atan2(dy, dx)
                    bullet_rect = pygame.Rect(player_rect.right, player_rect.top - 30, 15, 10)
                    bullet_direction_x = math.cos(angle)
                    bullet_direction_y = math.sin(angle)
                    bullets.append((bullet_rect, (bullet_direction_x, bullet_direction_y)))
                    shooting_animation_playing = True
                    player_fire_power -= 1  # Reduce player fire power
                if event.key == pygame.K_UP and not is_jumping :
                    is_jumping = True
                    player_velocity_y = jump_power
                if event.key == pygame.K_UP and is_jumping and not has_double_jumped:
                    player_velocity_y = double_jump_power
                    has_double_jumped = True

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            player_rect.x -= player_speed
        if keys[pygame.K_RIGHT]:
            player_rect.x += player_speed

        player_velocity_y += gravity
        player_rect.y += player_velocity_y
        if player_rect.y >= 500:
            player_rect.y = 500
            player_velocity_y = 0
            is_jumping = False
            has_double_jumped = False
        if player_rect.x < 0:
            player_rect.x = 0
        if player_rect.x > 800 - player_rect.width:
            player_rect.x = 800 - player_rect.width

        # Enemy follows player
        if enemy_rect.x < player_rect.x:
            enemy_rect.x += enemy_speed  # Move right
        elif enemy_rect.x > player_rect.x:
            enemy_rect.x -= enemy_speed  # Move left

        if enemy_rect.y < player_rect.y - 50:  # Move up
            enemy_rect.y += enemy_speed
        elif enemy_rect.y > player_rect.y - 50:  # Move down
             enemy_rect.y -= enemy_speed
        # Prevent monster from going out of bounds
        if enemy_rect.left < 0:
            enemy_rect.left = 0
        if enemy_rect.right > 800:
            enemy_rect.right = 800
        if enemy_rect.top < 0:
            enemy_rect.top = 0
        if enemy_rect.bottom > 600:
            enemy_rect.bottom =  600

        current_time = time .time()
        if current_time - last_monster_animation_time >= monster_animation_speed / 1000:
            monster_frame_index = (monster_frame_index + 1) % len(monster_frames)
            last_monster_animation_time = current_time

        # Update player running animation
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            # Draw player running animation
            if current_time - last_player_running_animation_time >= player_running_animation_speed / 1000:
                player_running_frame_index = (player_running_frame_index + 1) % 5  
                last_player_running_animation_time = current_time

        # Update player shooting animation
        if shooting_animation_playing:
            current_time = time.time()
            if current_time - last_player_shooting_animation_time >= player_shooting_animation_speed / 1000:
                player_shooting_frame_index += 1
                last_player_shooting_animation_time = current_time
                if player_shooting_frame_index >= 3:
                    shooting_animation_playing = False
                    player_shooting_frame_index = 0  # Reset the frame index

        # Check for attack

        if enemy_rect.colliderect(player_rect):
            if enemy_rect.x < player_rect.x:  # Check if enemy is on the left side of the player
                player_image = player_standing_inverted
            else:
                player_image = player_standing
            if player_shield > 0:
                player_shield -= 1  # Reduce player shield
            else:
                player_health -= 1  # Reduce player health on attack
            print(f"Player hit! Health: {player_health}")
        else:
            player_image = player_standing

        if player_health <= 0:
            print("Player defeated!")
            pygame.quit()
            sys.exit()

        for bullet in bullets[:]:
            bullet_rect, bullet_direction = bullet
            bullet_rect.x += bullet_direction[0] * 15
            bullet_rect.y += bullet_direction[1] * 1
            if bullet_rect.x > 800:
                bullets.remove(bullet)
            if bullet_rect.colliderect(enemy_rect):
                enemy_health -= 2
                impact_sound.play()  # Play impact sound effect
                bullets.remove(bullet)
                if enemy_health <= 0:
                    if player_fire_power >= 19:
                        print("You defeated the monster! Congratulations!")
                        pygame.quit()
                        sys.exit()
                    else:
                        print("You don't have enough fire to defeat the monster. Game Over!")
                        pygame.quit()
                        sys.exit()

        current_time = time.time()
        if current_time - last_enemy_shot >= enemy_shoot_interval:
            enemy_bullet = pygame .Rect(enemy_rect.left - 25, enemy_rect.top + enemy_rect.height // 2 - 5, 20, 10)
            enemy_bullets.append(enemy_bullet)
            last_enemy_shot = current_time

        for enemy_bullet in enemy_bullets:
            enemy_bullet.x -= 10
            if enemy_bullet.colliderect(pygame.Rect(player_rect.x, player_rect.y, player_rect.width, player_rect.height)):
                if player_shield > 0 :
                    player_shield -= 1  # Reduce player shield
                else:
                    player_health -= 10  # Reduce player health on attack
                enemy_bullets.remove(enemy_bullet)
                if player_health <= 0:
                    print("Player defeated!")
                    pygame.quit()
                    sys.exit()

        combat_win.blit(pygame.transform.scale(bg_image, (800, 600)), (0, 0))
        if shooting_animation_playing:
            shooting_frame_x = player_shooting_frame_index * shooting_frame_width
            shooting_frame_y = 0
            shooting_frame_rect = pygame.Rect(shooting_frame_x, shooting_frame_y, shooting_frame_width, shooting_frame_height)
            shooting_frame = player_shooting .subsurface(shooting_frame_rect)
            combat_win.blit(pygame.transform.scale(shooting_frame, (60, 80)), (player_rect.x, player_rect.y - 50))  # Adjust the -50 offset to lift the image higher
        elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
            # Draw player running animation
            running_frame_x = player_running_frame_index * frame_width
            running_frame_y = 0
            running_frame_rect = pygame.Rect(running_frame_x, running_frame_y, frame_width, frame_height)
            running_frame = player_running.subsurface(running_frame_rect)
            combat_win.blit(pygame.transform.scale(running_frame, (60, 80)), (player_rect.x, player_rect.y - 50))  # Adjust the -50 offset to lift the image higher
        else:
            combat_win.blit(player_image, (player_rect.x, player_rect.y - 50))  # Adjust the -50 offset to lift the image higher

        combat_win.blit(monster_frames[monster_frame_index], (enemy_rect.x, enemy_rect .y - 50))  # Adjust the -50 offset to lift the image higher

        for bullet in bullets:
            bullet_rect, bullet_direction = bullet
            combat_win.blit(fireball_image, (bullet_rect.x, bullet_rect.y))

        for enemy_bullet in enemy_bullets:
            combat_win.blit(enemy_bullet_image, enemy_bullet)

        player_health_bar_width =  200 * (player_health / 100)
        pygame.draw.rect(combat_win, (255, 0, 0), (50, 20, 200, 20))
        pygame.draw.rect(combat_win, (0, 255, 0), (50, 20, player_health_bar_width, 20))

        enemy_health_bar_width = 200 * (enemy_health / 100)
        pygame.draw.rect(combat_win, (255, 0, 0), (combat_win.get_width() - 250, 20, 200, 20))
        pygame.draw.rect(combat_win, (0, 255, 0), (combat_win.get_width() - 250, 20, enemy_health_bar_width, 20))

        # Draw the status bar
        font = pygame.font.Font(None, 18)
        status_bar = font.render(f"Fire: {player_fire_power} | Life: {player_life} | Shield: {player_shield}", True, (255, 255, 255))
        combat_win.blit(status_bar, (400 - status_bar.get_width() // 2, 5))  # Draw the status bar at the top middle of the combat window

        pygame.display.update()
        clock.tick(30) 
                        
# Function to interact with obstacles
def interact_obstacles():
    for obstacle in obstacles:
        if player.distance(obstacle) < 10:
            obstacle_sound.play()
            player.goto(-320, 320)# Reset player position on collision
            heart_display.decrease_heart() 
            obstacle_sound.play() 
            print("You hit an obstacle!  again.")

# Function to collect power-ups
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
            elif powerup.power_type  == "life":
                player.life += 1
                life_sound.play()
            player.update_status()
            print(f"{powerup.power_type.capitalize()} power-up collected!")

def interact_moving_bricks():
    for brick in moving_bricks:
        if player.distance(brick) < 12: 
            player.goto(-320, 320)
           #heart_display.decrease_ heart()
            print("You hit a moving brick! Going back to start.")

def quit_game():
    print("Game over! Quitting...")
    turtle.bye()

# Create instances of the classes
pen = Pen()
player = Player()
door = Door()
heart_display = Heart()  # Initialize heart display

# Create a pen for the status bar
status_pen = turtle.Turtle()
status_pen.penup()
status_pen.hideturtle()
status_pen.goto(0, 370)
status_pen.color("white")
status_pen.write(f"Fire: {player.fire_power} | Life: {player.life} | Shield: {player.shield}", align="center", font=("Courier", 16, "normal"))

# Setup the level
setup_maze(level_2)

# Timer settings

# displaying the timer
wn = turtle.Screen()
timer_pen = turtle.Turtle()
timer_pen.hideturtle()
timer_pen.penup()
timer_pen.color("black")
timer_pen.goto(600, 390)
 
game_time_limit = 60
start_time = time.time() #capture current time when the game begins.so will start from the beginning

paused = False
# Function to update the timer display
def update_timer():
    global paused
    elapsed_time = time.time() - start_time
    remaining_time = max(0, game_time_limit - int(elapsed_time))  # no below 0
    
    timer_pen.clear()
    timer_pen.write(f"Time left: {remaining_time}s", align="center", font=("Times New Roman", 16, "bold"))
    
    if remaining_time <= 0:
        timer_pen.clear()
        timer_pen.write("Time's up!", align="center", font=("Times New Roman", 24, "bold"))
        wn.update()
        print("Time's up! You didn't finish the maze in time. Game Over!")
        pygame.mixer.music.stop() 
        turtle.bye() 
    else:
        if not paused:
            wn.ontimer(update_timer, 1000)  # Update every second

update_timer()


# Keyboard bindings for player movements
wn.listen()
wn.onkey(player.move_up, "Up")
wn.onkey(player.move_down, "Down")
wn.onkey(player.move_left, "Left")
wn.onkey(player.move_right, "Right")

paused = False
pause_start_time = 0 #capture current time when the game begins.so will start from the beginning
pause_menu = turtle.Turtle()
pause_menu.hideturtle()

pause_menu = turtle.Turtle()
pause_menu.hideturtle()

def pause_game():
    global paused, pause_start_time
    paused = True
    pause_start_time = time.time()
    pause_menu.penup()
    pause_menu.goto(0, 0)  # Move the turtle back to the original position
    pause_menu.pendown()
    pause_menu.showturtle()  # Show the turtle
    pause_menu.color("white")
    pause_menu.write("Game Paused", align="center", font=("Arial", 24, "bold"))
    pause_menu.goto(0, -50)
    pause_menu.write("Press 'R' to Resume", align="center", font=("Arial", 18, "normal"))
    pause_menu.goto(0, -150)
    pause_menu.write("Press 'E' to Exit", align="center", font=("Arial", 18, "normal"))
    wn.update()

def resume_game():
    global paused, start_time
    paused = False
    pause_duration = time.time() - pause_start_time
    start_time += pause_duration
    pause_menu.clear()
    pause_menu.penup()
    pause_menu.goto(1000, 1000)  # Move the turtle to a position where it won't be visible
    pause_menu.hideturtle()  # Hide the turtle
    wn.update()
    update_timer()
    wn.ontimer(game_loop, 100)

def exit_game():
    global paused
    paused = False
    pause_menu.clear()
    pause_menu.penup()
    pause_menu.goto(1000, 1000)  # Move the turtle to a position where it won't be visible
    pause_menu.hideturtle()  # Hide the turtle
    print("Game exited!")
    turtle.bye()

wn.listen()
wn.onkey(pause_game, "p")
wn.onkey(resume_game, "r")
wn.onkey(exit_game, "e")


def game_loop():
    global paused
    if not paused:
        # Check if the player has reached the door
        if player.distance(door) < 10:
            door_sound.play()
            print("You've reached the door! You win!")
            pygame.mixer.music.stop()
            turtle.bye()
            return

        # Check for interactions with obstacles
        interact_obstacles()
        check_for_collision()
        wn.update()
        interact_obstacles()
        collect_powerups()
        check_for_collision()  # Check for collision with the monster
        # Check for interactions with moving bricks
        interact_moving_bricks()
    
        for brick in moving_bricks:
            brick.update()
        # Check for power-up collection
        collect_powerups()

        wn.update()
        wn.ontimer(game_loop, 100)

    else:
        pause_menu.clear()
        pause_menu.penup()
        pause_menu.color("white")
        pause_menu.goto(0, 0)
        pause_menu.write("Game Paused", align="center", font=("Arial", 24, "bold"))
        pause_menu.goto(0, -50)
        pause_menu.write("Press 'R' to Resume", align="center", font=("Arial", 18, "normal"))
        pause_menu.goto(0, -150)
        pause_menu.write("Press 'E' to Exit", align="center", font=("Arial", 18, "normal"))
        wn.update() # Repeat the game loop every 100 ms() # Repeat the game loop every 100 ms

# Start the game loop
game_loop()
turtle.done()

# Function to interact with obstacles
def interact_obstacles():
    for obstacle in obstacles:
        if player.distance(obstacle) < 10:
            obstacle_sound.play()
            player.goto(-320, 320)# Reset player position on collision
            heart_display.decrease_heart() 
            obstacle_sound.play() 
            print("You hit an obstacle!  again.")

# Function to collect power-ups
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
            elif powerup.power_type  == "life":
                player.life += 1
                life_sound.play()
            player.update_status()
            print(f"{powerup.power_type.capitalize()} power-up collected!")

def interact_moving_bricks():
    for brick in moving_bricks:
        if player.distance(brick) < 12: 
            player.goto(-320, 320)
           #heart_display.decrease_ heart()
            print("You hit a moving brick! Going back to start.")

def quit_game():
    print("Game over! Quitting...")
    turtle.bye()

# Create instances of the classes
pen = Pen()
player = Player()
door = Door()
heart_display = Heart()  # Initialize heart display

# Create a pen for the status bar
status_pen = turtle.Turtle()
status_pen.penup()
status_pen.hideturtle()
status_pen.goto(0, 370)
status_pen.color("white")
status_pen.write(f"Fire: {player.fire_power} | Life: {player.life} | Shield: {player.shield}", align="center", font=("Courier", 16, "normal"))

# Setup the level
setup_maze(level_2)

# Timer settings

# displaying the timer
wn = turtle.Screen()
timer_pen = turtle.Turtle()
timer_pen.hideturtle()
timer_pen.penup()
timer_pen.color("black")
timer_pen.goto(600, 390)

game_time_limit = 60
start_time = time.time() #capture current time when the game begins.so will start from the beginning

paused = False
# Function to update the timer display
def update_timer():
    global paused
    elapsed_time = time.time() - start_time
    remaining_time = max(0, game_time_limit - int(elapsed_time))  # no below 0
    
    timer_pen.clear()
    timer_pen.write(f"Time left: {remaining_time}s", align="center", font=("Times New Roman", 16, "bold"))
    
    if remaining_time <= 0:
        timer_pen.clear()
        timer_pen.write("Time's up!", align="center", font=("Times New Roman", 24, "bold"))
        wn.update()
        print("Time's up! You didn't finish the maze in time. Game Over!")
        pygame.mixer.music.stop() 
        turtle.bye() 
    else:
        if not paused:
            wn.ontimer(update_timer, 1000)  # Update every second

update_timer()


# Keyboard bindings for player movements
wn.listen()
wn.onkey(player.move_up, "Up")
wn.onkey(player.move_down, "Down")
wn.onkey(player.move_left, "Left")
wn.onkey(player.move_right, "Right")

paused = False
pause_start_time = 0 #capture current time when the game begins.so will start from the beginning
pause_menu = turtle.Turtle()
pause_menu.hideturtle()

pause_menu = turtle.Turtle()
pause_menu.hideturtle()

def pause_game():
    global paused, pause_start_time
    paused = True
    pause_start_time = time.time()
    pause_menu.penup()
    pause_menu.goto(0, 0)  # Move the turtle back to the original position
    pause_menu.pendown()
    pause_menu.showturtle()  # Show the turtle
    pause_menu.color("white")
    pause_menu.write("Game Paused", align="center", font=("Arial", 24, "bold"))
    pause_menu.goto(0, -50)
    pause_menu.write("Press 'R' to Resume", align="center", font=("Arial", 18, "normal"))
    pause_menu.goto(0, -150)
    pause_menu.write("Press 'E' to Exit", align="center", font=("Arial", 18, "normal"))
    wn.update()

def resume_game():
    global paused, start_time
    paused = False
    pause_duration = time.time() - pause_start_time
    start_time += pause_duration
    pause_menu.clear()
    pause_menu.penup()
    pause_menu.goto(1000, 1000)  # Move the turtle to a position where it won't be visible
    pause_menu.hideturtle()  # Hide the turtle
    wn.update()
    update_timer()
    wn.ontimer(game_loop, 100)


def exit_game():
    global paused
    paused = False
    pause_menu.clear()
    pause_menu.penup()
    pause_menu.goto(1000, 1000)  # Move the turtle to a position where it won't be visible
    pause_menu.hideturtle()  # Hide the turtle
    print("Game exited!")
    turtle.bye()

wn.listen()
wn.onkey(pause_game, "p")
wn.onkey(resume_game, "r")
wn.onkey(exit_game, "e")


def game_loop():
    global paused
    if not paused:
        # Check if the player has reached the door
        if player.distance(door) < 10:
            door_sound.play()
            print("You've reached the door! You win!")
            pygame.mixer.music.stop()
            turtle.bye()
            return

        # Check for interactions with obstacles
        interact_obstacles()
        check_for_collision()
        wn.update()
        interact_obstacles()
        collect_powerups()
        check_for_collision()  # Check for collision with the monster
        # Check for interactions with moving bricks
        interact_moving_bricks()
    
        for brick in moving_bricks:
            brick.update()
        # Check for power-up collection
        collect_powerups()

        wn.update()
        wn.ontimer(game_loop, 100)

    else:
        pause_menu.clear()
        pause_menu.penup()
        pause_menu.color("white")
        pause_menu.goto(0, 0)
        pause_menu.write("Game Paused", align="center", font=("Arial", 24, "bold"))
        pause_menu.goto(0, -50)
        pause_menu.write("Press 'R' to Resume", align="center", font=("Arial", 18, "normal"))
        pause_menu.goto(0, -150)
        pause_menu.write("Press 'E' to Exit", align="center", font=("Arial", 18, "normal"))
        wn.update() # Repeat the game loop every 100 ms() # Repeat the game loop every 100 ms

# Start the game loop
game_loop()
turtle.done()