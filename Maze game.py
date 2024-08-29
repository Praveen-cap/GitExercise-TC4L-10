import turtle

# Set up the screen
win = turtle.Screen()
win.bgpic("dungeon_bg.gif")
win.title("Infinite Maze")
win.setup(700, 700)
win.register_shape("wall.img.gif")
win.register_shape("door.maze.gif")
win.register_shape("Standing.gif") 
win.register_shape("Left.gif")  
win.register_shape("Right.gif") 

# Register monster frames as PNG images
win.register_shape("Monster1.5.gif")
win.register_shape("Monster2.5.gif")
win.register_shape("Monster3.5.gif")
win.register_shape("Monster4.5.gif")
win.register_shape("Monster5.5.gif")

# Pen class to draw the walls and door
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("wall.img.gif")
        self.color("white")
        self.penup()
        self.speed(0)

# Player class with integrated movement methods
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("Standing.gif")  # Set the initial image to standing
        self.color("green")
        self.penup()
        self.speed(0)
        self.goto(-264, 264)  # Adjusted to start inside the maze

    # Define movement methods
    def move_up(self):
        self.shape("Standing.gif")  # Change to standing image
        new_x = self.xcor()
        new_y = self.ycor() + 24
        if (new_x, new_y) not in walls:  # Prevent moving into walls
            self.goto(new_x, new_y)
            self.check_if_at_door()

    def move_down(self):
        self.shape("Standing.gif")  # Change to standing image
        new_x = self.xcor()
        new_y = self.ycor() - 24
        if (new_x, new_y) not in walls:  # Prevent moving into walls
            self.goto(new_x, new_y)
            self.check_if_at_door()

    def move_left(self):
        self.shape("Left.gif")  # Change to left-moving image
        new_x = self.xcor() - 24
        new_y = self.ycor()
        if (new_x, new_y) not in walls:  # Prevent moving into walls
            self.goto(new_x, new_y)
            self.check_if_at_door()

    def move_right(self):
        self.shape("Right.gif")  # Change to right-moving image
        new_x = self.xcor() + 24
        new_y = self.ycor()
        if (new_x, new_y) not in walls:  # Prevent moving into walls
            self.goto(new_x, new_y)
            self.check_if_at_door()

    def check_if_at_door(self):
        if (self.xcor(), self.ycor()) == door_position:
            print("You've reached the door! Game Over.")
            turtle.bye()

# Monster class for PNG animation
class Monster(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.frames = ["Monster1.5.gif", "Monster2.5.gif", "Monster3.5.gif", "Monster4.5.gif", "Monster5.5.gif"]
        self.frame_index = 0
        self.shape(self.frames[self.frame_index])
        self.penup()
        self.speed(0)
        self.goto(250, -310)  # Place the monster somewhere in the maze

    def animate(self):
        self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.shape(self.frames[self.frame_index])
        turtle.ontimer(self.animate, 200)  # Adjust the timer as needed for your animation speed

# Define the level layout
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
    "XXXXXXXXXX       XXXXX  X",
    "XXXXXXXXXXXXX    XXXXX  X",
    "XXX  XXXXXXXX           X",
    "XXX                     X",
    "XXX          XXXXXXXXXXXX",
    "XXXXXXXXXX   XXXXXXXXXXXX",
    "XXXXXXXXXX              X",
    "XX    XXXX              X",
    "XX    XXXXXXXXXXXX   XXXX",
    "X             XXXX   XXXX",      
    "X                    XXXX",
    "XXXXXXXXXXXXXX  XX   XXXX",
    "XXXXXXXXXXXXXXXXXXXX   XX",
    "XXXXXXXXXXXXXXXXXXXXX   D"
]

levels.append(level_1)

# Function to set up the maze
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

# Create instances of the Pen, Player, and Monster classes
pen = Pen()
player = Player()
monster = Monster()

# Lists to hold the walls and door position
walls = []
door_position = None

# Set up the maze based on the level layout
setup_maze(levels[1])
print(walls)

# Keyboard bindings for player movement
turtle.listen()
turtle.onkey(player.move_left, "Left")
turtle.onkey(player.move_right, "Right")
turtle.onkey(player.move_up, "Up")
turtle.onkey(player.move_down, "Down")

# Start the monster animation
monster.animate()

# Start the game loop
turtle.done()
