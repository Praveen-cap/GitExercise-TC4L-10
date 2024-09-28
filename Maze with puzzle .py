import turtle
import math
import os
import pygame
from puzzle import PuzzleGame  
pygame.mixer.init()


pygame.mixer.music.load("background_music.mp3") 
pygame.mixer.music.play(-1)

win = turtle.Screen()
win.bgpic("sword_bg.gif")
win.title("Infinite Maze")
win.setup(700, 700)
win.register_shape("wall.img.gif")
win.register_shape("door.maze.gif")
win.register_shape("trap.gif")
win.register_shape("puzzle_icon.gif") 

class Pen(turtle.Turtle):
    def _init_(self):
        turtle.Turtle._init_(self)
        self.shape("wall.img.gif")
        self.color("white")
        self.penup()
        self.speed(0)

class MovingBrick(turtle.Turtle):
    def _init_(self, start_pos, move_distance):
        turtle.Turtle._init_(self)
        self.shape("wall.img.gif")
        self.color("white")
        self.penup()
        self.speed(1)
        self.start_pos = start_pos
        self.move_distance = move_distance
        self.direction = 1  
        self.goto(start_pos)

    def move(self):
        self.clear()

        
        new_y = self.ycor() + (self.move_distance * self.direction)
        self.goto(self.xcor(), new_y)
        self.direction *= -1  

        
        self.stamp()

        
        if self.distance(player) < 12:
            player.hit_by_wall()

        win.ontimer(self.move, 1000)


class Player (turtle.Turtle):
    def _init_(self):
        turtle.Turtle._init_(self)
        self.shape("square")
        self.color("blue")
        self.penup()
        self.speed(0)  
        self.lives = 3  

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
        if (self.xcor(), self.ycor()) == door_position:
            print("You've reached the door! Game Over.")
            turtle.bye()

        if (self.xcor(), self.ycor()) in traps:
            self.hit_by_wall()

        
        if (self.xcor(), self.ycor()) == puzzle_position:
            print("Puzzle time!")
            self.open_puzzle_game()

    def hit_by_wall(self):
        self.lives -= 1
        print(f"You hit a wall! Lives left: {self.lives}")
        if self.lives > 0:
            self.goto(start_position)
        else:
            print("Game Over! You lost all your lives.")
            turtle.bye()

    def open_puzzle_game(self):
        turtle.bye()  
        puzzle_game = PuzzleGame("warrior.gif")
        puzzle_game.main()

levels = [""]

level_1 = [
    "XXXXXXXXXXXXXXXXXXXXXXXXX",
    "XP XXXXXXX          XXXXX",
    "X  XXXXXXX  XXXXXX  XXXXX",
    "X       XX  XXXXXX  XXXXX",
    "X       XX  XXX        XX",
    "X XXXX  XX  XXX        XX",
    "XMXXXX  XX  XXXXXX  XXXXX",
    "XXXXXX  XX    XXXX  XXXXX",
    "X  XXX   M    XXXX  XXXXX",
    "X  XXX TXXXXXXXXXXXXXXXXX",
    "X         XXXXXXXXXXXXXXX",
    "X                XXXXXXXX",
    "XXXXXXXXXXTTT    XXXXX  X",
    "XXXXXXXXXXXXX   TXXXXX  X",
    "XXX  XXXXXXXX     T     X",
    "XXX           ?         X", 
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

levels.append(level_1)


def setup_maze(level):
    global door_position
    global start_position
    global puzzle_position

    win.tracer(0)  

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
                start_position = (screen_x, screen_y)

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

            if character == "M":
                moving_brick =MovingBrick((screen_x, screen_y), 24)
                moving_bricks.append(moving_brick)
                moving_brick.stamp()
                moving_brick.move()

            if character == "?":
                pen.goto(screen_x, screen_y)
                pen.shape("puzzle_icon.gif")  
                pen.stamp()
                puzzle_position = (screen_x, screen_y)

    win.tracer(1)  

pen = Pen()
player=Player()

walls = []
traps = []
moving_bricks = []
door_position = None
start_position = None
puzzle_position = None

setup_maze(levels[1])

turtle.listen()
turtle.onkey(player.go_left, "Left")
turtle.onkey(player.go_right, "Right")
turtle.onkey(player.go_up, "Up")
turtle.onkey(player.go_down, "Down")

turtle.done()