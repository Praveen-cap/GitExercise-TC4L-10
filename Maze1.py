import turtle
#import math 
import pygame
import time

pygame.mixer.init()

pygame.mixer.music.load("maze 1 music.mp3")  # Background music
pygame.mixer.music.play(loops=-1)  # Play the background music on a loop

fire_sound = pygame.mixer.Sound("fire.mp3")  # Sound for fire power-up
life_sound = pygame.mixer.Sound("portal.mp3") #life sound # Sound for life power-up
shield_sound = pygame.mixer.Sound("shield.mp3") #sheild # Sound for shield power-up
door_sound = pygame.mixer.Sound("yay.mp3")

win = turtle.Screen()
win.bgpic("maze1 bck.gif")
win.title("Infinite Maze")
win.setup(800, 600)
win.tracer(0)  # Turn off screen updates for faster performance
win.register_shape("wall.img.gif")
win.register_shape("door.maze.gif")
win.register_shape("trap.gif")
win.register_shape("fire MAZE1.gif")
win.register_shape("lifeless maze1.gif")
win.register_shape("sheild maze1.gif")
win.register_shape("heart (1).gif")  

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("wall.img.gif")
        #self.color("white")
        self.penup()
        self.speed(0)

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("triangle")
        self.color("green")
        self.penup()
        self.speed(0) 
        self.goto(-320, 320) 
        #self.lives = 3 
        self.fire_power = 0
        self.life = 3
        self.shield = 0 

    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24
        print(f"Attempting to move up to ({move_to_x}, {move_to_y})")
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            self.check_position()
        else:
            print(f"Blocked by a wall at ({move_to_x}, {move_to_y})")

    def go_down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24
        print(f"Trying to move down to ({move_to_x}, {move_to_y})")
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            self.check_position()
        else:
            print(f"Blocked by a wall at ({move_to_x}, {move_to_y})")

    def go_left(self):
        move_to_x = self.xcor() - 24
        move_to_y = self.ycor()
        if (move_to_x, move_to_y) not in walls: 
            self.goto(move_to_x, move_to_y)
            self.check_position()

    def go_right(self):
        move_to_x = self.xcor() + 24
        move_to_y = self.ycor()
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            self.check_position() 

    def update_status(self):
        status_pen.clear()
        status_pen.write(f"Fire: {self.fire_power} | Life: {self.life} | Shield: {self.shield}", align="center", font=("Times New Roman", 16, "bold"))                  
    
    def check_position(self):
        if (self.xcor(), self.ycor()) == door_position:
            print("You've reached the door! Game Over.")
            turtle.bye()

        # ensure hits the trap
        if (self.xcor(), self.ycor()) in traps:
                self.hit_by_wall()

    def hit_by_wall(self):
        heart_display.decrease_heart()
        print(f"You hit a wall! ")

        #if self.lives > 0:
         #   self.goto(start_position)
        #else:
         #   print("Game Over! You lost all your lives.")
          #  turtle.bye()

levels = [""]

# PowerUp class for power-up items (Fire, Life Potion, Shield)
class PowerUp(turtle.Turtle):
    def __init__(self, shape, power_type):
        turtle.Turtle.__init__(self)
        self.shape(shape)
        self.penup()
        self.speed(0)
        self.power_type = power_type

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
win.update()

level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP XXXXXXX   L  F   XXXXX",
    "X  XXXXXXX  XXXXXX  XXXXX",
    "X     S  XX  XXXXXX  XXXXX",
    "X    F   XX  XXX F L    XX",
    "X XXXX  XX  XXX   S    XX",
    "XMXXXX  XX  XXXXXX  XXXXX",
    "XXXXXX  XX    XXXX  XXXXX",
    "X  XXX       XXXX  XXXXX",
    "X  XXX TXXXXXXXXXXXXXXXXX",
    "X    L     XXXXXXXXXXXXXXX",
    "X     S    S     XXXXXXXX",
    "XXXXXXXXXXTTT    XXXXX  X",
    "XXXXXXXXXXXXX F TXXXXX  X",
    "XXX  XXXXXXXX     T     X",
    "XXX   F   F   T   F     X",
    "XXXT        TXXXXXXXXXXXX",
    "XXXXXXXXXX   XXXXXXXXXXXX",
    "XXXXXXXXXX T     S      X",
    "XX    XXXXTTT     F     X",
    "XX    XXXXXXXXXXXX  TXXXX",
    "X   F   F F   XXXX   XXXX",      
    "X     S    T        XXXX",
    "XXXXXXXXXXXXXX  XX   XXXX",
    "XXXXXXXXXXXXXXXXXXXX  MXX",
    "XXXXXXXXXXXXXXXXXXXXXT  D"
]
# P=player
# D=door
# T=traps

