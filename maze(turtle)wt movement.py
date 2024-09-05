import turtle


wn = turtle.Screen()
wn.bgcolor("black")
wn.title("INFINITE MAZE")
wn.setup(900,700)


wn.register_shape("brick.gif")
wn.register_shape("bing3.gif")  
wn.register_shape("trap ori.gif")
wn.register_shape("fire new2.gif")  
wn.register_shape("life less.gif")  
wn.register_shape("sheildd.gif") 
wn.register_shape("doorr.gif")
#  background image
wn.bgpic("bing3.gif")

# Pen class for drawing the walls
class Pen(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("brick.gif")
        self.penup()
        self.speed(0)

#  Player class for controlling the player
class Player(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("triangle")
        self.color("green")
        self.penup()
        self.speed(0)
        self.goto(-320, 320)  # grid point,starting pointt.Adjusted to start inside the maze
        self.fire_power = 0
        self.life = 1
        self.shield = 0

    #  movement 
    def move_up(self):
        new_x = self.xcor() # player current x position
        new_y = self.ycor() + 32 #new y position IF THE MOVE UP
        if (new_x, new_y) not in walls:  # Prevent moving into walls ,if the new position is not in the walls list
            self.goto(new_x, new_y) #xde x thr :if no wall(no x at tht place ), move to the new position
#if got x,player is blocked,stay in current ...
#If the player is at (0, 0) and wants to move up to (0, 32), the game checks whether (0, 32) is in the walls list.
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

    #  power-up status bar
    def update_status(self): #current power up information
        status_pen.clear() #to  update the new information
        status_pen.write(f"Fire: {self.fire_power} | Life: {self.life} | Shield: {self.shield}", align="center", font=("Courier", 16, "normal"))
#fstring tht one .to insert in text
#  Door class to represent the exit
class Door(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("doorr.gif")
        #self.color("red")
        self.penup()
        self.speed(0)
        self.goto(384, -384)  # grid position.Adjusted the door position to fit in the maze

#  PowerUp class for power-up items (Fire, Life Potion, Shield)
class PowerUp(turtle.Turtle):
    def __init__(self, shape, power_type):
        turtle.Turtle.__init__(self)
        self.shape(shape)
        self.penup()
        self.speed(0)
        self.power_type = power_type

#  Obstacle class
class Obstacle(turtle.Turtle):
    def __init__(self):
        turtle.Turtle.__init__(self)
        self.shape("trap ori.gif")  
        self.penup()
        self.speed(0)


levels = [""]

# Define the first level layout
level_2 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXXX",
    "X  XXXF      OXXX    XXXXX",
    "X  XX   XXXX  XX  XX  XXXX",
    "X   F  XXXXX     SXXX OXXX",
    "XS  XX  XXXO    XX     FXX",
    "XXX XXL XXXX  X   XXXX  XX",
    "XX  XX  X    XXX   XXX  XX",
    "XXXS  XXX  XXXXXX  XX  XXX",
    "XXX  O  F  XXXXXX    S   X",
    "XXXXXXXXXXXXX   XX   XXX X",
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
    "XXS XX   X  XXO      CXXXX",
    "XX  XX YXX  XX  XXX  XXXXX",
    "XX  XX   XXXXX  XXX  XXXXX",
    "XXXO F   X   FF XXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXX"
]

# Add the level to the levels list
levels.append(level_2)

# List to store wall coordinates
walls = []
obstacles = []
powerups = []

#  level layout on the screen
def setup_maze(level):
    wn.tracer(0)  # Disable screen updates
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -384 + (x * 32) #coordinate of the screen
            screen_y = 384 - (y * 32)
            
            if character == "X":  # Wall
                pen.goto(screen_x, screen_y) #coordinate added to the walls list
                pen.stamp() #stamp wall onto the screen 
                walls.append((screen_x, screen_y))  # store walls pposition in the walls list
            elif character == "Y":  # Door
                door.goto(screen_x, screen_y)
            elif character == "O":  # Obstacle
                obstacle = Obstacle()
                obstacle.goto(screen_x, screen_y)
                obstacles.append(obstacle)  # Add to obstacles list    
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
    wn.update()  # Update the screen with all the drawings at once
def interact_obstacles():
    for obstacle in obstacles:
        if player.distance(obstacle) < 10:
            player.goto(-320, 320)  # Reset player position on collision
            #print("You hit an obstacle! Try again.")

# Function to collect power-ups
def collect_powerups():
    for powerup in powerups:
        if player.distance(powerup) < 10:
            powerup.hideturtle()
            powerups.remove(powerup)
            if powerup.power_type == "fire":
                player.fire_power += 1
            elif powerup.power_type == "shield":
                player.shield += 1
            elif powerup.power_type == "life":
                player.life += 1
            player.update_status()
            print(f"{powerup.power_type.capitalize()} power-up collected!")

# Create instances of the classes
pen = Pen()
player = Player()
door = Door()

# Create a pen for the status bar
status_pen = turtle.Turtle()
status_pen.penup()
status_pen.hideturtle()
status_pen.goto(0, 320)
status_pen.color("white")
status_pen.write(f"Fire: {player.fire_power} | Life: {player.life} | Shield: {player.shield}", align="center", font=("Courier", 16, "normal"))

# Setup the level
setup_maze(levels[1])

# keyboard keys to player movements
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
        break  

    # Check for interaction wiexplth obstacles
    interact_obstacles()

    # Check for power-up collection
    collect_powerups()

    wn.update() 
