import os
import sys

def resource_path(relative_path):
    """Get absolute path to resource (works for dev + exe)."""
    try:
        base_path = sys._MEIPASS  # PyInstaller temp folder
    except Exception:
        base_path = os.path.dirname(os.path.abspath(__file__))

    return os.path.join(base_path, relative_path)





import pygame
import math
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
CHARACTER_SIZE = 45
ENEMY_SIZE = 30
LASER_COLOR = (255, 56, 45)
CHARACTER1_COLOR = (80, 255, 25)
CHARACTER2_COLOR = (90, 90, 255)
ENEMY_COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 200, 250)
]
ENEMY_TEXTS = [
    "SINX",
    "COSX",
    "TANX",
    "+",
    "÷",
    "–",
    "1"
]
BACKGROUND_COLOR = (0, 0, 0)
FPS = 30
CHARACTER_SPEED = 5
LASER_LENGTH = 200
LASER_SEGMENTS = 100
LASER_WAVE_AMPLITUDE = 5
LASER_WAVE_FREQUENCY = 100
ENEMY_SPEED = 2
NUM_ENEMIES = 5
ENEMY_SPAWN_INTERVAL = 6000
DEATH_Y = SCREEN_HEIGHT - 10
BUTTON_COLOR = (80, 33, 0)
START_RESTART_HOVER_COLOR = (48,183,0)  # Green hover color for Start and Restart buttons
QUIT_HOVER_COLOR = (200, 0, 0)  # Red hover color for Quit button

BUTTON_FONT_COLOR = (255, 255, 255)
BUTTON_FONT_SIZE = 50
MAX_LASER_DISTANCE = 280
SCORE_FONT_SIZE = 30
ELIMINATED_FONT_SIZE = 20
GAME_OVER_FONT_SIZE = 100
GAME_OVER_COLOR = (204, 0, 0)
GAME_OVER_FONT = pygame.font.Font(None, GAME_OVER_FONT_SIZE)

# Setup the display in fullscreen mode
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("COSMIC IDENTITIES")

BACKGROUND_IMAGE = pygame.image.load(
    resource_path("Images/bg.png")
)

icon_image = pygame.image.load(
    resource_path("Images/icon.png")
)
pygame.display.set_icon(icon_image)
# Load background music and sound effects
# Load additional sound effects
pygame.mixer.music.load(resource_path("Sounds/title song.mp3"))

collision_sound = pygame.mixer.Sound(
    resource_path("Sounds/distortion-bass.mp3")
)

laser_sound = pygame.mixer.Sound(
    resource_path("Sounds/space.mp3")
)
enemy_hit_sound = pygame.mixer.Sound(
    resource_path("Sounds/bass.mp3")
)

# Play background music on a loop
pygame.mixer.music.play(-1)

# Clock for controlling the frame rate
clock = pygame.time.Clock()

# Load fonts
font = pygame.font.Font(None, BUTTON_FONT_SIZE)
score_font = pygame.font.Font(None, SCORE_FONT_SIZE)
eliminated_font = pygame.font.Font(None, ELIMINATED_FONT_SIZE)

def draw_text(surface, text, font, color, rect):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = rect.center
    surface.blit(textobj, textrect)

def show_start_screen():
    screen.fill(BACKGROUND_COLOR)
    
    start_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 250, 50)
    button_hovered = False

    # Check if the mouse is hovering over the start button
    mouse_x, mouse_y = pygame.mouse.get_pos()
    if start_button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, START_RESTART_HOVER_COLOR, start_button_rect, border_radius=25)
        button_hovered = True
    else:
        pygame.draw.rect(screen, BUTTON_COLOR, start_button_rect, border_radius=25)

    draw_text(screen, 'Start Game', font, BUTTON_FONT_COLOR, start_button_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_button_rect.collidepoint(event.pos):
                    waiting = False
                    return True
            if event.type == pygame.MOUSEMOTION:
                # Update hover effect on mouse motion
                if start_button_rect.collidepoint(event.pos):
                    button_hovered = True
                else:
                    button_hovered = False
        
        # Re-render the screen to update hover effect
        if button_hovered:
            pygame.draw.rect(screen, START_RESTART_HOVER_COLOR, start_button_rect, border_radius=25)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, start_button_rect, border_radius=25)
        
        draw_text(screen, 'Start Game', font, BUTTON_FONT_COLOR, start_button_rect)
        pygame.display.flip()

