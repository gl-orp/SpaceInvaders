# --- PLAYER CAN SHOOT MULTIPLE BULLETS CONTINUOUSLY ---

if keys[pygame.K_SPACE] and bullet_cooldown <= 0 and player.lives > 0:
    bullet = PlayerBullet(player.rect.centerx, player.rect.top)
    player_bullets.append(bullet)
    bullet_cooldown = 10  # fire rate
if bullet_cooldown > 0:
    bullet_cooldown -= 1

# move bullets + remove off-screen bullets
for bullet in player_bullets[:]:
    bullet.update()
    if bullet.rect.bottom < 0:
        player_bullets.remove(bullet)


# --- PLAYER BULLETS DESTROY INVADERS ---
new_player_bullets = []
for b in player_bullets:
    hit = False
    for inv in invaders:
        if inv.alive and inv.rect.collidepoint(b['x'], b['y']):
            inv.alive = False
            hit = True
            break
    if not hit:
        new_player_bullets.append(b)
player_bullets = new_player_bullets



# --- INVADERS SHOOT BULLETS ---

if random.randint(1, 50) == 1:  # roughly 1 laser per sec
    shooter = random.choice(invaders)
    laser = InvaderLaser(shooter.rect.centerx, shooter.rect.bottom)
    invader_lasers.append(laser)


# Move invader bullets
for b in invader_bullets:
    b["y"] += invader_bullet_speed
invader_bullets = [b for b in invader_bullets if b["y"] < HEIGHT]


# --- INVADER BULLETS HIT PLAYER (PLAYER LOSES LIFE) ---
for laser in invader_lasers[:]:
    if player_x < laser.rect.centerx < player_x + player_w and player_y < laser.rect.centery < player_y + player_h:
        lives -= 1
        invader_lasers.remove(laser)
        player_x = WIDTH // 2 - player_w // 2
        if lives <= 0:
            running = False


# --- DRAW PLAYER ---
pygame.draw.rect(screen, (0, 255, 0), (player_x, player_y, player_w, player_h))

# --- DRAW PLAYER BULLETS ---
for b in player_bullets:
    pygame.draw.rect(screen, (255, 255, 0), (b["x"]-2, b["y"], 4, 10))