walls = []
powerups = []
traps =[]
levels.append(level_1)

def setup_maze(level):
    global door_position
    global start_position

    win.tracer(0)  # Disable screen updates

    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -288 + (x * 24)
            screen_y = 288 - (y * 24)

            if character == "X":
                pen.goto(screen_x, screen_y)
                pen.shape("wall.img.gif")
                pen.stamp()
                walls.append((screen_x, screen_y))
            elif character == "P":
                player.goto(screen_x, screen_y)
                start_position = (screen_x, screen_y)
            elif character == "D":
                pen.goto(screen_x, screen_y)
                pen.shape("door.maze.gif")  
                pen.stamp()
                door_position = (screen_x, screen_y)               
            elif character == "T":
                pen.goto(screen_x, screen_y)
                pen.shape("trap.gif")  
                pen.stamp()
                traps.append((screen_x, screen_y))                          
            elif character == "F":  # Fire PowerUp
                powerup = PowerUp("fire MAZE1.gif", "fire")
                powerup.goto(screen_x, screen_y)
                powerups.append(powerup)
            elif character == "S":  # Shield PowerUp
                powerup = PowerUp("sheild maze1.gif", "shield")
                powerup.goto(screen_x, screen_y)
                powerups.append(powerup)
            elif character == "L":  # Life Potion PowerUp
                powerup = PowerUp("lifeless maze1.gif", "life")
                powerup.goto(screen_x, screen_y)
                powerups.append(powerup)
    win.update() 

    #win.tracer(1)  # Re-enable screen updates
def collect_powerups():
    for powerup in powerups:
        if player.distance(powerup) < 20:
            print(f"Power-up {powerup.power_type} collected at {powerup.position()}")
            powerup.hideturtle()
            powerups.remove(powerup)
            if powerup.power_type == "fire":
                player.fire_power += 1
                fire_sound.play()
                print("Fire power-up collected!")
            elif powerup.power_type == "shield":
                player.shield += 1
                shield_sound.play()
                print("Shield power-up collected!")
            elif powerup.power_type == "life":
                player.life += 1
                life_sound.play()
            #player.update_status()
            print(f"{powerup.power_type.capitalize()} power-up collected!")
            player.update_status()
pen = Pen() # pen-provides turtle graphics primitives
player = Player()
heart_display = Heart()  # Initialize heart display

walls = []
traps = []
door_position = None
start_position = None

setup_maze(levels[1])

# Create a pen for the status bar
status_pen = turtle.Turtle()
status_pen.penup()
status_pen.hideturtle()
status_pen.goto(0, 370)
status_pen.color("white")
status_pen.write(f"Fire: {player.fire_power} | Life: {player.life} | Shield: {player.shield}", align="center", font=("Times New Roman", 16, "bold"))


# Timer settings
game_time_limit = 60
start_time = time.time() #capture current time when the game begins.so will start from the beginning

# displaying the timer
timer_pen = turtle.Turtle()
timer_pen.hideturtle()
timer_pen.penup()
timer_pen.color("white")
timer_pen.goto(600, 390)

# Function to update the timer display
def update_timer():
    elapsed_time = time.time() - start_time
    remaining_time = max(0, game_time_limit - int(elapsed_time))  # no below 0
    
    
    timer_pen.clear()
    timer_pen.write(f"Time left: {remaining_time}s", align="center", font=("Times New Roman", 16, "bold"))
    
    
    if remaining_time <= 0:
        print("Time's up! You didn't finish the maze in time. Game Over!")
        pygame.mixer.music.stop()
        turtle.bye() 
    else:
        
        win.ontimer(update_timer, 1000)  # Update every second


# Call the function to start the timer
update_timer()

turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")


def game_loop():
    collect_powerups()
    win.update()
    win.ontimer(game_loop, 100)  # Repeat the game loop every 100 ms


# Start the game loop
game_loop()

turtle.done()

#PRAVEEN TRAP NO SOUND. 