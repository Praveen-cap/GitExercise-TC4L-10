import turtle
import random
import pygame

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
    "XX     XXXXXX  Y  XXXX     L  XX",
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
    wn.update()

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
                new_y = random.choice(range(-384, 384, 32))
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
    #interact_with_door()
    interact_with_teleports()
    collect_treasures()
    check_door()

    wn.update()

#except turtle.Terminator:  # Handles window close event
   # pygame.mixer.music.stop()  # Ensure the music stops if the window is closed

#background small .key n portal not working .the sound effect not working.