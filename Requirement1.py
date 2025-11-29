# Importing Required Modules
import pygame
import sys

# Initilaizing pygame
# modules
pygame.init()

# Pygame window
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption("Space Invaders")

running = True
# Event handler
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
    
    screen.fill((0, 0, 0))
    pygame.display.flip()

pygame.quit()
sys.exit()
