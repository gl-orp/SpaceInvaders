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
# --- player bullet class
class PlayerBullet:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 4, 15)
        self.color = (0, 255, 0)  # neon green
        self.speed = 6

    def update(self):
        self.rect.y -= self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

# game variables (use this one as its the combined req1 and req2 ones)
invader_lasers = []
player_bullets = [] # req2
invader_direction = 1
standard_speed = 1
max_speed = 5
drop_distance = 5

player = Player()   # req2
bullet_cooldown = 0 # req2


# --- REQUIREMENT 2 ---
# --- continuous shooting logic (add me into main game loop)

# player movement - draws the player only when alive
    if player.lives > 0:
        player.move(keys)

    # shooting bullets continuously
    if keys[pygame.K_SPACE] and bullet_cooldown <= 0 and player.lives > 0:
        bullet = PlayerBullet(player.rect.centerx, player.rect.top)
        player_bullets.append(bullet)
        bullet_cooldown = 10  # frames between bullets
    if bullet_cooldown > 0:
        bullet_cooldown -= 1

    # move and update player bullets
    for bullet in player_bullets[:]:
        bullet.update()
        if bullet.rect.bottom < 0:
            player_bullets.remove(bullet)
        else:
            # check collision with invaders
            for invader in invaders[:]:
                if bullet.rect.colliderect(invader.rect):
                    invaders.remove(invader)
                    if bullet in player_bullets:
                        player_bullets.remove(bullet)
                    break


# --- REQUIREMENT 2 ---
# --- player being hit by laser + respawn + lives (this should go into game loop after updating lasers)


    elif player.lives > 0 and laser.rect.colliderect(player.rect) and not player.invincible:
        player.lives -= 1
        player.invincible = True
        player.respawn_timer = pygame.time.get_ticks()
        invader_lasers.remove(laser)
        player.rect.midbottom = (WIDTH // 2, HEIGHT - 20)


# --- REQUIREMENT 2 ---
# --- end invincibility after being hit for 2 secs
if player.invincible and pygame.time.get_ticks() - player.respawn_timer > 2000:
    player.invincible = False


    # Draw all elements
    # (cleaner combined draw of req1 and req2)
    for invader in invaders:
        invader.draw(screen)
    for bullet in player_bullets:
        bullet.draw(screen)       # req2
    for laser in invader_lasers:
        laser.draw(screen)
    if player.lives > 0:
        player.draw(screen)       # req 2


# --- REQUIREMENT 2 ---
# --- display player lives
    font = pygame.font.SysFont(None, 30)
    lives_text = font.render(f"Lives: {player.lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))