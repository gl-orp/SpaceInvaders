# Importing Required Modules
import pygame
import sys
import random

# Initilaizing pygame
# modules
pygame.init()
# Requirement 2
# merge prep
WIDTH = 600
HEIGHT = 600

# Pygame window and Clock
screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()
pygame.display.set_caption("Space Invaders")


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
        
# Game Variables
invader_lasers = []
# Requirement 2
# merge prep
player_bullets = []
cooldown = 0

# Movemnt
invader_direction = 1
invader_speed = 1
drop_distance = 5
# Speed increaments
standard_speed = 1
max_speed = 5

running = True
# Event handler
while running:
    clock.tick(60) # Limit FPS==60
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

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
     
    # Draw invaders
    for invader in invaders:
        # Added for Requirement 2
        if invader.alive:
            invader.draw(screen)
    
    # Draw invader lasers
    for laser in invader_lasers:
        laser.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
