# Importing Required Modules
import pygame
import sys

# Initilaizing pygame
# modules
pygame.init()

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
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

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

# Movemnt
invader_direction = 1
invader_speed = 1

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
    # drawing invader
    screen.fill((0, 0, 0))

    # move invader horizontally
    for invader in invaders:
        invader.rect.x += invader_direction * invader_speed
    
    # checking windows edges
    hit_edge = False
    for invader in invaders:
        if invader.rect.right >= 600 or invader.rect.left <= 0:
            hit_edge = True
            break
    
    # Reverse detection
    if hit_edge:
        invader_direction *= -1
    
    # Draw invaders
    for invader in invaders:
        invader.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
