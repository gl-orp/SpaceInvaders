# Importing Required Modules
import pygame
import sys

# Initilaizing pygame
# modules
pygame.init()

# Pygame window
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Space Invaders")


# Creating Invader Cclass
class Invader:
    def __init__(self, x, y, invader_type):
        self.type = invader_type
        # File path
        image_path = f"images/Invader_{invader_type}.png"
        self.image = pygame.image.load(image_path).convert_alpha()
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

running = True
# Event handler
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    # drawing invader
    screen.fill((0, 0, 0))
    
    for invader in invaders:
        invader.draw(screen)

    pygame.display.flip()

pygame.quit()
sys.exit()
