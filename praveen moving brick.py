import turtle
import pygame
import math 

pygame.mixer.init()

# Load background music and sound effects (MP3 format)
pygame.mixer.music.load("background 3.mp3")  # Background music
pygame.mixer.music.play(loops=-5)  # Play the background music on a loop

fire_sound = pygame.mixer.Sound("fire.mp3")  # Sound for fire power-up
life_sound = pygame.mixer.Sound("portal.mp3") #life sound # Sound for life power-up
shield_sound = pygame.mixer.Sound("shield.mp3") #sheild # Sound for shield power-up
obstacle_sound = pygame.mixer.Sound("Enemy.mp3")  # Sound for collisions
door_sound = pygame.mixer.Sound("yay.mp3")
# Setup the screen
wn = turtle.Screen()
pen=turtle.Turtle()


wn.bgcolor("black")
wn.title("INFINITE MAZE")
wn.setup(900, 700)



# Register shapes
wn.register_shape("brick.gif")
wn.register_shape("bing3.gif")
wn.register_shape("trap ori.gif")
wn.register_shape("fire new2.gif")
wn.register_shape("life less.gif")
wn.register_shape("sheildd.gif")
wn.register_shape("doorr.gif")
wn.register_shape("character2.gif")

# Set background image
wn.bgpic("maze2jungle.gif")

# Pen class for drawing walls
class Pen(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("brick.gif")
        self.penup()
        self.speed(0)

#Player class for controlling the player
class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("triangle")

        self.penup()
        self.speed(0)
        self.goto(-320, 320)  # Starting position inside the maze
        self.fire_power = 0
        self.life = 1
        self.shield = 0
        self.lives = 3 
    
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
   

    # Update status
    def update_status(self):
        status_pen.clear()
        status_pen.write(f"Fire: {self.fire_power} | Life: {self.life} | Shield: {self.shield}", align="center", font=("Courier", 16, "normal"))

    def hit_by_wall(self):
        self.lives -= 1
        print(f"You hit a wall! Lives left: {self.lives}")

        if self.lives > 0:
            self.goto(-320, 320)
        else:
            print("Game Over! You lost all your lives.")
            turtle.bye()
class MovingBrick(turtle.Turtle):
    def __init__(self, start_pos, move_distance):
        turtle.Turtle.__init__(self)
        self.shape("KJ (2)/brick.gif")
        self.color("white")
        self.penup()
        self.speed(1)
        self.start_pos = start_pos
        self.move_distance = move_distance
        self.direction = 1  # 1 means moving up, -1 means moving down
        self.goto(start_pos)
        self.stamp()
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

        # Check if the moving brick collides with the player
        if self.distance(player) < 12:
            player.hit_by_wall()

        wn.ontimer(self.move, 1000)    
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
    def __init__(self, shape, power_type):
        super().__init__()
        self.shape(shape)
        self.penup()
        self.speed(0)
        self.power_type = power_type


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
    "XXMXXXXXXXXXXXXXXXXXXXXXXXX",
    "X  XXXF      OXXXF        X",
    "X  XX   XXXXS XX  XXM XXXXX",
    "X  MF  XXXXX     SXXX OXXX",
    "XS  XX  XXXO    XX     FXX",
    "XXX XXL XXXX  X   XXXX  XX",
    "XX  XX  X    XXX   XXX  XX",
    "XXXS  XXX MXXXXXX  XX  XXX",
    "XXX  O MF  XXXXXX  M S   X",
    "XXXXXXXXXXXXX   XX  MXXX X",
    "XXX LXXX   X  F   XX   XXX",
    "XXX   F     X  XXXXXXM OXX",
    "XXXXX  XXXXX XXXX     L XX",
    "XXXXX  XXX M FFMF F    MXX",
    "XXO  F  XX     XX   F  OXX",
    "XX  XXX  F  XXXXXO    XXXX",
    "X  XX  F   XXXXXX    XXXXX",
    "X  XXXXXO       M F  XXCXX",
    "XX  XXF     MLXXXXXX    XX",
    "XX  XX MXXXXXXXXXXX   SXXX",
    "XXS XX M YX  XXO      XXXX",
    "XX  XX  XX  XX  XXX  XXXXX",
    "XX  XX  MXXXXX  XXX  XXXXX",
    "XXXO FMM X   FF XXXXXXXXXX",
    "XXXXXXXXXXXXXXXXXXXXXXXXXX"
]

# List to store wall coordinates
walls = []
obstacles = []
powerups = []
moving_bricks = [] 

# Setup maze on the screen
def setup_maze(level):
    global door_position
    global start_position

    wn.tracer(0)  # Turn off screen updates
    for y in range(len(level)):
        for x in range(len(level[y])):
            character = level[y][x]
            screen_x = -384 + (x * 32)
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
                moving_brick = MovingBrick((screen_x, screen_y), 24)
                moving_bricks.append(moving_brick)  
                moving_brick.move()
            elif character == "F":  # Fire PowerUp
                powerup = PowerUp("KJ (2)/fire new2.gif", "fire")
                powerup.goto(screen_x, screen_y)
                powerups.append(powerup)
            elif character == "S":  # Shield PowerUp
                powerup = PowerUp("KJ (2)/sheildd.gif", "shield")
                powerup.goto(screen_x, screen_y)
                powerups.append(powerup)
            elif character == "L":  # Life Potion PowerUp
                powerup = PowerUp("KJ (2)/life less.gif", "life")
                powerup.goto(screen_x, screen_y)
                powerups.append(powerup)
    wn.update()  # Update the screen with all the drawings at once


# Function to interact with obstaTrycles
def interact_obstacles():
    for obstacle in obstacles:
        if player.distance(obstacle) < 10:
            obstacle_sound.play()
            player.goto(-320, 320) # Reset player position on collision
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
            elif powerup.power_type == "life":
                player.life += 1
                life_sound.play()
            player.update_status()
            print(f"{powerup.power_type.capitalize()} power-up collected!")

def quit_game():
    print("Game over! Quitting...")
    turtle.bye()

# Create instances of the classes
pen = Pen()
player = Player()
door = Door()

# Create a pen for the status bar
status_pen = turtle.Turtle()
status_pen.penup()
status_pen.hideturtle()
status_pen.goto(0, 370)
status_pen.color("white")
status_pen.write(f"Fire: {player.fire_power} | Life: {player.life} | Shield: {player.shield}", align="center", font=("Courier", 16, "normal"))

setup_maze(level_2)

   
# Keyboard bindings for player movements
wn.listen()
wn.onkey(player.move_up, "Up")
wn.onkey(player.move_down, "Down")
wn.onkey(player.move_left, "Left")
wn.onkey(player.move_right, "Right")


# Main game loop
def game_loop():

    # Check if the player has reached the door
    if player.distance(door) < 10:
        door_sound.play()
        print("You've reached the door! You win!")
        pygame.mixer.music.stop()
        turtle.bye()
        return
    # Check for interactions with obstacles
    interact_obstacles()

    # Check for power-up collection
    collect_powerups()

    wn.update  

    wn.ontimer(game_loop, 100)
  
game_loop

wn.mainloop()
#except turtle.Terminator:  # Handles window close event
   # pygame.mixer.music.stop()  # Ensure the music stops if the window is closed
