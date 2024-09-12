import turtle

# Setup the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("INFINITE MAZE")
wn.setup(900,700)

# Register the custom images (ensure these images are in the same folder as the script)
wn.register_shape("brick.gif")
wn.register_shape("bing3.gif")  # Register the background image
wn.register_shape("trap ori.gif")

# Set the background image
wn.bgpic("bing3.gif")

# Create the Pen class for drawing the walls
class Pen(turtle.Turtle):
    def _init_(self):
        turtle.Turtle._init_(self)
        self.shape("brick.gif")
        self.penup()
        self.speed(0)

# Create the Player class for controlling the player
class Player(turtle.Turtle):
    def _init_(self):
        turtle.Turtle._init_(self)
        self.shape("turtle")
        self.color("green")
        self.penup()
        self.speed(0)
        self.goto(-320, 320)  # Adjusted to start inside the maze

    # Define movement methods
    def move_up(self):
        new_x = self.xcor()
        new_y = self.ycor() + 32
        if (new_x, new_y) not in walls:  # Prevent moving into walls
            self.goto(new_x, new_y)

    def move_down(self):
        new_x = self.xcor()
        new_y = self.ycor() - 32
        if (new_x, new_y) not in walls:  # Prevent moving into walls
            self.goto(new_x, new_y)

    def move_left(self):
        new_x = self.xcor() - 32
        new_y = self.ycor()
        if (new_x, new_y) not in walls:  # Prevent moving into walls
            self.goto(new_x, new_y)

    def move_right(self):
        new_x = self.xcor() + 32
        new_y = self.ycor()
        if (new_x, new_y) not in walls:  # Prevent moving into walls
            self.goto(new_x, new_y)

# Create the Door class to represent the exit
class Door(turtle.Turtle):
    def _init_(self):
        turtle.Turtle._init_(self)
        self.shape("square")
        self.color("red")
        self.penup()
        self.speed(0)
        self.goto(384, -384)  # Adjusted the door position to fit in the maze

# Create the Collectible class for items the player can collect
class Collectible(turtle.Turtle):
    def _init_(self):
        turtle.Turtle._init_(self)
        self.shape("circle")
        self.color("yellow")
        self.penup()
        self.speed(0)

# Create the Obstacle class for obstacles in the maze
class Obstacle(turtle.Turtle):
    def _init_(self):
        turtle.Turtle._init_(self)
        self.shape("trap ori.gif")
        self.penup()
        self.speed(0)

# List of levels
levels = [""]

# Define the first level layout
level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X  XXX       OXXX    XXXXX",
    "X  XX   XXXX  XX  XX  XXXX",
    "X      XXXXX      XXX OXXX",
    "X   XX  XXXO    XX     CXX",
    "XXX XX  XXXX  X   XXXX  XX",
    "XX  XX  X    XXX   XXX  XX",
    "XXX   XXX  XXXXXX  XX  XXX",
    "XXX  O     XXXXXX        X",
    "XXXXXXXXXXXXX   XX   XXX X",
    "XXX  XXX   X      XX   XXX",
    "XXX   C     X  XXXXXX  OXX",
    "XXXXX  XXXXX XXXX       XX",
    "XXXXX  XXX              XX",
    "XXO     XX     XX      OXX",
    "XX  XXX     XXXXXO    XXXX",
    "X  XX      XXXXXX    XXXXX",
    "X  XXXXXO            XXCXX",
    "XX  XX        XXXXXX    XX",
    "XX  XX  XXXXXXXXXXX    XXX",
    "XX  XX   X  XXO      CXXXX",
    "XX  XX YXX  XX  XXX  XXXXX",
    "XX  XX   XXXXX  XXX  XXXXX",
    "XXXO     X      XXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXX"
]

# Add the level to the levels list
levels.append(level_1)

# List to store wall coordinates
walls = []
collectibles = []
obstacles = []

# Setup the level layout on the screen
def setup_maze(level):
    wn.tracer(0)  # Disable screen updates
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -384 + (x * 32)
            screen_y = 384 - (y * 32)
            
            if character == "X":  # Wall
                pen.goto(screen_x, screen_y)
                pen.stamp()
                walls.append((screen_x, screen_y))  # Add to walls list
            elif character == "Y":  # Door
                door.goto(screen_x, screen_y)
            elif character == "C":  # Collectible
                collectible = Collectible()
                collectible.goto(screen_x, screen_y)
                collectibles.append(collectible)  # Add to collectibles list
            elif character == "O":  # Obstacle
                obstacle = Obstacle()
                obstacle.goto(screen_x, screen_y)
                obstacles.append(obstacle)  # Add to obstacles list    
    wn.update()  # Update the screen with all the drawings at once

# Function to check for item collection
def collect_items():
    for collectible in collectibles:
        if player.distance(collectible) < 10:
            collectible.hideturtle()
            collectibles.remove(collectible)
            print("Item collected!")

# Function to check for interaction with obstacles
def interact_obstacles():
    for obstacle in obstacles:
        if player.distance(obstacle) < 10:
            player.goto(-320, 320)  # Reset player position on collision
            print("You hit an obstacle! Try again.")

# Create instances of the classes
pen = Pen()
player = Player()
door = Door()

# Setup the level
setup_maze(levels[1])

# Bind keyboard keys to player movements
wn.listen()
wn.onkey(player.move_up, "Up")
wn.onkey(player.move_down, "Down")
wn.onkey(player.move_left, "Left")
wn.onkey(player.move_right, "Right")

# Main game loop
while True:
    # Check if the player has reached the door
    if player.distance(door) < 10:
        print("You've reached the door! You win!")
        break  # End the game
    # Check for item collection
    collect_items()

    # Check for interaction with obstacles
    interact_obstacles()

    wn.update()  # Update the screen