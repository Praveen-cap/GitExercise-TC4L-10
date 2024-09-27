import turtle
import random
import pygame
import sys
import time

pygame.mixer.init()

# Load background music and sound effects (MP3 format)
pygame.mixer.music.load("background 3.mp3")  # Background music
pygame.mixer.music.play(loops=-1)  # Play the background music on a loop

fire_sound = pygame.mixer.Sound("fire.mp3")  # Sound for fire power-up
life_sound = pygame.mixer.Sound("portal.mp3") #life sound # Sound for life power-up
shield_sound = pygame.mixer.Sound("shield.mp3") #sheild # Sound for shield power-up
obstacle_sound = pygame.mixer.Sound("Enemy.mp3")  # Sound for collisions
door_sound = pygame.mixer.Sound("yay.mp3")
key_sound = pygame.mixer.Sound("fire.mp3")
portal_sound =pygame.mixer.Sound("fire.mp3")
treasure_sound =pygame.mixer.Sound("TREASURE.mp3")
door_locked_sound=pygame.mixer.Sound("door close.mp3")
# Initialize the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("INFINITE MAZE")
wn.setup(800, 600)

# Register shapes
wn.register_shape("brick.gif")
wn.register_shape("LEVEL3.gif")
wn.register_shape("trap ori.gif")
wn.register_shape("fire new2.gif")
wn.register_shape("life less.gif")
wn.register_shape("sheildd.gif")
wn.register_shape("doorr.gif")
wn.register_shape("KEY1 (1).gif")
wn.register_shape("treasure.gif")
wn.register_shape("portal.gif")
wn.bgpic("background3new.gif")
wn.register_shape("Monster 3.1.gif")
wn.register_shape("Monster 3.2.gif")
wn.register_shape("Monster 3.3.gif")
wn.register_shape("Monster 3.4.gif")
wn.register_shape("Monster 3.5.gif")
wn.register_shape("Monster 3.6.gif")


# Pen class for drawing the walls
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("brick.gif")
        self.penup()
        self.speed(0)

# Player class for controlling the player
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("triangle")
        self.color("green")
        self.penup()
        self.speed(0)
        self.goto(-320, 320)
        self.fire_power = 0
        self.life = 1
        self.shield = 0
        self.keys_collected = 0

    def move_up(self):
        new_x = self.xcor()
        new_y = self.ycor() + 32
        if (new_x, new_y) not in walls:
            self.goto(new_x, new_y)

    def move_down(self):
        new_x = self.xcor()
        new_y = self.ycor() - 32
        if (new_x, new_y) not in walls:
            self.goto(new_x, new_y)

    def move_left(self):
        new_x = self.xcor() - 32
        new_y = self.ycor()
        if (new_x, new_y) not in walls:
            self.goto(new_x, new_y)

    def move_right(self):
        new_x = self.xcor() + 32
        new_y = self.ycor()
        if (new_x, new_y) not in walls:
            self.goto(new_x, new_y)

    def update_status(self):
        status_pen.clear()
        status_pen.write(f"Fire: {self.fire_power} | Life: {self.life} | Shield: {self.shield} | Keys: {self.keys_collected}", align="center", font=("Courier", 16, "normal"))

