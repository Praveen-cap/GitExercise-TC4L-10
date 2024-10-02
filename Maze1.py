import turtle
import pygame
import time     
import os
import sys

def maze1_main():
    global paused, start_time, pause_start_time
    paused = False
    start_time = time.time()
    pause_start_time = 0
 
    pygame.mixer.init()

    pygame.mixer.music.load("maze 1 music.mp3")  
    pygame.mixer.music.play(loops=-1)  

    fire_sound = pygame.mixer.Sound("fire.mp3")  
    life_sound = pygame.mixer.Sound("portal.mp3") 
    shield_sound = pygame.mixer.Sound("shield.mp3") 
    door_sound = pygame.mixer.Sound("yay.mp3")

    win = turtle.Screen()
    win.bgpic("maze1 bck.gif")
    win.title("Infinite Maze")
    win.setup(width=1.0, height=1.0, startx=None, starty=None)
    win.tracer(0)  # Turn off screen updates for faster performance
    win.register_shape("wall.img.gif")
    win.register_shape("door.maze.gif")
    win.register_shape("trap.gif")
    win.register_shape("fire MAZE1.gif")
    win.register_shape("lifeless maze1.gif")
    win.register_shape("sheild maze1.gif")
    win.register_shape("heart (1).gif")  
    win.register_shape("up.gif")  # Register up movement GIF
    win.register_shape("down.gif")  # Register down movement GIF
    win.register_shape("left.gif")  # Register left movement GIF
    win.register_shape("right.gif")
    win.register_shape("standing.gif")
    win.register_shape("Monster1.5.gif")
    win.register_shape("Monster2.5.gif")
    win.register_shape("Monster3.5.gif")
    win.register_shape("Monster4.5.gif")
    win.register_shape("Monster5.5.gif")
    win.register_shape("Monster 2.6.gif")

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
            self.shape("standing.gif")  # Start with the idle GIF
            self.color("green")
            self.penup()
            self.speed(0) 
            self.goto(-320, 320) 
            self.fire_power = 0
            self.life = 3
            self.shield = 0 

        def go_up(self):
            move_to_x = self.xcor()
            move_to_y = self.ycor() + 24
            print(f"Attempting to move up to ({move_to_x}, {move_to_y})")
            if (move_to_x, move_to_y) not in walls:
                self.shape("up.gif")  # Change to the up movement GIF
                self.goto(move_to_x, move_to_y)
                self.check_position()
                turtle.ontimer(self.stop, 300)  # Go back to idle after 300ms
            else:
                print(f"Blocked by a wall at ({move_to_x}, {move_to_y})")

        def go_down(self):
            move_to_x = self.xcor()
            move_to_y = self.ycor() - 24
            print(f"Trying to move down to ({move_to_x}, {move_to_y})")
            if (move_to_x, move_to_y) not in walls:
                self.shape("down.gif")  # Change to the down movement GIF
                self.goto(move_to_x, move_to_y)
                self.check_position()
                turtle.ontimer(self.stop, 300)
            else:
                print(f"Blocked by a wall at ({move_to_x}, {move_to_y})")

        def go_left(self):
            move_to_x = self.xcor () - 24
            move_to_y = self.ycor()
            if (move_to_x, move_to_y) not in walls: 
                self.shape("left.gif")  # Change to the left movement GIF
                self.goto(move_to_x, move_to_y)
                self.check_position()
                turtle.ontimer(self.stop, 300)

        def go_right(self):
            move_to_x = self.xcor() + 24
            move_to_y = self.ycor()
            if (move_to_x, move_to_y) not in walls:
                self.shape("right.gif") # Change to the right movement GIF
                self.goto(move_to_x, move_to_y)
                self.check_position()
                turtle.ontimer(self.stop, 300)

        def stop (self):
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
            status_pen.write(f"Fire: {self.fire_power} | Life: {self.life} | Shield: {self.shield}", align="center", font=("Times New Roman", 16, "bold")) 

    class Monster(turtle.Turtle):
        def __init__(self):
            super().__init__()
            self.frames = ["Monster1.5.gif", "Monster2.5.gif", "Monster3.5.gif", "Monster4.5.gif", "Monster5.5.gif", "Monster 2.6.gif"]
            self.frame_index = 0
            self.shape(self.frames[self.frame_index])
            self.penup()
            self.speed(0)
            self.goto(250, -310 )

        def animate (self):
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.shape(self.frames[self.frame_index])
            turtle.ontimer(self.animate, 200)

        def go_up(self):
            move_to_x = self.xcor()
            move_to_y = self.ycor() + 24
            print(f"Attempting to move up to ({move_to_x}, {move_to_y})")
            if (move_to_x, move_to_y) not in walls:
                self.shape("up.gif")  # Change to the up movement GIF
                self.goto(move_to_x, move_to_y)
                self.check_position()
                turtle.ontimer(self.stop, 300)  # Go back to idle after 300ms
            else:
                print(f"Blocked by a wall at ({move_to_x}, {move_to_y})")

        def go_down(self):
            move_to_x = self.xcor()
            move_to_y = self.ycor() - 24
            print(f"Trying to move down to ({move_to_x}, {move_to_y})")
            if (move_to_x, move_to_y) not in walls:
                self.shape("down.gif")  # Change to the down movement GIF
                self.goto(move_to_x, move_to_y)
                self.check_position()
                turtle.ontimer(self.stop,  300)
            else:
                print(f"Blocked by a wall at ({move_to_x}, {move_to_y})")

        def go_left(self):
            move_to_x = self.xcor() - 24
            move_to_y = self.ycor()
            if (move_to_x, move_to_y) not in walls: 
                self.shape("left.gif")  # Change to the left movement GIF
                self.goto(move_to_x, move_to_y)
                self.check_position()
                turtle.ontimer(self.stop, 300)

        def go_right(self):
            move_to_x = self.xcor() + 24
            move_to_y = self.ycor()
            if (move_to_x, move_to_y) not in walls:
                self.shape("right.gif")  # Change to the right movement GIF
                self.goto(move_to_x, move_to_y)
                self.check_position()
                turtle.ontimer(self.stop, 300)

        def stop(self):
            self.shape("standing.gif")  # Revert to the idle GIF when not moving

        def update_status(self):
            status_pen.clear()
            status_pen.write(f"Fire: {self.fire_power} | Life: {self.life} | Shield: {self.shield}", align="center", font=("Times New Roman", 16, "bold"))                  
    
        def check_position(self):
            if (self.xcor(), self.ycor()) == door_position:
                print("You 've reached the door! Game Over.")
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
        " XXXXXXXXXX   XXXXXXXXXXXX",
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
    monster = Monster()
    monster.animate()
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
                    start_position = ( screen_x, screen_y)
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
                elif character == "S":  # Shield Power Up
                    powerup = PowerUp("sheild maze1.gif", "shield")
                    powerup.goto(screen_x, screen_y)
                    powerups.append(powerup)
                elif character == "L":  # Life Potion PowerUp
                    powerup = PowerUp("lifeless maze1.gif", "life")
                    powerup.goto(screen_x, screen_y)
                    powerups.append(powerup )
        win.update() 

    def check_for_collision():
        if player.distance(monster) < 24:  # Check if player is near the monster
            turtle.bye()  
            open_combat_window(player.fire_power) 

    # Function to open the combat window
    def open_combat_window(player_fire_power):
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer module
        combat_win = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Combat Game")

        # Load and play background music
        pygame.mixer.music.load("bck.mp3")
        pygame.mixer.music.play(-1)  # Loop the music indefinitely

        # Load sound effect
        impact_sound = pygame.mixer.Sound("impact-152508.mp3")

        bg_image = pygame.image.load("background.jpg")
        bullet_image = pygame.image.load("fireball.png")  
        bullet_image = pygame.transform.scale(bullet_image, (100, 30))

        enemy_bullet_image = pygame.image.load("greenfire..png")  # Replace wit h your image file
        enemy_bullet_image = pygame.transform.scale(enemy_bullet_image, (100, 30)) 

        player_rect = pygame.Rect(100, 500, 120, 80)      
        enemy_image = pygame.image.load("Monster1.png")
        enemy_image = pygame.transform.scale(enemy_image, (200, 200))  # Adjusted size
        enemy_rect = pygame.Rect(600, 400, 200, 200)  # Adjusted size

        bullets = []  # List to hold player bullets
        max_bullets = player_fire_power  # Maximum number of bullets based on player's fire power
        current_bullets = 0  # Current number of bullets shot
        enemy_bullets = []  # List to hold enemy bullets

        clock = pygame.time.Clock()

        player_health = 100
        enemy_health = 100

        player_speed = 10
        gravity = 2
        jump_power = -20
        player_velocity_y = 0
        is_jumping = False
        has_double_jumped = False

        # Monster animation frames
        monster_frames = [
            pygame.transform.scale(pygame.image .load("Monster1.png"), (200, 200)),
            pygame.transform.scale(pygame.image.load("Monster2.png"), (200, 200)),
            pygame.transform.scale(pygame.image.load("Monster3.png"), (200, 200)),
            pygame.transform.scale(pygame.image.load ("Monster4.png"), (200, 200)),
            pygame.transform.scale(pygame.image.load("Monster5.png"), (200, 200))
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
                    enemy_health -= 50
                    impact_sound.play()  # Play impact sound effect
                    bullets .remove(bullet)
                    if enemy_health <= 0:
                        print("Enemy defeated!")
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
                        pygame
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
                return True
                

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
                    player.shield += 1  # Update the shield value
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
     #capture current time when the game begins.so will start from the beginning

    # displaying the timer
    timer_pen = turtle.Turtle()
    timer_pen.hideturtle()
    timer_pen.penup()
    timer_pen.color("white")
    timer_pen.goto(600, 390)

    game_time_limit = 100
    start_time = time.time()

    paused = False
    pause_start_time = 0
    elapsed_time = 0

    def update_timer():
        global paused, start_time, pause_start_time, elapsed_time
        if not paused:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, game_time_limit - int(elapsed_time))  # no below 0
        
            timer_pen.clear()
            timer_pen.write(f"Time left: {remaining_time}s", align="center", font=("Times New Roman", 16, "bold"))
        
            if remaining_time <= 0:
                timer_pen.clear()
                timer_pen.write("Time's up!", align="center", font=("Times New Roman", 24, "bold"))
                win.update()
                print("Time's up! You didn't finish the maze in time. Game Over!")
                pygame.mixer.music.stop() 
                turtle.bye() 
            else:
                win.ontimer(update_timer, 1000)


    # Keyboard bindings for player movements
    win.listen()
    win.onkey(player.go_up, "Up")
    win.onkey(player.go_down, " Down")
    win.onkey(player.go_left, "Left")
    win.onkey(player.go_right, "Right")

    paused = False
    pause_start_time = 0 #capture current time when the game begins.so will start from the beginning
    pause_menu = turtle.Turtle()
    pause_menu.hideturtle()

    pause_menu = turtle.Turtle()
    pause_menu.hideturtle()

    def pause_game():
        global paused, pause_start_time, elapsed_time
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
        win.update()

    def resume_game():
        global paused, start_time, pause_start_time, elapsed_time
        paused = False
        if pause_start_time != 0:
            pause_duration = time.time() - pause_start_time
            start_time += pause_duration
        pygame.mixer.music.unpause()
        pause_menu.clear()
        pause_menu.penup()
        pause_menu.goto(1000, 1000)  # Move the turtle to a position where it won't be visible
        pause_menu.hideturtle()  # Hide the turtle
        win.update()
        update_timer()
        game_loop()

    update_timer

    def exit_game():
        global paused
        paused = False
        pause_menu.clear()
        pause_menu.penup()
        pause_menu.goto(1000, 1000)  # Move the turtle to a position where it won't be visible
        pause_menu.hideturtle()  # Hide the turtle
        print("Game exited!")
        turtle.bye()

    win.listen()
    win.onkey(pause_game, "p")
    win.onkey(resume_game, "r")
    win.onkey(exit_game, "e")


    def game_loop():
        update_timer()
        global paused
        if not paused:
            # Check if the player has reached the door
            if door_position is not None and player.distance(door_position) < 10:
                door_sound.play()
                print("You've reached the door! You win!")
                pygame.mixer.music.stop()
                turtle.bye()
                return
            
            collect_powerups()
            check_for_collision()
            win.update()                
            
            win.ontimer(game_loop, 100)

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
            win.update() # Repeat the game loop every 100 ms() # Repeat the game loop every 100 ms

    # Start the game loop
    game_loop()
    turtle.done()

if __name__ == "__main__":
    maze1_main()