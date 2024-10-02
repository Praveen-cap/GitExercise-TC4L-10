import turtle
import random
import pygame
import sys
import time
import Main
pygame.mixer.init()

def maze4_main():
    global paused, start_time, pause_start_time, question_answered
    paused = False
    start_time = time.time()
    pause_start_time = 0
    question_answered = False
    pygame.display.init()
    


    pygame.mixer.music.load("minions song.mp3")  
    pygame.mixer.music.play(loops=-1)  

    fire_sound = pygame.mixer.Sound("fire.mp3")  
    life_sound = pygame.mixer.Sound("portal.mp3") 
    shield_sound = pygame.mixer.Sound("shield.mp3")
    obstacle_sound = pygame.mixer.Sound("trap.mp3") 
    door_sound = pygame.mixer.Sound("yay.mp3")
    key_sound = pygame.mixer.Sound("fire.mp3")
    portal_sound =pygame.mixer.Sound("fire.mp3")
    door_locked_sound=pygame.mixer.Sound("door close.mp3")
    hole_sound = pygame.mixer.Sound("portal.mp3")
    turtle.register_shape("portal.gif")


    wn = turtle.Screen()
    pen = turtle.Turtle()
    wn.bgcolor("black")
    wn.title("INFINITE MAZE")
    wn.setup(width=1.0, height=1.0, startx=None, starty=None)
    wn.register_shape("question_icon.gif")

    
    wn.tracer(0)
    wn.register_shape("brick4.gif")
    wn.register_shape("LEVEL3.gif")
    wn.register_shape("trap ori.gif")
    wn.register_shape("fire new2.gif")
    wn.register_shape("life less.gif")
    wn.register_shape("sheildd.gif")
    wn.register_shape("doorr.gif")
    wn.register_shape("KEY1 (1).gif")
    wn.register_shape("random.gif")
    wn.register_shape("heart (1).gif")
    wn.bgpic("future3.gif")
    wn.register_shape("up.gif") 
    wn.register_shape("down.gif")  
    wn.register_shape("left.gif")  
    wn.register_shape("right.gif")
    wn.register_shape("standing.gif")
    wn.register_shape("Monster 4.1.gif")
    wn.register_shape("Monster 4.2.gif")
    wn.register_shape("Monster 4.3.gif")
    wn.register_shape("Monster 4.4.gif")
    wn.register_shape("Monster 4.5.gif")
    

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
            self.shape("standing.gif")
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
                self.shape("up.gif")
                self.goto(new_x, new_y)

        def move_down(self):
            new_x = self.xcor()
            new_y = self.ycor() - 40
            if (new_x, new_y) not in walls:
                self.shape("down.gif")
                self.goto(new_x, new_y)

        def move_left(self):
            new_x = self.xcor() - 40
            new_y = self.ycor()
            if (new_x, new_y) not in walls:
                self.goto(new_x, new_y)
                self.shape("left.gif")


        def move_right(self):
            new_x = self.xcor() + 40
            new_y = self.ycor()
            if (new_x, new_y) not in walls:
                self.goto(new_x, new_y)
                self.shape("right.gif")
        
        def stop(self):
            self.shape("standing.gif")  # Revert to the idle GIF when not moving
        
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
        
        def update_status(self):
            status_pen.clear()
            status_pen.write(f"Fire: {self.fire_power} | Life: {self.life} | Shield: {self.shield} | Keys: {self.keys_collected}", align="center", font=("Times New Roman", 16, "bold"))
        
    class Monster(turtle.Turtle):
        def __init__(self):
            super().__init__()
            self.frames = ["Monster 4.1.gif", "Monster 4.2.gif", "Monster 4.3.gif", "Monster 4.4.gif", "Monster 4.5.gif"]
            self.frame_index = 0
            self.shape(self.frames[self.frame_index])
            self.penup()
            self.speed(0)
            self.goto(90, -80)


        def animate (self):
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.shape(self.frames[self.frame_index])
            turtle.ontimer(self.animate, 200)

        def move_up(self):
            new_x = self.xcor()
            new_y = self.ycor() + 32
            if (new_x, new_y) not in walls:
                self.shape("up.gif")
                self.goto(new_x, new_y)

        def move_down(self):
            new_x = self.xcor()
            new_y = self.ycor() - 32
            if (new_x, new_y) not in walls:
                self.goto(new_x, new_y)
                self.shape("down.gif")

        def move_left(self):
            new_x = self.xcor() - 32
            new_y = self.ycor()
            if (new_x, new_y) not in walls:
                self.goto(new_x, new_y)
                self.shape("left.gif")

        def move_right(self):
            new_x = self.xcor() + 32
            new_y = self.ycor()
            if (new_x, new_y) not in walls:
                self.goto(new_x, new_y)
                self.shape("right.gif")

        def stop(self):
            self.shape("standing.gif")  # Revert to the idle GIF when not moving

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

        def update_status(self):
            status_pen.clear()
            status_pen.write(f"Fire: {self.fire_power} | Life: {self.life} | Shield: {self.shield} | Keys: {self.keys_collected}", align="center", font=("Times New Roman", 16, "bold"))
            #if self.lives > 0:
            #   self.goto(start_position)
            #else:
            #   print("Game Over! You lost all your lives.")
            #  turtle.bye()

    level= [""]

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

    class Hole(turtle.Turtle):
        def __init__(self, position, destination):
            turtle.Turtle.__init__(self)
            self.shape("random.gif")  # Use a shape that represents a hole
            self.penup()
            self.speed(0)
            self.goto(position)
            self.destination = destination

        def push_player(self, player):
            player.goto(self.destination)
            print("You've fallen into a hole and been transported to a different location!")

    class TeleportHole(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.shape("portal.gif")
            self.penup()
            self.speed(0)

    class QuestionMark(turtle.Turtle):
        def __init__(self, x, y):
            super().__init__()
            self.shape("question_icon.gif")
            self.penup()
            self.speed(0)
            self.goto(384,-160)

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


    walls = []
    traps=[]
    door_position = None
    start_position = None
    obstacles = []
    powerups = []
    keys = []
    teleport_holes = []
    holes = []
    question_marks = []
    monster = Monster()
    monster.animate()

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
                elif character == "C":
                    teleport_hole = TeleportHole()
                    teleport_hole.goto(screen_x, screen_y)
                    teleport_holes.append(teleport_hole)
                elif character == "H":
                    hole = Hole((screen_x, screen_y), (100, -200))  # Create a hole at the current position that pushes the player to (100, -200)
                    holes.append(hole)
                elif character == "?":
                    question_mark = turtle.Turtle()
                    question_mark.shape("question_icon.gif")
                    question_mark.penup()
                    question_mark.speed(0)
                    question_mark.goto(screen_x, screen_y)
                    question_marks.append(question_mark)    

        wn.update()

    pen = Pen()
    player = Player()
    door = Door()
    heart_display = Heart()  # Initialize heart display

    # Setup the level
    setup_maze(level)

    setup_maze([ 
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "XH  XXF   L  L  CX  F      XXHXXX",
        "X   X   XXXXS     XX  T   XX   XX",
        "XX     F  XXXXX     SXXX  O   XX",
        "XS  XX   XXO    XX     F    XXXXX",
        "XXX   XL  XXXX  X   XXXX   XL  XX",
        "XX            XXX   XXX   XK  OXX",
        " XXXS  XXX  XXXXXX       XX FXXX",
        "XXX  O  F  XXXXX     S  XXX   XX",
        "XXX       XXXXX  XXX   XXX L  XX",
        "XXX LXXX      F   XX       O  XXX",
        " XXXX   F   XXXXXXXX  F F     XXX",
        "XK     XXXXXX  ?  YXXXX     L  XXX",
        "XXX    XXX     FXXXF          XXX",
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
    ])


    def display_question_window():
        pygame.init()
        screen = pygame.display.set_mode((750, 400))
        pygame.display.set_caption("Memory Question")
        font = pygame.font.Font(None, 36)
        
        questions = [
        {
            "question": "What type of powerups we had in all the previous mazes?",
            "options": ["Shield", "Invisible Man", "Sword", "Super Speed"],
            "correct_answer": "Shield"
        },
        {
            "question": "What types of traps we had in Maze Level 2",
            "options": ["Spikes", "Spikes and Moving Bricks", "Spikes, Moving Bricks and Spiky Traps"],
            "correct_answer": "Spikes, Moving Bricks and Spiky Traps"
        },
        {
            "question": "How many keys should be collected to exit the game?",
            "options": ["1", "2","3"],
            "correct_answer": "3"
        },
        {
            "question": "What does the '?' icon represent ?",
            "options": ["A riddle to solve", "A quizzy to complete", "You get a special key"],
            "correct_answer": "A quizzy to complete"
        }
        ]
        
        current_question = 0
        running = True
        while running:
            screen.fill((255, 255, 255))
            
            question = questions[current_question]["question"]
            options = questions[current_question]["options"]
            correct_answer = questions[current_question]["correct_answer"]
            
            question_text = font.render(question, True, (0, 0, 0))
            screen.blit(question_text, (20, 20))
            
            for idx, option in enumerate(options):
                option_text = font.render(f"{idx + 1}. {option}", True, (0, 0, 0))
                screen.blit(option_text, (20, 60 + (idx * 40)))
        
            pygame.display.flip()
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 and options[0] == correct_answer:
                        print("Correct!")
                        current_question += 1
                    elif event.key == pygame.K_2 and options[1] == correct_answer:
                        print("Correct!")
                        current_question += 1
                    elif event.key == pygame.K_3 and options[2] == correct_answer:
                        print("Correct!")
                        current_question += 1
                    else:
                        print("That's the wrong answer. You lost!")
                        running = False
                        return False
                    if current_question >= len(questions):
                        print("You've answered all questions!")
                        running = False
                        return True
        return False
       
    question_answered = False

    def interact_with_question_marks():
        global question_answered
        for question_mark in question_marks:
            if player.distance(question_mark) < 20:
                question_mark.hideturtle()
                question_marks.remove(question_mark)
                print("Question mark touched! Displaying questions...")
                result = display_question_window()
                pygame.display.quit()  # Close the Pygame window
                if result:
                    print("You've answered all questions correctly! Continuing the maze game...")
                    question_answered = True
                    wn.ontimer(game_loop, 100)  # Call the game_loop function again
                else:
                    print("You've answered incorrectly. Game over! You will have to start from the beginning.")
                    player.goto(-320, 320)  # Move the player back to the start
                    player.fire_power = 0
                    player.life = 1
                    player.shield = 0
                    player.keys_collected = 0
                    question_answered = False
                    wn.ontimer(game_loop, 100)  # Close the Turtle graphics window)  # Close the Turtle graphics window    

    def interact_obstacles():
        for obstacle in obstacles:
            if player.distance(obstacle) < 10:
                player.goto(-320, 320) #mula
                heart_display.decrease_heart()  # Decrease heart count
                obstacle_sound.play() 
                print("You hit an obstacle! Try again.")

    def check_for_collision():
        if player.distance(monster) < 20:
            if player.keys_collected < 3:
                print("You need to collect 3 keys before approaching the monster!")
                player.goto(-320, 320)  # Reset player position
            elif player.keys_collected >= 3:
                open_combat_window(player.fire_power)


    def open_combat_window(player_fire_power):
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer module
        combat_win = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Combat Game")


        impact_sound = pygame.mixer.Sound("impact.mp3")

        bg_image = pygame.image.load("background.jpg")
        bullet_image = pygame.image.load("fireball.png")  
        bullet_image = pygame.transform.scale(bullet_image, (100, 30))

        enemy_bullet_image = pygame.image.load("purplefire.png")  
        enemy_bullet_image = pygame.transform.scale(enemy_bullet_image, (100, 30)) 

        player_rect = pygame.Rect(100, 500, 120, 80)      
        enemy_image = pygame.image.load("purplespritesheet.png")
        enemy_image = pygame.transform.scale(enemy_image, (200, 200))  
        enemy_rect = pygame.Rect(600, 400, 200, 200)  

        bullets = [] 
        max_bullets = player_fire_power  
        current_bullets = 0  
        enemy_bullets = []  

        clock = pygame.time.Clock()

        player_health = 100
        enemy_health = 100

        player_speed = 10
        gravity = 2
        jump_power = -20
        player_velocity_y = 0
        is_jumping = False
        has_double_jumped = False

        monster_frames = [
            pygame.transform.scale(pygame.image .load("Monster 4.1.png"), (200, 200)),
            pygame.transform.scale(pygame.image.load("Monster 4.2.png"), (200, 200)),
            pygame .transform.scale(pygame.image.load("Monster 4.3.png"), (200, 200)),
            pygame.transform.scale(pygame.image.load ("Monster 4.4.png"), (200, 200)),
            pygame.transform.scale(pygame.image.load("Monster 4.5.png"), (200, 200))
        ]
        monster_frame_index = 0
        monster_animation_speed = 200  # Milliseconds per frame
        last_monster_animation_time = time.time()

        # Enemy shooting timer
        last_enemy_shot = time.time()
        enemy_shoot_interval = 3 

        # Load player standing image
        player_standing = pygame.image.load("standing2.png")

        # Load player running spritesheet
        player_running = pygame.image.load("running.png")
        frame_width = player_running.get_width() // 5 
        frame_height = player_running.get_height()
        player_running_frame_index = 0
        player_running_animation_speed = 200
        last_player_running_animation_time = time.time()

        # Load player shooting spritesheet
        player_shooting = pygame.image.load("shoot.png")
        shooting_frame_width = player_shooting.get_width() // 3
        shooting_frame_height = player_shooting.get_height()
        player_shooting_frame_index = 0
        player_shooting_animation_speed = 200
        last_player_shooting_animation_time = time.time()
        shooting_animation_playing = False

        current_time = time.time()

        # Create a font object for the power -up text
        power_up_font = pygame.font.SysFont("Arial", 24)

        bullets_fired = 0

        # Main loop for the combat window
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.type == pygame.KEYDOWN:
                        bullet_offset = player_rect.height * -0.8

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE and current_bullets < max_bullets:
                            bullet_rect = pygame.Rect(player_rect.centerx, player_rect.top + bullet_offset, 15, 10)
                            bullets.append(bullet_rect)
                            current_bullets += 1
                            bullets_fired += 1
                            shooting_animation_playing = True
                            player.fire_power -= 1  # Decrease fire power
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT]:
                player_rect.x -= player_speed
            if keys[pygame.K_RIGHT]:
                player_rect.x += player_speed
            if keys[pygame.K_UP] and not is_jumping:  
                is_jumping = True
                player_velocity_y = jump_power
            elif keys[pygame.K_UP] and is_jumping and not has_double_jumped:
                player_velocity_y = jump_power
                has_double_jumped = True

            player_velocity_y += gravity
            player_rect.y += player_velocity_y

            if player_rect.y >= 500:
                player_rect.y = 500
                is_jumping = False
                has_double_jumped = False

            if player_rect.x < 0:
                player_rect.x = 0
            if player_rect.x > 800 - player_rect.width:
                player_rect.x = 800 - player_rect.width

            # Update bullets
            for bullet in bullets[:]:
                bullet.x += 30
                if bullet.x > 800:  
                    bullets.remove(bullet)
                if bullet.colliderect(enemy_rect):
                    enemy_health -= 10
                    impact_sound.play()  # Play impact sound effect
                    bullets .remove(bullet)
                    if enemy_health <= 0:
                        Main.levels_screen()
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()

            # Monster shoots every 3 seconds
            current_time = time.time()
            if current_time - last_enemy_shot >= enemy_shoot_interval:
                enemy_bullet = pygame.Rect(enemy_rect.left - 25, enemy_rect.top + enemy_rect.height // 2 - 5, 20, 10)
                enemy_bullets.append(enemy_bullet)
                last_enemy_shot = current_time

            # Move enemy bullets
            for bullet in enemy_bullets[:]:
                bullet.x -= 25     
                if bullet.x < 0:  
                    enemy_bullets.remove(bullet)
                if bullet.colliderect(player_rect):
                    if player.shield > 0:
                        player.shield -= 1  # Decrease shield
                        print("Shield hit!")
                    else:
                        player.life -= 1  # Decrease life if shield is 0
                        print("Life hit!")
                    enemy_bullets.remove(bullet)
                    if player.life <= 0:
                        print("Player defeated!")
                        pygame.mixer.music.stop()
                        pygame.quit()
                        sys.exit()

            # Monster frame-by-frame animation
            if current_time - last_monster_animation_time >= monster_animation_speed / 1000:
                monster_frame_index = (monster_frame_index + 1) % len(monster_frames)
                last_monster_animation_time = current_time

            # Update player running animation
            if keys[pygame.K_LEFT ] or keys[pygame.K_RIGHT]:
                if current_time - last_player_running_animation_time >= player_running_animation_speed / 1000:
                    player_running_frame_index = (player_running_frame_index + 1) % 5  
                    last_player_running_animation_time = current_time

            # Update player shooting animation
            if shooting_animation_playing:
                current_time = time.time()
                if current_time - last_player_shooting_animation_time >= player_shooting_animation_speed / 1000:
                    player_shooting_frame_index += 1
                    last_player_shooting_animation_time = current_time 
                    if player_shooting_frame_index >= 3:
                        shooting_animation_playing = False
                        player_shooting_frame_index = 0  # Reset the frame index

            # Render the game
            combat_win.blit(pygame.transform.scale(bg_image, (800, 600)), (0, 0))

            # Display collected power-ups
            power_up_text = power_up_font.render(f"Fire: {player.fire_power} | Shield: {player.shield} | Heart: {player.life}", True, (255, 255, 255))
            combat_win.blit(power_up_text, ( 400 - power_up_text.get_width() // 2, 20))

            if shooting_animation_playing:
                shooting_frame_x = player_shooting_frame_index * shooting_frame_width
                shooting_frame_y = 0
                shooting_frame_rect = pygame.Rect(shooting_frame_x, shooting_frame_y, shooting_frame_width, shooting_frame_height)
                shooting_frame = player_shooting.subsurface(shooting_frame_rect)
                combat_win.blit(pygame.transform.scale(shooting_frame, (60, 80)), (player_rect.x, player_rect.y - 50))  # Adjust the -50 offset to lift the image higher
            elif keys[pygame.K_LEFT] or keys[pygame.K_RIGHT]:
                # Draw player running animation
                running_frame_x = player_running_frame_index * frame_width
                running_frame_y = 0
                running_frame_rect = pygame.Rect(running_frame_x, running_frame_y, frame_width, frame_height)
                running_frame = player_running.subsurface(running_frame_rect)
                combat_win.blit(pygame.transform.scale(running_frame, (60 , 80)), (player_rect.x, player_rect.y - 50))  # Adjust the -50 offset to lift the image higher
            else:
                combat_win.blit(player_standing, (player_rect.x, player_rect.y - 50))  # Adjust the -50 offset to lift the image higher

            combat_win.blit(monster_frames[monster_frame_index], enemy_rect)  

            # Draw bullets
            for bullet in bullets:
                combat_win.blit(bullet_image, (bullet.x, bullet.y))
            for bullet in enemy_bullets:
                combat_win.blit(enemy_bullet_image, (bullet.x, bullet.y))

            # Draw health bars
            player_health_bar_width = 200 * (player.life / 3) # changed to 3
            pygame.draw.rect(combat_win, (255, 0, 0), (50, 20, 200, 20))
            pygame.draw.rect (combat_win, (0, 255, 0), (50, 20, player_health_bar_width, 20))
            
            enemy_health_bar_width = 200 * (enemy_health / 100)
            pygame.draw.rect(combat_win, (255, 0, 0), (combat_win.get_width() - 250, 20, 200, 20))
            pygame.draw.rect(combat_win, (0, 255, 0), (combat_win.get_width() - 250, 20, enemy_health_bar_width, 20))

            pygame.display.update()
            clock.tick(30)

            # Check if the monster is defeated
            if bullets_fired >= 11 and enemy_health <= 0:
                print("Victory! You defeated the monster!")
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

                sys.exit()
            

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


    def is_position_valid(x, y):
        """Check if the position (x, y) is valid (not a wall)."""
        return (x, y) not in walls #

    def interact_with_teleports():
        for teleport in teleport_holes:
            if player.distance(teleport) < 20:
                # Teleport the player to a specific set of coordinates
                player.goto(240, -240)  # Change these coordinates to the desired teleport location
                print("You've used the teleport hole!")
            else:
                for hole in holes:
                    if player.distance(hole) < 20:
                        while True:
                            new_x = random.choice(range(-400, 400, 40))  #  TO STAY ON THE GRID
                            new_y = random.choice(range(-400, 400, 40))  # creates a new random nposition withinn the grid
                            if is_position_valid(new_x, new_y): #if no wall thn yes
                                player.goto(new_x, new_y)
                                #portal_sound.play()
                                print("You've used the teleport hole!")
                                break  # Exit the loop once a valid position is found)

    # Create a pen for the status bar
    status_pen = turtle.Turtle()
    status_pen.penup()
    status_pen.hideturtle()
    status_pen.goto(0, 390)
    status_pen.color("white")
    status_pen.write(f"Fire: {player.fire_power} | Life: {player.life} | Shield: {player.shield} | Keys: {player.keys_collected}", align="center", font=("Times New Roman", 16, "bold"))


    # Timer settings
    game_time_limit = 120
    start_time = time.time() #record current time when the game begins.so will start from the beginning

    # displaying the timer
    timer_pen = turtle.Turtle()
    timer_pen.hideturtle()
    timer_pen.penup()
    timer_pen.color("white")
    timer_pen.goto(600, 390)

    # Function to update the timer display
    
    # Function to update the timer display
    def update_timer():
        global paused, start_time, pause_start_time
        if not paused:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, game_time_limit - int(elapsed_time))  # no below 0
        
            timer_pen.clear()
            timer_pen.write(f"Time left: {remaining_time}s", align="center", font=("Times New Roman", 16, "bold"))
        
            if remaining_time <= 0:
                timer_pen.clear()
                timer_pen.write("Time's up!", align="center", font=("Times New Roman", 24, "bold"))
                wn.update()
                print("Time's up! You didn't finish the maze in time. Game Over!")
                pygame.mixer.music.stop() 
                turtle.bye() 
            else:
                wn.ontimer(update_timer, 1000)  # Update every second
    
 
    wn.listen()
    wn.onkey(player.move_up, "Up")
    wn.onkey(player.move_down, "Down")
    wn.onkey(player.move_left, "Left")
    wn.onkey(player.move_right, "Right")

    paused = False
    pause_start_time = 0 #capture current time when the game begins.so will start from the beginning
    pause_menu = turtle.Turtle()
    pause_menu.hideturtle()

    def pause_game():
        global paused, pause_start_time
        paused = True
        pause_start_time = time.time()
        pygame.mixer.music.pause()
        time.sleep(0.1)
        pause_menu.penup()
        pause_menu.goto(0, 0)  # Move the turtle back to the original position
        pause_menu.pendown()
        pause_menu.showturtle()  # Show the turtle
        pause_menu.color("white")
        pause_menu.write("Game Paused", align="center", font=("Arial", 24, "bold"))
        pause_menu.goto(0, -50)
        pause_menu.write("Press 'R' to Resume", align="center", font=("Arial", 18, "normal"))
        pause_menu.goto(0, -150)
        pause_menu.write("Press 'E' to Exit", align="center", font=("Arial", 18, "normal"))
        wn.update()

    def resume_game():
        global paused, start_time, pause_start_time
        paused = False
        if pause_start_time != 0:
            pause_duration = time.time() - pause_start_time
            start_time += pause_duration
        pygame.mixer.music.unpause()
        pause_menu.clear()
        pause_menu.penup()
        pause_menu.goto(1000, 1000)  # Move the turtle to a position where it won't be visible
        pause_menu.hideturtle()  # Hide the turtle
        wn.update()
        update_timer()
        game_loop()

    def exit_game():
        global paused
        paused = False
        pause_menu.clear()
        pause_menu.penup()
        pause_menu.goto(1000, 1000)  # Move the turtle to a position where it won't be visible
        pause_menu.hideturtle()  # Hide the turtle
        print("Game exited!")
        turtle.bye()

    wn.listen()
    wn.onkey(pause_game, "p")
    wn.onkey(resume_game, "r")
    wn.onkey(exit_game, "e")



    def game_loop():
        global question_answered
        update_timer()
        global paused
        if not paused:

            if player.distance(door) < 10:
                if player.keys_collected >= 3:
                    door_sound.play()
                    print("Congratulations! You've collected all keys and completed the maze.")
            else:
                print(f"You need {3 - player.keys_collected} more key(s) to open the door.")
                door_locked_sound.play()
                
                
            check_for_collision()    
            interact_obstacles()
            collect_powerups()
            collect_keys()
            interact_with_teleports()
            if not question_answered:
                interact_with_question_marks()
            wn.update()
            wn.ontimer(game_loop, 100)

        else:
            pause_menu.clear()
            pause_menu.penup()
            pause_menu.color("white")
            pause_menu.goto(0, 0)
            pause_menu.write("Game Paused", align="center", font=("Arial", 24, "bold"))
            pause_menu.goto(0, -50)
            pause_menu.write("Press 'R' to Resume", align="center", font=("Arial", 18, "normal"))
            pause_menu.goto(0, -150)
            pause_menu.write("Press 'E' to Exit", align="center", font=("Arial", 18, "normal"))
            wn.update()

    update_timer()
    game_loop()
    turtle.done()      

if __name__ == "__main__":
    maze4_main()