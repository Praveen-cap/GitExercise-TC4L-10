import turtle
import math 
import pygame

pygame.mixer.init()

pygame.mixer.music.load("background 3.mp3")  # Background music
pygame.mixer.music.play(loops=-1)  # Play the background music on a loop

fire_sound = pygame.mixer.Sound("fire.mp3")  # Sound for fire power-up
life_sound = pygame.mixer.Sound("portal.mp3") #life sound # Sound for life power-up
shield_sound = pygame.mixer.Sound("shield.mp3") #sheild # Sound for shield power-up
door_sound = pygame.mixer.Sound("yay.mp3")

win = turtle.Screen()
win.bgpic("sword_bg.gif")
win.title("Infinite Maze")
win.setup(700, 700)
win.register_shape("wall.img.gif")
win.register_shape("door.maze.gif")
win.register_shape("trap.gif")
win.register_shape("fire new2.gif")
win.register_shape("life less.gif")
win.register_shape("sheildd.gif")  

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("wall.img.gif")
        self.color("white")
        self.penup()
        self.speed(0)

class MovingBrick(turtle.Turtle):
    def __init__(self, start_pos, move_distance):
        turtle.Turtle.__init__(self)
        self.shape("wall.img.gif")
        self.color("white")
        self.penup()
        self.speed(1)
        self.start_pos = start_pos
        self.move_distance = move_distance
        self.direction = 1  # 1 means moving up, -1 means moving down
        self.goto(start_pos)

    def move(self):
        self.clear()

        # moving vertically
        new_y = self.ycor() + (self.move_distance * self.direction)
        self.goto(self.xcor(), new_y)
        self.direction *= -1  # Reverse the direction for the next move

        # return to it's position
        self.stamp()

        # ensuring the player is in position after collusion
        if self.distance(player) < 12:
            player.hit_by_wall()

        win.ontimer(self.move, 1000)

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)  
        self.lives = 3 
        self.fire_power = 0
        self.life = 3
        self.shield = 0 

    def go_up(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() + 24
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            self.check_position()

    def go_down(self):
        move_to_x = self.xcor()
        move_to_y = self.ycor() - 24
        if (move_to_x, move_to_y) not in walls:
            self.goto(move_to_x, move_to_y)
            self.check_position()

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
        status_pen.write(f"Fire: {self.fire_power} | Life: {self.life} | Shield: {self.shield} | Keys: {self.keys_collected}", align="center", font=("Courier", 16, "normal"))                  
    
    def check_position(self):
        if (self.xcor(), self.ycor()) == door_position:
            print("You've reached the door! Game Over.")
            turtle.bye()

        # ensure hits the trap
        if (self.xcor(), self.ycor()) in traps:
            self.hit_by_wall()

    def hit_by_wall(self):
        self.lives -= 1
        print(f"You hit a wall! Lives left: {self.lives}")

        if self.lives > 0:
            self.goto(start_position)
        else:
            print("Game Over! You lost all your lives.")
            turtle.bye()

levels = [""]

# PowerUp class for power-up items (Fire, Life Potion, Shield)
class PowerUp(turtle.Turtle):
    def __init__(self, shape, power_type):
        turtle.Turtle.__init__(self)
        self.shape(shape)
        self.penup()
        self.speed(0)
        self.power_type = power_type


level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP XXXXXXX          XXXXX",
    "X  XXXXXXX  XXXXXX  XXXXX",
    "X       XX  XXXXXX  XXXXX",
    "X       XX  XXX F L    XX",
    "X XXXX  XX  XXX   S    XX",
    "XMXXXX  XX  XXXXXX  XXXXX",
    "XXXXXX  XX    XXXX  XXXXX",
    "X  XXX   M    XXXX  XXXXX",
    "X  XXX TXXXXXXXXXXXXXXXXX",
    "X         XXXXXXXXXXXXXXX",
    "X                XXXXXXXX",
    "XXXXXXXXXXTTT    XXXXX  X",
    "XXXXXXXXXXXXX   TXXXXX  X",
    "XXX  XXXXXXXX     T     X",
    "XXX                     X",
    "XXX          XXXXXXXXXXXX",
    "XXXXXXXXXX   XXXXXXXXXXXX",
    "XXXXXXXXXX              X",
    "XX    XXXXTTT           X",
    "XX    XXXXXXXXXXXX  TXXXX",
    "X             XXXX   XXXX",      
    "X                M   XXXX",
    "XXXXXXXXXXXXXX  XX   XXXX",
    "XXXXXXXXXXXXXXXXXXXX  MXX",
    "XXXXXXXXXXXXXXXXXXXXXT  D"
]
# P=player
# D=door
# T=traps
# M=brick movement

powerups = []

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
                
            elif character == "M":
                moving_brick = MovingBrick((screen_x, screen_y), 24)
                moving_bricks.append(moving_brick)
                moving_brick.stamp()  
                moving_brick.move()
            
            elif character == "F":  # Fire PowerUp
                powerup = PowerUp("fire new2.gif", "fire")
                powerup.goto(screen_x, screen_y)
                powerups.append(powerup)
            elif character == "S":  # Shield PowerUp
                powerup = PowerUp("sheildd.gif", "shield")
                powerup.goto(screen_x, screen_y)
                powerups.append(powerup)
            elif character == "L":  # Life Potion PowerUp
                powerup = PowerUp("life less.gif", "life")
                powerup.goto(screen_x, screen_y)
                powerups.append(powerup)
    win.update() 

    win.tracer(1)  # Re-enable screen updates
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

pen = Pen() # pen-provides turtle graphics primitives
player = Player()

walls = []
traps = []
moving_bricks = []
door_position = None
start_position = None

setup_maze(levels[1])

# Create a pen for the status bar
status_pen = turtle.Turtle()
status_pen.penup()
status_pen.hideturtle()
status_pen.goto(0, 370)
status_pen.color("white")
status_pen.write(f"Fire: {player.fire_power} | Life: {player.life} | Shield: {player.shield}", align="center", font=("Courier", 16, "normal"))

turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")

collect_powerups()


turtle.done()