# Monster class to animate the monster
class Monster(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.frames = ["Monster 3.1.gif", "Monster 3.2.gif", "Monster 3.3.gif", "Monster 3.4.gif", "Monster 3.5.gif", "Monster 3.6.gif"]
        self.frame_index = 0
        self.shape(self.frames[self.frame_index])
        self.penup()
        self.speed(0)
        #self.goto(125, -5)  # Position of the monster in the maze

    def animate(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)  # Cycle through the frames
        self.shape(self.frames[self.frame_index])
        turtle.ontimer(self.animate, 200)  # Adjust the time interval for animation (in milliseconds)

# Door class to represent the exit
class Door(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("doorr.gif")
        self.penup()
        self.speed(0)
        self.goto(384, -384)

# PowerUp class for power-up items (Fire, Life Potion, Shield)
class PowerUp(turtle.Turtle):
    def __init__(self, shape, power_type):
        turtle.Turtle.__init__(self)
        self.shape(shape)
        self.penup()
        self.speed(0)
        self.power_type = power_type

# Obstacle class
class Obstacle(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("trap ori.gif")
        self.penup()
        self.speed(0)

# Key class
class Key(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("KEY1 (1).gif")
        self.penup()
        self.speed(0)

# Treasure class
class Treasure(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("treasure.gif")
        self.penup()
        self.speed(0)

# Teleport Hole class
class TeleportHole(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("portal.gif")
        self.penup()
        self.speed(0)

# Define the third level layout
level_3 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X   XXF  K      CX     XXXXXX",
    "X   X   XXXXS     XX     XXXX",
  "XX     F  XXXXX     SXXX  O XXX",
  "XS  XX   XXO    XX  K K F    XX",
  "XXX   XL  XXXX  X   XXXX   XXX",
  "XX         K  XXX   XXX   XXX",
    "XXXS  XXX  XXXXXX         XXXXXX",
    "XXX  O  F  XXXXX     S  XXX   XX",
    "XXX       XXXXX  XXX   XXX       XX",
    "XXX LXXX      F   XX          XXX",
    "XXX   F     XXXXXX       XXXXOXX",
    "XX     XXXXXX   MYXXXX     L  XX",
    "XXX    XXX   F   F   K      XXX",
    "XXO  F  XX     XX   F     OXX",
    " XX  XXX  F  XXXXXO      X   XXX",
  "X  XX  F   XXXXXX       XXXXXXXX",
   "XXXXXXO    TT   F  XXCXXXXX",
    "XX  XXF      LXXXXXX    XX",
    "XX    XXXXXXXXX   S XX",
    "XXS     XX  X    XO      C  XX",
    "XX  X  XX  XX  XXX  X   X",
    "XX  X    XXXXX  XXX     XX",
    "XXXO F   X   FF        XXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]

# Add the level to the levels list
#level.append(level_3)

# List to store wall coordinates
walls = []
obstacles = []
powerups = []
keys = []
treasures = []
teleport_holes = []
monster = Monster()
monster.animate()

def open_combat_window():
    pygame.init()
    combat_win = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Combat Game")

    bg_image = pygame.image.load("background.jpg")  
    player_rect = pygame.Rect(100, 500, 60, 80)      
    enemy_image = pygame.image.load("Monster1.png")  
    enemy_image = pygame.transform.scale(enemy_image, (200, 200))  
    enemy_rect = pygame.Rect(600, 400, 100, 100)  

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
        pygame.transform.scale(pygame.image.load("Monster1.png"), (200, 200)),
        pygame.transform.scale(pygame.image.load("Monster2.png"), (200, 200)),
        pygame.transform.scale(pygame.image.load("Monster3.png"), (200, 200)),
        pygame.transform.scale(pygame.image.load("Monster4.png"), (200, 200)),
        pygame.transform.scale(pygame.image.load("Monster5.png"), (200, 200))
    ]
    monster_frame_index = 0
    monster_animation_speed = 200
    last_monster_animation_time = time.time()

    last_enemy_shot = time.time()
    enemy_shoot_interval = 3 

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
        for bullet in enemy_bullets[:]:
            bullet.x -= 10  
            if bullet.x < 0:  
                enemy_bullets.remove(bullet)
            if bullet.colliderect(player_rect):
                player_health -= 10
                enemy_bullets.remove(bullet)
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
        for bullet in enemy_bullets:
            pygame.draw.rect(combat_win, (0, 0, 255), bullet)

        player_health_bar_width = 200 * (player_health / 100)
        pygame.draw.rect(combat_win, (255, 0, 0), (50, 20, 200, 20))
        pygame.draw.rect(combat_win, (0, 255, 0), (50, 20, player_health_bar_width, 20))
        
        enemy_health_bar_width = 200 * (enemy_health / 100)
        pygame.draw.rect(combat_win, (255, 0, 0), (combat_win.get_width() - 250, 20, 200, 20))
        pygame.draw.rect(combat_win, (0, 255, 0), (combat_win.get_width() - 250, 20, enemy_health_bar_width, 20))

        pygame.display.update()
        clock.tick(30)

def check_door():
    if player.distance(door) < 20:
        if player.keys_collected >= 3:
            print("You've reached the door and collected enough keys! Opening combat window...")
            door_sound.play()
            wn.bye()  # Close the turtle graphics window
            open_combat_window()  # Open the combat window
        else:
            print(f"You need {3 - player.keys_collected} more key(s) to open the door.")
            door_locked_sound.play()

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
            elif character == "K":
                key = Key()
                key.goto(screen_x, screen_y)
                keys.append(key)
            elif character == "T":
                treasure = Treasure()
                treasure.goto(screen_x, screen_y)
                treasures.append(treasure)
            elif character == "C":
                teleport_hole = TeleportHole()
                teleport_hole.goto(screen_x, screen_y)
                teleport_holes.append(teleport_hole)
            elif character == "M":
                monster = Monster()
                monster.goto(screen_x, screen_y)
    wn.update()

monster = Monster()

def interact_obstacles():
    for obstacle in obstacles:
        if player.distance(obstacle) < 10:
            player.goto(-320, 320)
            obstacle_sound.play() 
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

def collect_keys():
    for key in keys:
        if player.distance(key) < 20:
            key.hideturtle()
            keys.remove(key)
            player.keys_collected += 1
            key_sound.play()
            player.update_status()
            print("Key collected!")

def check_door():
    # Player can enter the door only if they have collected 3 keys
    if player.distance(door) < 20:
        if player.keys_collected >= 3:
            print("Congratulations! You've collected all keys and completed the maze.")
            door_sound.play()
            turtle.bye()  # Close the game window
        else:
            print(f"You need {3 - player.keys_collected} more key(s) to open the door.")
            door_locked_sound.play()  # Optional: add a sound effect for locked door



#def interact_with_door():
 #   if player.distance(door) < 10 and player.keys_collected >= 3:
  #      door_sound.play()
   #     print("You've reached the door and collected enough keys! You win!")
    #    return True
    #return False

def is_position_valid(x, y):
    """Check if the position (x, y) is valid (not a wall)."""
    return (x, y) not in walls #

def interact_with_teleports():
    for teleport in teleport_holes:
        if player.distance(teleport) < 20:
            # Keep trying until we find a valid position
            while True:
                new_x = random.choice(range(-384, 384, 32))  # MULTIPLES OF 32 TO STAY ON THE GRID
                new_y = random.choice(range(-384, 384, 32))  # creates a new random nposition withinn the grid
                if is_position_valid(new_x, new_y):
                    player.goto(new_x, new_y)
                    #portal_sound.play()
                    print("You've used the teleport hole!")
                    break  # Exit the loop once a valid position is found

#def interact_with_teleports():
 #   for teleport in teleport_holes:
  #      if player.distance(teleport) < 20:
   #         # Teleport the player to a random position on the screen
    #        new_x = random.choice(range(-384, 384, 32)) #MULTIPLES OF 32 TO STAY ON THE GRID
     #       new_y = random.choice(range(-384, 384, 32))
      #      player.goto(new_x, new_y)
        #    portal_sound.play()
       #     #player.update_status()
         #   print("You've used the teleport hole!")

def collect_treasures():
    for treasure in treasures:
        if player.distance(treasure) < 20:  # Increase distance for collection
            treasure.hideturtle()
            treasures.remove(treasure)
            treasure_sound.play()
            # Add relevant logic for what happens when treasure is collected
            print("Treasure collected!")

# Create instances of the classes
pen = Pen()
player = Player()
door = Door()

# Setup the
# Setup the level
setup_maze(level_3)

# Create a pen for the status bar
status_pen = turtle.Turtle()
status_pen.penup()
status_pen.hideturtle()
status_pen.goto(0, 370)
status_pen.color("white")
status_pen.write(f"Fire: {player.fire_power} | Life: {player.life} | Shield: {player.shield} | Keys: {player.keys_collected}", align="center", font=("Courier", 16, "normal"))

# Keyboard bindings for player movements
wn.listen()
wn.onkey(player.move_up, "Up")
wn.onkey(player.move_down, "Down")
wn.onkey(player.move_left, "Left")
wn.onkey(player.move_right, "Right")

# Main game loop
while True:
    if player.distance(monster) < 20:  # Adjust the distance as needed
        print("You've reached the dinosaur! Opening combat window...")
        open_combat_window()
    # Check if the player has reached the door
    #if player.distance(door) < 10:
     #   door_sound.play()
      #  print("You've reached the door! You win!")
       # pygame.mixer.music.stop()
        #break

    # Check for interactions with obstacles
    interact_obstacles()

    # Check for power-up collection
    collect_powerups()

    collect_keys()
    #interact_with_door()65
    interact_with_teleports()
    collect_treasures()
    check_door()

    wn.update()

#except turtle.Terminator:  # Handles window close event
   # pygame.mixer.music.stop()  # Ensure the music stops if the window is closed

#background small .key n portal not working .the sound effect not working.