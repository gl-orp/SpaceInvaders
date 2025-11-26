import pygame
import random

pygame.init()

# --- WINDOW SETUP ---
WIDTH, HEIGHT = 640, 480
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")
clock = pygame.time.Clock()

# --- COLORS & FONT ---
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)
FONT = pygame.font.SysFont(None, 30)

# --- PLAYER SETUP ---
player_w, player_h = 40, 20
player_x = WIDTH // 2 - player_w // 2
player_y = HEIGHT - 50
player_speed = 5
lives = 3
player_bullets = []
bullet_speed = -7

# --- INVADERS ---
class Invader:
    def __init__(self, x, y, w, h, points, fire_chance):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.points, self.fire_chance = points, fire_chance
        self.alive = True
    def rect(self):
        return pygame.Rect(self.x, self.y, self.w, self.h)

class Squid(Invader):
    def __init__(self, x, y):
        super().__init__(x, y, 26, 18, 30, 0.0015)
class Crab(Invader):
    def __init__(self, x, y):
        super().__init__(x, y, 30, 20, 20, 0.002)
class Octopus(Invader):
    def __init__(self, x, y):
        super().__init__(x, y, 34, 24, 10, 0.001)

# Build invader grid
invaders = []
rows, cols = 5, 10
x_margin, y_margin = 60, 40
x_spacing, y_spacing = 40, 35
for r in range(rows):
    for c in range(cols):
        x = x_margin + c * x_spacing
        y = y_margin + r * y_spacing
        if r == 0: invaders.append(Squid(x, y))
        elif r in (1, 2): invaders.append(Crab(x, y))
        else: invaders.append(Octopus(x, y))

invader_dir = 1
invader_speed = 1
move_down = False
invader_bullets = []
invader_bullet_speed = 4

# --- BARRIERS WITH MASKS ---
barrier_w, barrier_h = 60, 40
barrier_y = HEIGHT - 130
barriers = []
for i in range(4):
    bx = 60 + i*140
    surf = pygame.Surface((barrier_w, barrier_h))
    surf.fill(BLACK)
    mask = [[0]*barrier_w for _ in range(barrier_h)]
    thickness = 8
    # top arch
    for y in range(thickness):
        for x in range(barrier_w):
            surf.set_at((x, y), GREEN)
            mask[y][x] = 1
    # left pillar
    for y in range(barrier_h):
        for x in range(thickness):
            surf.set_at((x, y), GREEN)
            mask[y][x] = 1
    # right pillar
    for y in range(barrier_h):
        for x in range(barrier_w-thickness, barrier_w):
            surf.set_at((x, y), GREEN)
            mask[y][x] = 1
    barriers.append({"x": bx, "y": barrier_y, "surf": surf, "mask": mask})

# --- EROSION FUNCTION ---
def erode_pixel(barrier, x, y):
    radius = 8
    mask = barrier['mask']
    surf = barrier['surf']
    for dy in range(-radius, radius+1):
        for dx in range(-radius, radius+1):
            if dx*dx + dy*dy <= radius*radius:
                px, py = int(x+dx), int(y+dy)
                if 0 <= px < barrier_w and 0 <= py < barrier_h:
                    mask[py][px] = 0
                    surf.set_at((px, py), BLACK)

# --- BULLET-BARRIER COLLISION ---
def handle_barrier_collision(bullets):
    new_bullets = []
    for b in bullets:
        hit = False
        for barrier in barriers:
            bx, by = barrier['x'], barrier['y']
            if bx <= b["x"] < bx+barrier_w and by <= b["y"] < by+barrier_h:
                mx, my = int(b["x"]-bx), int(b["y"]-by)
                if 0 <= mx < barrier_w and 0 <= my < barrier_h:
                    if barrier['mask'][my][mx]:
                        erode_pixel(barrier, mx, my)
                        hit = True
                        break
        if not hit:
            new_bullets.append(b)
    return new_bullets

# --- GAME LOOP ---
cooldown = 0
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]: player_x -= player_speed
    if keys[pygame.K_RIGHT]: player_x += player_speed
    if keys[pygame.K_SPACE] and cooldown <= 0:
        player_bullets.append({"x": player_x + player_w//2, "y": player_y})
        cooldown = 10
    cooldown = max(cooldown-1, 0)

    player_x = max(0, min(WIDTH-player_w, player_x))

    # --- MOVE BULLETS ---
    for b in player_bullets: b["y"] += bullet_speed
    player_bullets = [b for b in player_bullets if b["y"] > 0]

    for b in invader_bullets: b["y"] += invader_bullet_speed
    invader_bullets = [b for b in invader_bullets if b["y"] < HEIGHT]

    # --- BULLET COLLISION WITH BARRIERS ---
    player_bullets = handle_barrier_collision(player_bullets)
    invader_bullets = handle_barrier_collision(invader_bullets)

    # --- INVADER MOVEMENT ---
    xs = [inv.x for inv in invaders if inv.alive]
    if xs:
        leftmost = min(xs)
        rightmost = max(xs) + 34
        if leftmost <= 0 or rightmost >= WIDTH:
            invader_dir *= -1
            move_down = True
    for inv in invaders:
        if inv.alive:
            inv.x += invader_dir * invader_speed
            if move_down: inv.y += 12
    move_down = False

    # --- INVADER FIRING ---
    for inv in invaders:
        if inv.alive and random.random() < inv.fire_chance:
            invader_bullets.append({"x": inv.x + inv.w//2, "y": inv.y + inv.h})

    # --- PLAYER BULLETS HITTING INVADERS ---
    new_player_bullets = []
    for b in player_bullets:
        hit = False
        for inv in invaders:
            if inv.alive and inv.rect().collidepoint(b['x'], b['y']):
                inv.alive = False
                hit = True
                break
        if not hit:
            new_player_bullets.append(b)
    player_bullets = new_player_bullets

    # --- INVADER SPEED ADJUSTMENT ---
    alive_count = sum(inv.alive for inv in invaders)
    invader_speed = 1 + (rows*cols - alive_count)*0.02

    # --- INVADER BULLETS HITTING PLAYER ---
    for b in invader_bullets:
        if player_x < b["x"] < player_x+player_w and player_y < b["y"] < player_y+player_h:
            lives -= 1
            b["y"] = HEIGHT+9999
            player_x = WIDTH//2 - player_w//2
            if lives <= 0:
                running = False

    # --- DRAW ---
    screen.fill(BLACK)
    pygame.draw.rect(screen, GREEN, (player_x, player_y, player_w, player_h))

    for b in player_bullets:
        pygame.draw.rect(screen, WHITE, (b["x"], b["y"], 3, 10))
    for b in invader_bullets:
        pygame.draw.rect(screen, RED, (b["x"], b["y"], 3, 10))

    for inv in invaders:
        if inv.alive:
            pygame.draw.rect(screen, WHITE, inv.rect())

    for barrier in barriers:
        screen.blit(barrier["surf"], (barrier["x"], barrier["y"]))

    lives_text = FONT.render(f"Lives: {lives}", True, WHITE)
    screen.blit(lives_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