def show_game_over_screen(score, trig_identities):
    screen.fill((0, 0, 0))  # Set a background color or image
    game_over_text = GAME_OVER_FONT.render('Game Over!', True, GAME_OVER_COLOR)
    score_text = score_font.render(f'Score: {score}', True, (255, 255, 255))
    identities_text = score_font.render(f'Identities: {"; ".join(trig_identities)}', True, (255, 255, 255))

    restart_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 60, 200, 50)
    quit_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 10, 200, 50)

    pygame.draw.rect(screen, BUTTON_COLOR, restart_button_rect, border_radius=25)
    pygame.draw.rect(screen, BUTTON_COLOR, quit_button_rect, border_radius=25)
    draw_text(screen, 'Restart', font, BUTTON_FONT_COLOR, restart_button_rect)
    draw_text(screen, 'Quit', font, BUTTON_FONT_COLOR, quit_button_rect)

    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 100))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - score_text.get_height() // 2 + 20))
    screen.blit(identities_text, (SCREEN_WIDTH // 2 - identities_text.get_width() // 2, SCREEN_HEIGHT  /10+120))
    
    pygame.display.flip()

    return restart_button_rect, quit_button_rect

def compute_trig_identity(eliminated_enemies):
    counts = {text: eliminated_enemies.count(text) for text in ENEMY_TEXTS}
    
    identities = []
    
    if counts.get("SINX") == 2 and counts.get("COSX") == 2 and counts.get("+") == 1:
        identities.append("sin²x + cos²x = 1")
    
    elif counts.get("1") == 1 and counts.get("TANX") == 2 and counts.get("+") == 1:
        identities.append("1 + tan²x = sec²x")

    elif counts.get("1") == 2 and counts.get("÷") == 1 and counts.get("TANX") == 2 and counts.get("+") ==1:
       identities.append("1 + cot²x = cosec²x")
    
    elif counts.get("SINX") ==1  and counts.get("COSX") == 1 and counts.get("1") == 2 and counts.get("+") ==1:
       identities.append("sin2x=2sinx.cosx")
    elif counts.get("1") == 3 and counts.get("–") == 1 and counts.get("SINX") == 2 and counts.get("+")==1:
       identities.append("cos2x=1-2sin²x")
    
    elif counts.get("1") == 3 and counts.get("–") == 1 and counts.get("COSX") == 2 and counts.get("+")==1 :
       identities.append("cos2x=2cos²x-1")
   
    elif counts.get("1") == 7 and counts.get("–") == 1 and counts.get("SINX") == 4 and counts.get("+")==5 :
       identities.append("sin3x=3sinx-4sin³x")
   
    elif counts.get("1") == 7 and counts.get("–") == 1 and counts.get("COSX") == 4 and counts.get("+")==5:
       identities.append("cos3x=4cos³x-3cosx") 

    elif counts.get("COSX") == 2 and counts.get("–") == 1 and counts.get("SINX") == 2 :
       identities.append("cos2x=cos²x-sin²x")

    if not identities:
        identities.append("No significant identities")

    return identities

def select_random_identity():
    possible_identities = [
        "1 = ?",
        "sec²x = ?",
        "cosec²x = ?",
        "sin2x = ?",
        "sin3x = ?",
        "cos3x = ?",
        "cos2x = ?"
    ]
    return random.choice(possible_identities)


def check_identity_match(eliminated_enemies, target_identity):
    trig_identities = compute_trig_identity(eliminated_enemies)
    return target_identity in trig_identities

def draw_eliminated_enemies(surface, eliminated_enemies):
    eliminated_text = "Eliminated: " + " ".join(eliminated_enemies)
    textobj = eliminated_font.render(eliminated_text, True, (255, 255, 255))
    surface.blit(textobj, (10, 10))

class Character(pygame.sprite.Sprite):
    def __init__(self, color, start_x, start_y):
        super().__init__()
        self.radius = CHARACTER_SIZE // 2
        self.image = pygame.Surface((CHARACTER_SIZE, CHARACTER_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect(center=(start_x, start_y))
        self.speed = CHARACTER_SPEED
        self.pivot = self.rect.center

    def update(self, keys, move_keys):
        if keys[move_keys[0]]:
            self.rect.x -= self.speed
        if keys[move_keys[1]]:
            self.rect.x += self.speed
        if keys[move_keys[2]]:
            self.rect.y -= self.speed
        if keys[move_keys[3]]:
            self.rect.y += self.speed

        # Keep the character within screen bounds
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

        self.pivot = self.rect.center

    def is_dead(self):
        return self.rect.bottom >= DEATH_Y

    def check_collision_with_enemy(self, enemies):
        for enemy in enemies:
            if pygame.sprite.collide_circle(self, enemy):
                return True
        return False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, text, font, color):
        super().__init__()
        # Font size setup for each enemy type
        self.front_sizes = {
            "SINX": 32,
            "COSX": 32,
            "TANX": 32,
            "+": 50,
            "÷": 50,
            "–": 40,
            "1": 40
        }
        self.font = pygame.font.Font(None, self.front_sizes.get(text, 36))
        self.color = color
        self.text = text
        self.image = self.font.render(self.text, True, self.color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - self.rect.height)
        self.speed = ENEMY_SPEED
        self.alive = True
        self.direction = self.get_random_direction()

    def get_random_direction(self):
        return random.choice([(-1, 0), (1, 0), (0, -1), (0, 1)])

    def update(self):
        if self.alive:
            self.rect.x += self.direction[0] * self.speed
            self.rect.y += self.direction[1] * self.speed

            if self.rect.left < 0 or self.rect.right > SCREEN_WIDTH:
                self.direction = (-self.direction[0], self.direction[1])
            if self.rect.top < 0 or self.rect.bottom > SCREEN_HEIGHT:
                self.direction = (self.direction[0], -self.direction[1])

            if random.random() < 0.02:
                self.direction = self.get_random_direction()

    def check_laser_hit(self, laser_positions):
        return any(pygame.Rect(pos[0] - self.rect.width // 2, pos[1] - self.rect.height // 2, self.rect.width, self.rect.height).colliderect(self.rect) for pos in laser_positions)

class Laser:
    def __init__(self, char1, char2, segments):
        self.char1 = char1
        self.char2 = char2
        self.segments = segments
        self.segments_pos = [(0, 0)] * segments

    def update(self):
        pass

    def draw(self, screen):
        x1, y1 = self.char1.pivot
        x2, y2 = self.char2.pivot
        dx = x2 - x1
        dy = y2 - y1
        distance = math.sqrt(dx**2 + dy**2)

        if distance > MAX_LASER_DISTANCE:
            return

        angle = math.atan2(dy, dx)
        for i in range(self.segments):
            t = i / (self.segments - 1)
            x = x1 + t * dx
            y = y1 + t * dy
            wave_offset = LASER_WAVE_AMPLITUDE * math.sin(LASER_WAVE_FREQUENCY * t * distance)
            wave_x = x + wave_offset * math.cos(angle + math.pi / 2)
            wave_y = y + wave_offset * math.sin(angle + math.pi / 2)
            if i > 0:
                prev_x, prev_y = self.segments_pos[i - 1]
                pygame.draw.line(screen, LASER_COLOR, (prev_x, prev_y), (wave_x, wave_y), 2)
            self.segments_pos[i] = (wave_x, wave_y)

def main_game():
    pygame.mixer.music.play(-1)  # Play background music indefinitely

    global NUM_ENEMIES
    enemy_font = pygame.font.Font(None, 36)

    char1 = Character(CHARACTER1_COLOR, SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)
    char2 = Character(CHARACTER2_COLOR, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    enemies = pygame.sprite.Group()
    for _ in range(NUM_ENEMIES):
        text, color = random.choice(list(zip(ENEMY_TEXTS, ENEMY_COLORS)))
        enemy = Enemy(text, enemy_font, color)
        enemies.add(enemy)

    laser = Laser(char1, char2, LASER_SEGMENTS)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(char1)
    all_sprites.add(char2)
    all_sprites.add(enemies)

    spawn_timer = pygame.time.get_ticks()
    eliminated_enemies = []

    target_identity = select_random_identity()  # Select and display a random identity

    def restart_game():
        pygame.mixer.music.play(-1)
        nonlocal eliminated_enemies, target_identity
        eliminated_enemies = []
        target_identity = select_random_identity()  # Select a new random identity
        char1.rect.center = (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2)
        char2.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        enemies.empty()
        all_sprites.empty()
        for _ in range(NUM_ENEMIES):
            text, color = random.choice(list(zip(ENEMY_TEXTS, ENEMY_COLORS)))
            enemy = Enemy(text, enemy_font, color)
            enemies.add(enemy)
            all_sprites.add(enemy)
        all_sprites.add(char1)
        all_sprites.add(char2)
        laser.__init__(char1, char2, LASER_SEGMENTS)  # Reinitialize the laser

    # Show start screen
    if not show_start_screen():
        pygame.quit()
        return

    running = True
    while running:
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        char1.update(keys, [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s])
        char2.update(keys, [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN])
        enemies.update()

        if char1.check_collision_with_enemy(enemies) or char2.check_collision_with_enemy(enemies):
            # Play the collision sound effect
            collision_sound.play()

            # Check if the eliminated enemies satisfy any winning condition
            counts = {text: eliminated_enemies.count(text) for text in ENEMY_TEXTS}
            if (
                (counts.get("SINX") == 2 and counts.get("COSX") == 2 and counts.get("+") == 1) or
                (counts.get("1") == 1 and counts.get("TANX") == 2 and counts.get("+") == 1) or
                (counts.get("1") == 2 and counts.get("÷") == 1 and counts.get("TANX") == 2 and counts.get("+") == 1) or
                (counts.get("SINX") == 1 and counts.get("COSX") == 1 and counts.get("1") == 2 and counts.get("+") == 1) or
                (counts.get("1") == 3 and counts.get("–") == 1 and counts.get("SINX") == 2 and counts.get("+") == 1) or
                (counts.get("1") == 3 and counts.get("–") == 1 and counts.get("COSX") == 2 and counts.get("+") == 1) or
                (counts.get("1") == 7 and counts.get("–") == 1 and counts.get("SINX") == 4 and counts.get("+") == 5) or
                (counts.get("1") == 7 and counts.get("–") == 1 and counts.get("COSX") == 4 and counts.get("+") == 5) or
                (counts.get("COSX") == 2 and counts.get("–") == 1 and counts.get("SINX") == 2)
            ):
                screen.fill(BACKGROUND_COLOR)
                win_text = font.render('You Win!  ^_^ ', True, (0, 255, 0))
                identity_text = score_font.render(f'Target Identity: {target_identity}', True, (255, 255, 255))
                screen.blit(BACKGROUND_IMAGE, (0, 0))  # Draw the background image
                screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - win_text.get_height() // 2 - 30))
                screen.blit(identity_text, (SCREEN_WIDTH // 2 - identity_text.get_width() // 2, SCREEN_HEIGHT // 2 + 10))
                pygame.display.flip()
                pygame.time.wait(10000)  # Wait t seconds before restarting 
                continue

            restart_button_rect, quit_button_rect = show_game_over_screen(0, compute_trig_identity(eliminated_enemies))
            pygame.mixer.music.stop()
            game_over = True
            while game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if restart_button_rect.collidepoint(event.pos):
                            restart_game()
                            game_over = False
                        if quit_button_rect.collidepoint(event.pos):
                            pygame.quit()
                            return
                # Button hover effect
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if restart_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, START_RESTART_HOVER_COLOR, restart_button_rect, border_radius=25)
                else:
                    pygame.draw.rect(screen, BUTTON_COLOR, restart_button_rect, border_radius=25)
                
                if quit_button_rect.collidepoint(mouse_x, mouse_y):
                    pygame.draw.rect(screen, QUIT_HOVER_COLOR, quit_button_rect, border_radius=25)
                else:
                    pygame.draw.rect(screen, BUTTON_COLOR, quit_button_rect, border_radius=25)
                
                draw_text(screen, 'Restart', font, BUTTON_FONT_COLOR, restart_button_rect)
                draw_text(screen, 'Quit', font, BUTTON_FONT_COLOR, quit_button_rect)
                
                pygame.display.flip()

        screen.blit(BACKGROUND_IMAGE, (0, 0))  # Draw the background image
        laser.update()
        laser_positions = laser.segments_pos
        for enemy in enemies:
            if enemy.check_laser_hit(laser_positions):
                enemies.remove(enemy)
                all_sprites.remove(enemy)
                eliminated_enemies.append(enemy.text)
                enemy_hit_sound.play()  # Play the sound effect when an enemy is hit

        all_sprites.draw(screen)
        laser.draw(screen)
        
        # Display the target identity on the screen
        target_identity_text = score_font.render(f'Target Identity: {target_identity}', True, (255, 255, 255))
        screen.blit(target_identity_text, (10, SCREEN_HEIGHT - 40))
        
        # Display the eliminated enemies at the top
        draw_eliminated_enemies(screen, eliminated_enemies)
        
        pygame.display.flip()

        now = pygame.time.get_ticks()
        if now - spawn_timer > ENEMY_SPAWN_INTERVAL:
            text, color = random.choice(list(zip(ENEMY_TEXTS, ENEMY_COLORS)))
            new_enemy = Enemy(text, enemy_font, color)
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            spawn_timer = now

        clock.tick(FPS)



# Start the game
main_game()
pygame.quit()
