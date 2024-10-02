import turtle
import random
import pygame
import time
import sys
import Main
from puzzle import PuzzleGame

def maze3_main():
    global paused, start_time, pause_start_time, question_answered
    paused = False
    start_time = time.time()
    pause_start_time = 0
    question_answered = False
    pygame.display.init()

    wn = turtle.Screen()
    wn.bgcolor("black")
    wn.title("INFINITE MAZE")
    wn.setup(width=1.0, height=1.0, startx=None, starty=None)


    # Register shapes
    wn.tracer(0)
    wn.register_shape("brick.gif")
    wn.register_shape("LEVEL3.gif")
    wn.register_shape("trap ori.gif")  
    wn.register_shape("fire new2.gif")
    wn.register_shape("life less.gif")
    wn.register_shape("sheildd.gif")
    wn.register_shape("doorr.gif")
    wn.register_shape("KEY1 (1).gif")
    wn.register_shape("treasure.gif")
    wn.register_shape("random.gif")
    wn.bgpic("background3new.gif")
    wn.register_shape("heart (1).gif")
    wn.register_shape("puzzle_icon (2).gif")
    wn.register_shape("up.gif")  # Register up movement GIF
    wn.register_shape("down.gif")  # Register down movement GIF
    wn.register_shape("left.gif")  # Register left movement GIF
    wn.register_shape("right.gif")
    wn.register_shape("standing.gif")
    wn.register_shape("Monster 3.1.gif")
    wn.register_shape("Monster 3.2.gif")
    wn.register_shape("Monster 3.3.gif")
    wn.register_shape("Monster 3.4.gif")
    wn.register_shape("Monster 3.5.gif")
    wn.register_shape("Monster 3.6.gif")

    # Pen class for drawing the walls
    class Pen(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.shape("brick.gif")
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
            self.treasures_collected = 0

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

    class Monster(turtle.Turtle):
        def __init__(self):
            super().__init__()
            self.frames = ["Monster 3.1.gif", "Monster 3.2.gif", "Monster 3.3.gif", "Monster 3.4.gif", "Monster 3.5.gif", "Monster 3.6.gif"]
            self.frame_index = 0
            self.shape(self.frames[self.frame_index])
            self.penup()
            self.speed(0)
            self.goto(90, -4 )


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

    levels = [""]

    # Door class to represent the exit
    class Door(turtle.Turtle):
        def __init__(self ):
            turtle.Turtle.__init__(self)
            self.shape("doorr.gif")
            self.penup()
            self.speed(0)
            self.goto(384, -384)

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
            wn.update()

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
            self.shape("KEY1 (1).gif")  # Remove the extra space
            self.penup()
            self.speed(0)

    class Treasure(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.shape("treasure.gif")
            self.penup()
            self.speed(0)

    # Teleport Hole class
    class TeleportHole(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.shape("random.gif")
            self.penup()
            self.speed(0)
    # Close the game window

    class PuzzleIcon(turtle.Turtle):
        def __init__(self):
            turtle.Turtle.__init__(self)
            self.shape("puzzle_icon (2).gif")  # Replace with the actual image path
            self.penup()
            self.speed(0)
            # Replace with the actual coordinates

    # List to store wall coordinates
    walls = []
    obstacles = []
    powerups = []
    keys = []
    treasures = []
    teleport_holes = []
    puzzle_icons = []
    puzzle_started = False
    monster = Monster()
    monster.animate()

    def setup_maze(level):
        wn.tracer(0)
        for y in range(len(level)):
            for x in range(len(level[y])):
                character = level[y][x]
                screen_x = -384 + (x * 32)
                screen_y = 384 - (y * 32)
                
                if character == "X":
                    pen.goto(screen_x, screen_y)
                    pen.stamp()
                    walls.append((screen_x, screen_y))
                elif character == "Y":
                    door.goto(screen_x, screen_y)
                elif character == "P":
                    puzzle_icon = PuzzleIcon()
                    puzzle_icon.goto(screen_x, screen_y)
                    puzzle_icons.append(puzzle_icon)
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
                elif character == "T":
                    treasure = Treasure()
                    treasure.goto(screen_x, screen_y)
                    treasures.append(treasure)
                elif character == "C":
                    teleport_hole = TeleportHole()
                    teleport_hole.goto(screen_x, screen_y)
                    teleport_holes.append(teleport_hole)
        wn.update()

    def interact_obstacles():
        for obstacle in obstacles:
            if player.distance(obstacle) < 10:
                player.goto(-320, 320)
                heart_display.decrease_heart()  # Decrease heart count
                print("You hit an obstacle! Try again.")

    def check_for_collision():
        if player.distance(monster) < 20:  # Check if player is near the monster
            turtle.bye()  
            open_combat_window(player.fire_power)

    def open_combat_window(player_fire_power):
        pygame.init()
        pygame.mixer.init()  # Initialize the mixer module
        combat_win = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Combat Game")

        # Loop the music indefinitely

        # Load sound effect
        impact_sound = pygame.mixer.Sound("impact.mp3")

        bg_image = pygame.image.load("background.jpg")
        bullet_image = pygame.image.load("fireball.png")  
        bullet_image = pygame.transform.scale(bullet_image, (100, 30))

        enemy_bullet_image = pygame.image.load("purplefire.png")  # Replace wit h your image file
        enemy_bullet_image = pygame.transform.scale(enemy_bullet_image, (100, 30)) 

        player_rect = pygame.Rect(100, 500, 120, 80)      
        enemy_image = pygame.image.load("Monster 3.1.png")
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
            pygame.transform.scale(pygame.image .load("Monster 3.1.png"), (200, 200)),
            pygame.transform.scale(pygame.image.load("Monster 3.2.png"), (200, 200)),
            pygame.transform.scale(pygame.image.load("Monster 3.3.png"), (200, 200)),
            pygame.transform.scale(pygame.image.load ("Monster 3.4.png"), (200, 200)),
            pygame.transform.scale(pygame.image.load("Monster 3.5.png"), (200, 200))
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

        enemy_speed = 5  # Speed at which the enemy follows the player

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
            if keys[pygame .K_RIGHT]:
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

            # Update enemy position to follow the player
            if enemy_rect.x < player_rect.x:
                enemy_rect.x += enemy_speed
            elif enemy_rect.x > player_rect.x:
                enemy_rect.x -= enemy_speed

            # Update bullets
            for bullet in bullets[:]:
                bullet.x += 30
                if bullet.x > 800:  
                    bullets.remove(bullet)
                if bullet.colliderect(enemy_rect):
                    enemy_health -= 10
                    impact_sound.play()  # Play impact sound effect
                    bullets.remove(bullet)
                    if enemy_health <= 0:
                        
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
                Main.levels_screen()
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

    def collect_powerups():
        for powerup in powerups:
            if player.distance(powerup) < 10 :
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

    def collect_keys():
        for key in keys:
            if player.distance(key) < 20:
                key.hideturtle()
                keys.remove(key)
                player.keys_collected += 1
                player.update_status()
                print("Key collected!")

    def check_door():
        # Player can enter the door only if they have collected 3 keys
        if player.distance(door) < 20:
            if player.keys_collected >= 3:
                print("Congratulations! You've collected all keys and completed the maze.")
                turtle.bye()  # Close the game window
            else:
                print(f"You need {3 - player.keys_collected} more key(s) to open the door.")

    def interact_with_teleports():
        global puzzle_started
        for teleport in teleport_holes:
            if player.distance(teleport) < 20:
                # Keep trying until we find a valid position
                while True:
                    new_x = random.choice(range(-384, 384, 32))  # MULTIPLES OF 32 TO STAY ON THE GRID
                    new_y = random.choice(range(-384, 384, 32))  # creates a new random nposition withinn the grid
                    if is_position_valid(new_x, new_y):
                        player.goto(new_x, new_y)
                        print("You've used the teleport hole!")
                        # Start the puzzle game when the player reaches a certain point
                        if (new_x, new_y) == (-192, 192) and not puzzle_started:  # Replace with the actual coordinates
                            puzzle_started = True
                            start_puzzle_game()
                        break  # Exit the loop once a valid position is found
        for puzzle_icon in puzzle_icons:  # You need to define puzzle_icons as a list of puzzle icons
            if player.distance(puzzle_icon) < 20 and not puzzle_started:
                puzzle_started = True
                start_puzzle_game()

    def collect_treasures():
        for treasure in treasures:
            if player.distance(treasure) < 20:  # Increase distance for collection
                treasure.hideturtle()
                treasures.remove(treasure)
                #collect_treasure_reward

                player.fire_power += 5
                player.life += 2
                player.shield += 2
                player.update_status()
                #Add relevant logic for what happens when treasure is collected
                print("Treasure collected!")

    def is_position_valid(x, y):
        """Check if the position (x, y) is valid (not a wall)."""
        return (x, y) not in walls 

    def start_puzzle_game():
        game = PuzzleGame("dragon.jpg")  # Replace with the actual image path
        game.main()
        if game.was_solved():
            print("Puzzle solved! You can proceed.")
            # Add logic to proceed with the game
            return True
        else:
            print("Puzzle not solved. Game over.")
            player.goto(-320, 320) # Reset player position
            return False

    # Create instances of the classes
    pen = Pen()
    player = Player()
    door = Door()
    heart_display = Heart()  # Initialize heart display

    walls = []
    traps = []
    door_position = None
    start_position = None

    # Setup the level
    setup_maze([
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
        "X   XXF   L  L  CX  F    T  XXXXXX",
        "X   X   XXXXS     XX      XX   XX",
        "XX     F  XXXXX     SXXX  O X XX",
        "XS  XX   XXO    XX     F    XXX XX",
        "XXX   XL  XXXX  X   XXXX   XL  XX",
        "XX            XXX   XXX   XK  OXX",
        " XXXS  XXX  XXXXXX       XX FXXX",
        "XXX  O  F  XXXXX P    S  XXX   XX",
        "XXX       XXXXX  XXX   XXX L  XX",
        "XXX LXXX      F   XX       O  XXX",
        " XXXX   F   XXXXXXXX  F F     XXX",
        "XK     XXXXXX   YXXXX     L XXX",
        "XXX    XXX     FXXF          XXX",
        "XXO  F  XX     XX   F O  XX",
        " XX  XXX  F  XXXXXO      X   XXX",
        "X  XX  F   XXXXXX       XXXXXXXX",
    " XXXXXOT         F  XXCX X K  XXX",
        " XXL XXF      LXXXXXX    XX   XXX",
        " XXX    X  XXXF  F    F XXX   S XX",
        "XXS     XX  X    XO      C    XX",
        "XX  X  XX  XX  XXX  X      XXXXX",
        "XX  XK    XXXXX  XXX      XXXXXXX",
        "XXXO F   X   FF        XX  XXXXX",
        "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
    ])

    # Create a pen for the status bar
    status_pen = turtle.Turtle()
    status_pen.penup()
    status_pen.hideturtle()
    status_pen.goto(0, 370)
    status_pen.color("white")
    status_pen.write(f"Fire: {player.fire_power} | Life: {player.life} | Shield: {player.shield} | Keys: {player.keys_collected}", align="center", font=("Times New Roman", 16, "bold"))

    # Timer settings
    game_time_limit = 120
    start_time = time.time() #capture current time when the game begins .so will start from the beginning

    # displaying the timer
    timer_pen = turtle.Turtle()
    timer_pen.hideturtle()
    timer_pen.penup()
    timer_pen.color("white")
    timer_pen.goto(600, 390)

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
                wn.ontimer(update_timer, 1000)

    # Keyboard bindings for player movements
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
        if not paused:
            return
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
        update_timer()
        global paused
        if not paused:
            if player.distance(monster) < 20:
                if player.keys_collected >= 3:
                    print("Congratulations! You've collected all keys and completed the maze.")
                    player.goto(-320, 320)
                elif player.keys_collected >= 3:
                    open_combat_window(player.fire_power)

         
            interact_obstacles()
            collect_powerups()
            check_for_collision()
            collect_keys()
            interact_with_teleports()
            collect_treasures()
            check_door()
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
    wn.mainloop()

if __name__ == "__main__":
    maze3_main()