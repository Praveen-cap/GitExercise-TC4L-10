import turtle
import math 

win = turtle.Screen()
win.bgpic("sword_bg.gif")
win.title("Infinite Maze")
win.setup(700, 700)
win.register_shape("wall.img.gif")
win.register_shape("door.maze.gif")
win.register_shape("trap.gif") 

class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("wall.img.gif")
        self.color("white")
        self.penup()
        self.speed(0)

class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)  
        self.lives = 3  # Player starts with 3 lives

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
    
    def check_position(self):
        # Check if the player is at the door
        if (self.xcor(), self.ycor()) == door_position:
            print("You've reached the door! Game Over.")
            turtle.bye()

        # Check if the player hits a trap
        if (self.xcor(), self.ycor()) in traps:
            self.lives -= 1
            print(f"You hit a trap! Lives left: {self.lives}")
            if self.lives <= 0:
                print("Game Over! You lost all your lives.")
                turtle.bye()

levels = [""]

level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP  XXXXXXX          XXXXX",
    "X  XXXXXXX  XXXXXX  XXXXX",
    "X       XX  XXXXXX  XXXXX",
    "X       XX  XXX        XX",
    "XXXXXX  XX  XXX        XX",
    "XXXXXX  XX  XXXXXX  XXXXX",
    "XXXXXX  XX    XXXX  XXXXX",
    "X  XXX        XXXX  XXXXX",
    "X  XXX  XXXXXXXXXXXXXXXXX",
    "X         XXXXXXXXXXXXXXX",
    "X                XXXXXXXX",
    "XXXXXXXXXX  T    XXXXX  X",
    "XXXXXXXXXXXXX   TXXXXX  X",
    "XXX  XXXXXXXX           X",
    "XXX                     X",
    "XXX          XXXXXXXXXXXX",
    "XXXXXXXXXX   XXXXXXXXXXXX",
    "XXXXXXXXXX              X",
    "XX    XXXXTTT           X",
    "XX    XXXXXXXXXXXX  TXXXX",
    "X             XXXX   XXXX",      
    "X                    XXXX",
    "XXXXXXXXXXXXXX  XX   XXXX",
    "XXXXXXXXXXXXXXXXXXXX  TXX",
    "XXXXXXXXXXXXXXXXXXXXX   D"
]

levels.append(level_1)

def setup_maze(level):
    global door_position

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

            if character == "P":
                player.goto(screen_x, screen_y)

            if character == "D":
                pen.goto(screen_x, screen_y)
                pen.shape("door.maze.gif")  
                pen.stamp()
                door_position = (screen_x, screen_y)
                
            if character == "T":
                pen.goto(screen_x, screen_y)
                pen.shape("trap.gif")  
                pen.stamp()
                traps.append((screen_x, screen_y))

pen = Pen()
player = Player()

walls = []
traps = []
door_position = None

setup_maze(levels[1])
print(walls)

turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")

turtle.done()
