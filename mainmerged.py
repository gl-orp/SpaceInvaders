# Importing Required Modules
import pygame
import sys
import random

# Intialising pygame modules
pygame.init()

# Window settings
WIDTH = 600
HEIGHT = 600
# Pygame window and clock
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")


# --- REQUIREMENT 2 ---
# Player class
class Player:
    def __init__(self):
        self.image = pygame.image.load("images/Player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 30))
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
        self.speed = 5
        self.lives = 3
        self.respawn_timer = 0
        self.invincible = False

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += self.speed

    def draw(self, surface):
        if not self.invincible or (pygame.time.get_ticks() // 250) % 2 == 0:  # blink when invincible
            surface.blit(self.image, self.rect)


# --- REQUIREMENT 2 ---
# --- Player bullet class
class PlayerBullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 4, 15)
        self.color = (0, 255, 0)  # neon green
        self.speed = 6

    def update(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)


# Creating Invader Cclass
class Invader:
    def __init__(self, x, y, invader_type):
        self.type = invader_type
        # File path
        image_path = f"images/Invader_{invader_type}.png"
        self.image = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 25))
        # Rect for position
        self.rect = self.image.get_rect(topleft=(x, y))

        # Adding mirror values
        # for Requirement 2
        # compatability.
        self.x = x
        self.y = y
        self.w = 30
        self.h = 25
        # Requirement 2
        # compatability
        self.alive = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Creatung InvaderLaser
# class
class InvaderLaser:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 4, 15)
        self.color = (159, 51, 52) # Red Orche
        self.speed = 4
    
    def update(self):
        self.rect.y += self.speed
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# Creating Invader Grid

invaders = []

ROWS = 5
COLUMNS = 11

START_X = 50
START_Y = 50
GAP_X = 45
GAP_Y = 40

# Invader grid (rrows * column)
for row in range(ROWS):
    for col in range(COLUMNS):
        # Calculation of the position
        # for each invader in the grid.
        x = START_X + col * GAP_X
        y = START_Y + row * GAP_Y

        # invader type based on row number
        if row == 0:
            invader_type = 3
        elif row == 1 or row == 2:
            invader_type = 2
        else:
            invader_type = 1
        invader = Invader(x, y, invader_type)
        invaders.append(invader)
        
# Game variables (merged req1 and req2)
invader_lasers = []
player_bullets = [] # req2
invader_direction = 1
standard_speed = 1
max_speed = 5
drop_distance = 5

player = Player()   # req2
bullet_cooldown = 0 # req2

running = True
while running:
    clock.tick(60) # Limit FPS==60
    screen.fill((0,0,0))
    keys = pygame.key.get_pressed()


    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

# --- REQUIREMENT 2 ---

    # Player movement
    if player.lives > 0:
        player.move(keys)

    # Shooting bullets continuously
    if keys[pygame.K_SPACE] and bullet_cooldown <= 0 and player.lives > 0:
        bullet = PlayerBullet(player.rect.centerx, player.rect.top)
        player_bullets.append(bullet)
        bullet_cooldown = 10  # frames between bullets
    if bullet_cooldown > 0:
        bullet_cooldown -= 1

    # Move and update player bullets
    for bullet in player_bullets[:]:
        bullet.update()
        if bullet.rect.bottom < 0:
            player_bullets.remove(bullet)
        else:
            # Check collision with invaders
            for invader in invaders[:]:
                if bullet.rect.colliderect(invader.rect):
                    invaders.remove(invader)
                    if bullet in player_bullets:
                        player_bullets.remove(bullet)
                    break   
# ------------------------------------------------------------------------

    # How many invaders
    # are left and setting
    # speed based on invaders
    alive_count = len(invaders)
    invader_speed = standard_speed + (max_speed - standard_speed) * (1 - (alive_count / (ROWS * COLUMNS)))

    # drawing invader
    screen.fill((0, 0, 0))

    # move invader horizontally
    for invader in invaders:
        if invader.alive:
            invader.rect.x += invader_direction * invader_speed
            # Adding updates for
            # Requirement 2
            # compatability.
            invader.x = invader.rect.x
            invader.y = invader.rect.y
    
    # checking windows edges
    hit_edge = False
    for invader in invaders:
        if invader.rect.right >= 600 or invader.rect.left <= 0:
            hit_edge = True
            break
    
    # Reverse detection
    if hit_edge:
        invader_direction *= -1
        for invader in invaders:
            # Added for req 2
            if invader.alive:
                invader.rect.y += drop_distance
                invader.x = invader.rect.x
                invader.y = invader.rect.y


    
    # random invader firing
    if random.randint(1, 50) == 1: # 1 laser/sec
        shooter = random.choice(invaders)
        laser_x = shooter.rect.centerx
        laser_y = shooter.rect.bottom
        laser = InvaderLaser(laser_x, laser_y)
        invader_lasers.append(laser)
    
    # updating lasers, move downwards   
    for laser in invader_lasers[:]:
        laser.update()
        # Removing laser
        # when it leaves
        # screen
        if laser.rect.top > 600:
            invader_lasers.remove(laser)
        elif player.lives > 0 and laser.rect.colliderect(player.rect) and not player.invincible:
            player.lives -= 1
            player.invincible = True
            player.respawn_timer = pygame.time.get_ticks()
            invader_lasers.remove(laser)
            player.rect.midbottom = (WIDTH // 2, HEIGHT - 20)

    # End invincibility after 2 seconds
    if player.invincible and pygame.time.get_ticks() - player.respawn_timer > 2000:
        player.invincible = False

    # Draw all elements
    for invader in invaders:
        invader.draw(screen)
    for bullet in player_bullets:
        bullet.draw(screen)
    for laser in invader_lasers:
        laser.draw(screen)
    if player.lives > 0:
        player.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
