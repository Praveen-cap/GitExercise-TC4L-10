import turtle
import random
import pygame
import time
pygame.mixer.init()

# Load background music and sound effects (MP3 format)
pygame.mixer.music.load("minions song.mp3")  # Background music
pygame.mixer.music.play(loops=-1)  # Play the background music on a loop

fire_sound = pygame.mixer.Sound("fire.mp3")  # Sound for fire power-up
life_sound = pygame.mixer.Sound("portal.mp3") #life sound # Sound for life power-up
shield_sound = pygame.mixer.Sound("shield.mp3") #sheild # Sound for shield power-up
obstacle_sound = pygame.mixer.Sound("trap.mp3")  # Sound for collisions
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
wn.register_shape("brick4.gif")
wn.register_shape("LEVEL3.gif")
wn.register_shape("trap ori.gif")
wn.register_shape("fire new2.gif")
wn.register_shape("life less.gif")
wn.register_shape("sheildd.gif")
wn.register_shape("doorr.gif")
wn.register_shape("KEY1 (1).gif")
wn.register_shape("treasure.gif")
wn.register_shape("random.gif")
wn.register_shape("heart (1).gif")
wn.bgpic("future3.gif")

# Pen class for drawing the walls
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("brick4.gif")
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
        new_y = self.ycor() + 40
        if (new_x, new_y) not in walls: #x
            self.goto(new_x, new_y)

    def move_down(self):
        new_x = self.xcor()
        new_y = self.ycor() - 40
        if (new_x, new_y) not in walls:
            self.goto(new_x, new_y)

    def move_left(self):
        new_x = self.xcor() - 40
        new_y = self.ycor()
        if (new_x, new_y) not in walls:
            self.goto(new_x, new_y)

    def move_right(self):
        new_x = self.xcor() + 40
        new_y = self.ycor()
        if (new_x, new_y) not in walls:
            self.goto(new_x, new_y)

    def update_status(self):
        status_pen.clear()
        status_pen.write(f"Fire: {self.fire_power} | Life: {self.life} | Shield: {self.shield} | Keys: {self.keys_collected}", align="center", font=("Times New Roman", 16, "bold"))

# Door class to represent the exit
class Door(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("doorr.gif")
        self.penup()
        self.speed(0)
        self.goto(400, -400)

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
        self.shape("random.gif")
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
                turtle.bye()  # Close the game window
wn.update()
# Define the third level layout
level_4 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X   XXF   L  L  CX  F      XXXXXX",
    "X   X   XXXXS     XX  T   XX   XX",
    "XX     F  XXXXX     SXXX  O X XX",
    "XS  XX   XXO    XX     F    XXXXX",
    "XXX   XL  XXXX  X   XXXX   XL  XX",
    "XX            XXX   XXX   XK  OXX",
 " XXXS  XXX  XXXXXX       XX FXXX",
    "XXX  O  F  XXXXX     S  XXX   XX",
    "XXX       XXXXX  XXX   XXX L  XX",
    "XXX LXXX      F   XX       O  XXX",
    " XXXX   F   XXXXXXXX  F F     XXX",
    "XK     XXXXXX   YXXXX     L  XXX",
    "XXX    XXX     FXXF          XXX",
    "XXO  F  XX     XX   F     O  XX",
    " XX  XXX  F  XXXXXO      X   XXX",
    "X  XX  F   XXXXXX       XXXXXXXX",
   " XXXXXOT    T   F  XXCX    K  XXX",
    " XXL XXF      LXXXXXX    XX   XXX",
    " XXX    X  XXXF  F    F XXX   S XX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "XX  XK    XXXXX  XXX      XXXXXXX",
    "XXXO F   X   FF        XX  XXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
]

# Add the level to the levels list
#level.append(level_3)

# List to store wall coordinates
 
obstacles = []
powerups = []
keys = []
treasures = []
teleport_holes = []
walls = []
def setup_maze(level):
    wn.tracer(0)
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -600 + (x * 40)
            screen_y = 400 - (y * 40)
            
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
            player.goto(-320, 320) #mula
            heart_display.decrease_heart()  # Decrease heart count
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
                new_x = random.choice(range(-400, 400, 40))  #  TO STAY ON THE GRID
                new_y = random.choice(range(-400, 400, 40))  # creates a new random nposition withinn the grid
                if is_position_valid(new_x, new_y): #if no wall thn yes
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
heart_display = Heart()  # Initialize heart display
# Setup the
# Setup the level
setup_maze(level_4)

# Create a pen for the status bar
status_pen = turtle.Turtle()
status_pen.penup()
status_pen.hideturtle()
status_pen.goto(0, 390)
status_pen.color("white")
status_pen.write(f"Fire: {player.fire_power} | Life: {player.life} | Shield: {player.shield} | Keys: {player.keys_collected}", align="center", font=("Times New Roman", 16, "bold"))


# Timer settings
game_time_limit = 60
start_time = time.time() #record current time when the game begins.so will start from the beginning

# displaying the timer
timer_pen = turtle.Turtle()
timer_pen.hideturtle()
timer_pen.penup()
timer_pen.color("white")
timer_pen.goto(600, 390)

# Function to update the timer display
def update_timer():
    elapsed_time = time.time() - start_time #tikme passed 
    remaining_time = max(0, game_time_limit - int(elapsed_time))  # no below 0
    
    
    timer_pen.clear()
    timer_pen.write(f"Time left: {remaining_time}s", align="center", font=("Times New Roman", 16, "bold"))
    
    
    if remaining_time <= 0:
        print("Time's up! You didn't finish the maze in time. Game Over!")
        turtle.bye() 
    else:
        
        wn.ontimer(update_timer, 1000)  # Update every second

# Call the function to start the timer
update_timer()

# Keyboard for player movements
wn.listen()
wn.onkey(player.move_up, "Up")
wn.onkey(player.move_down, "Down")
wn.onkey(player.move_left, "Left")
wn.onkey(player.move_right, "Right")

# Main game loop
while True:
    interact_obstacles()

    # Check for power-up collection
    collect_powerups()

    collect_keys()
    #interact_with_door()65
    interact_with_teleports()
    collect_treasures()
    check_door()

    wn.update()

    #ALL GOOD. ADD THIS TRAP SOUND THO OTHER MAZE , AND KEY SYSTEM and status to maze 3

