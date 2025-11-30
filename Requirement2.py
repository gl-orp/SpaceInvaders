

# --- PLAYER CAN SHOOT MULTIPLE BULLETS CONTINUOUSLY ---

player_bullets = []
bullet_speed = -7
cooldown = 0

# Shooting
if keys[pygame.K_SPACE] and cooldown <= 0:
    player_bullets.append({"x": player_x + player_w//2, "y": player_y})
    cooldown = 10
cooldown = max(cooldown-1, 0)

# Move bullets
for b in player_bullets:
    b["y"] += bullet_speed
player_bullets = [b for b in player_bullets if b["y"] > 0]


# --- PLAYER BULLETS DESTROY INVADERS ---

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


# --- INVADERS SHOOT BULLETS ---

invader_bullets = []
invader_bullet_speed = 4

# Invader firing
for inv in invaders:
    REDUCED_CHANCE = inv.fire_chance * 0.62
    if inv.alive and random.random() < REDUCED_CHANCE:
        invader_bullets.append({"x": inv.x + inv.w//2, "y": inv.y + inv.h})

# Move invader bullets
for b in invader_bullets:
    b["y"] += invader_bullet_speed
invader_bullets = [b for b in invader_bullets if b["y"] < HEIGHT]


# --- INVADER BULLETS HIT PLAYER (PLAYER LOSES LIFE) ---
for b in invader_bullets:
    if player_x < b["x"] < player_x + player_w and player_y < b["y"] < player_y + player_h:
        lives -= 1
        b["y"] = HEIGHT + 9999
        player_x = WIDTH // 2 - player_w // 2
        if lives <= 0:
            running = False