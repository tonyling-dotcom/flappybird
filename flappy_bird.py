import pygame
import sys
import json
import random
import os
import math
from pygame import mixer

# Initialize Pygame
pygame.init()
mixer.init()

# Load configuration
with open('levels.json', 'r') as f:
    config = json.load(f)

game_settings = config['game_settings']
levels = config['levels']

# Screen setup
SCREEN_WIDTH = game_settings['screen_width']
SCREEN_HEIGHT = game_settings['screen_height']
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird - City Edition')

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
BUILDING_COLORS = [
    (100, 149, 237),  # Cornflower blue
    (255, 127, 80),   # Coral
    (144, 238, 144),  # Light green
    (255, 218, 185),  # Peach
    (221, 160, 221),  # Plum
]

# Load high score
HIGH_SCORE_FILE = 'highscore.json'

def load_high_score():
    if os.path.exists(HIGH_SCORE_FILE):
        with open(HIGH_SCORE_FILE, 'r') as f:
            return json.load(f).get('high_score', 0)
    return 0

def save_high_score(score):
    with open(HIGH_SCORE_FILE, 'w') as f:
        json.dump({'high_score': score}, f)

# Load and scale images
def load_image(path, size):
    image = pygame.image.load(path)
    return pygame.transform.scale(image, size)

player_img = load_image('assets/images/player.png', (game_settings['player_size'], game_settings['player_size']))
enemy_img = load_image('assets/images/enemy.png', (game_settings['enemy_size'], game_settings['enemy_size']))
background_original = pygame.image.load('assets/images/map.png')
background = pygame.transform.scale(background_original, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Create blurred background
def create_blurred_background():
    blur_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    blur_surface.blit(background, (0, 0))
    blur_surface.set_alpha(180)
    return blur_surface

blurred_bg = create_blurred_background()

# Load sounds
def load_sound(path):
    try:
        return mixer.Sound(path)
    except:
        return None

flap_sound = load_sound('assets/audio/flap.mp3')
enemy_sound = load_sound('assets/audio/enemy.mp3')
gameover_sound = load_sound('assets/audio/gameover.mp3')

# Background music
try:
    mixer.music.load('assets/audio/bg.mp3')
    mixer.music.set_volume(0.3)
except:
    pass

# Fonts
font_large = pygame.font.Font(None, 72)
font_medium = pygame.font.Font(None, 48)
font_small = pygame.font.Font(None, 36)

class Player:
    def __init__(self):
        self.x = 150
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.size = game_settings['player_size']
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.angle = 0
        self.started = False
        
    def flap(self):
        self.velocity = game_settings['flap_strength']
        self.started = True
        if flap_sound:
            flap_sound.play()
    
    def update(self):
        if self.started:
            self.velocity += game_settings['gravity']
            self.y += self.velocity
        
        # Update angle based on velocity
        self.angle = max(-30, min(30, -self.velocity * 3))
        
        # Keep player on screen
        if self.y < 0:
            self.y = 0
            self.velocity = 0
        if self.y > SCREEN_HEIGHT - self.size:
            self.y = SCREEN_HEIGHT - self.size
            self.velocity = 0
        
        self.rect.y = self.y
    
    def draw(self, surface):
        rotated = pygame.transform.rotate(player_img, self.angle)
        rect = rotated.get_rect(center=(self.x + self.size//2, self.y + self.size//2))
        surface.blit(rotated, rect)
    
    def reset(self):
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
        self.started = False

class Wall:
    def __init__(self, x, gap_y, gap_height, speed):
        self.x = x
        self.gap_y = gap_y
        self.gap_height = gap_height
        self.width = game_settings['wall_width']
        self.speed = speed
        self.passed = False
        self.color = random.choice(BUILDING_COLORS)
        
    def update(self):
        self.x -= self.speed
    
    def draw(self, surface):
        # Top building (wall)
        top_height = self.gap_y
        self.draw_building(surface, self.x, 0, self.width, top_height)
        
        # Bottom building (wall)
        bottom_y = self.gap_y + self.gap_height
        bottom_height = SCREEN_HEIGHT - bottom_y
        self.draw_building(surface, self.x, bottom_y, self.width, bottom_height)
    
    def draw_building(self, surface, x, y, width, height):
        # Main building body
        pygame.draw.rect(surface, self.color, (x, y, width, height))
        # Building outline
        pygame.draw.rect(surface, BLACK, (x, y, width, height), 3)
        
        # Windows
        window_size = 8
        window_spacing = 15
        for wx in range(int(x + 10), int(x + width - 10), window_spacing):
            for wy in range(int(y + 10), int(y + height - 10), window_spacing):
                window_color = (255, 255, 200) if random.random() > 0.3 else (50, 50, 70)
                pygame.draw.rect(surface, window_color, (wx, wy, window_size, window_size))
    
    def collides_with(self, player):
        player_rect = pygame.Rect(player.x + 10, player.y + 10, player.size - 20, player.size - 20)
        top_rect = pygame.Rect(self.x, 0, self.width, self.gap_y)
        bottom_rect = pygame.Rect(self.x, self.gap_y + self.gap_height, self.width, SCREEN_HEIGHT)
        return player_rect.colliderect(top_rect) or player_rect.colliderect(bottom_rect)
    
    def is_off_screen(self):
        return self.x + self.width < 0

class Enemy:
    def __init__(self, level_config):
        self.x = SCREEN_WIDTH + 50
        self.y = random.randint(100, SCREEN_HEIGHT - 100)
        self.size = game_settings['enemy_size']
        self.speed = level_config['enemy_speed']
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.wave_offset = random.random() * 10
        self.wave_amplitude = 30
        self.wave_frequency = 0.05
        self.original_y = self.y
        self.last_shot_time = pygame.time.get_ticks()
        self.shoot_interval = level_config['enemy_shoot_interval']
        self.projectile_speed = level_config['projectile_speed']
        
    def update(self, frame_count):
        self.x -= self.speed
        # Flying motion - sine wave
        self.y = self.original_y + self.wave_amplitude * math.sin(
            (frame_count + self.wave_offset) * self.wave_frequency
        )
        self.rect.x = self.x
        self.rect.y = self.y
    
    def can_shoot(self, current_time, player):
        # Only shoot if enemy is on screen and player is visible
        if self.x > SCREEN_WIDTH or self.x < -self.size:
            return False
        if current_time - self.last_shot_time > self.shoot_interval:
            # Only shoot if player is somewhat in front (to the left)
            if self.x > player.x:
                return True
        return False
    
    def shoot(self, player):
        self.last_shot_time = pygame.time.get_ticks()
        # Create projectile from enemy center toward player center
        start_x = self.x + self.size // 2
        start_y = self.y + self.size // 2
        target_x = player.x + player.size // 2
        target_y = player.y + player.size // 2
        return Projectile(start_x, start_y, target_x, target_y, self.projectile_speed)
    
    def draw(self, surface):
        surface.blit(enemy_img, (self.x, self.y))
    
    def collides_with(self, player):
        player_rect = pygame.Rect(player.x + 10, player.y + 10, player.size - 20, player.size - 20)
        enemy_rect = pygame.Rect(self.x + 10, self.y + 10, self.size - 20, self.size - 20)
        return player_rect.colliderect(enemy_rect)
    
    def is_off_screen(self):
        return self.x + self.size < 0

class Projectile:
    def __init__(self, start_x, start_y, target_x, target_y, speed):
        self.x = start_x
        self.y = start_y
        self.size = game_settings['projectile_size']
        self.speed = speed
        
        # Calculate direction vector
        dx = target_x - start_x
        dy = target_y - start_y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Normalize and multiply by speed
        if distance > 0:
            self.velocity_x = (dx / distance) * speed
            self.velocity_y = (dy / distance) * speed
        else:
            self.velocity_x = -speed
            self.velocity_y = 0
        
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.animation_frame = 0
        
    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.rect.x = self.x
        self.rect.y = self.y
        self.animation_frame += 1
    
    def draw(self, surface):
        # Draw a dark energy ball with pulsing effect
        pulse = abs(math.sin(self.animation_frame * 0.2)) * 3
        radius = self.size // 2 + int(pulse)
        center_x = int(self.x + self.size // 2)
        center_y = int(self.y + self.size // 2)
        
        # Outer glow (dark purple/red)
        pygame.draw.circle(surface, (80, 20, 60), (center_x, center_y), radius + 2)
        # Middle layer (red)
        pygame.draw.circle(surface, (180, 40, 40), (center_x, center_y), radius)
        # Inner core (bright red/orange)
        pygame.draw.circle(surface, (255, 100, 80), (center_x, center_y), max(2, radius - 3))
        # Center bright spot
        pygame.draw.circle(surface, (255, 200, 150), (center_x, center_y), max(1, radius - 5))
    
    def collides_with(self, player):
        player_rect = pygame.Rect(player.x + 10, player.y + 10, player.size - 20, player.size - 20)
        projectile_rect = pygame.Rect(self.x, self.y, self.size, self.size)
        return player_rect.colliderect(projectile_rect)
    
    def is_off_screen(self):
        return (self.x < -self.size or self.x > SCREEN_WIDTH + self.size or 
                self.y < -self.size or self.y > SCREEN_HEIGHT + self.size)

class Coin:
    def __init__(self, level_config):
        self.x = SCREEN_WIDTH + 50
        self.y = random.randint(100, SCREEN_HEIGHT - 100)
        self.size = game_settings['coin_size']
        self.speed = level_config['coin_speed']
        self.rect = pygame.Rect(self.x, self.y, self.size, self.size)
        self.rotation = 0
        self.rotation_speed = 3
        self.float_offset = random.random() * 10
        self.float_amplitude = 15
        self.float_frequency = 0.08
        self.original_y = self.y
        
    def update(self, frame_count):
        self.x -= self.speed
        # Floating motion - slower sine wave
        self.y = self.original_y + self.float_amplitude * math.sin(
            (frame_count + self.float_offset) * self.float_frequency
        )
        # Rotation animation
        self.rotation = (self.rotation + self.rotation_speed) % 360
        self.rect.x = self.x
        self.rect.y = self.y
    
    def draw(self, surface):
        # Create coin surface
        coin_surface = pygame.Surface((self.size, self.size), pygame.SRCALPHA)
        
        # Calculate 3D rotation effect (oval width based on rotation)
        rotation_factor = abs(math.cos(math.radians(self.rotation)))
        oval_width = int(self.size * rotation_factor)
        
        if oval_width > 2:  # Only draw if visible
            # Outer gold ring
            pygame.draw.ellipse(coin_surface, (255, 215, 0), 
                              (self.size//2 - oval_width//2, 2, oval_width, self.size - 4))
            # Inner darker gold
            if oval_width > 6:
                pygame.draw.ellipse(coin_surface, (218, 165, 32), 
                                  (self.size//2 - oval_width//2 + 3, 5, oval_width - 6, self.size - 10))
            # Highlight
            if oval_width > 10:
                pygame.draw.ellipse(coin_surface, (255, 255, 200), 
                                  (self.size//2 - oval_width//2 + 4, 6, oval_width//2, self.size//4))
        
        surface.blit(coin_surface, (self.x, self.y))
    
    def collides_with(self, player):
        player_rect = pygame.Rect(player.x + 10, player.y + 10, player.size - 20, player.size - 20)
        coin_rect = pygame.Rect(self.x + 5, self.y + 5, self.size - 10, self.size - 10)
        return player_rect.colliderect(coin_rect)
    
    def is_off_screen(self):
        return self.x + self.size < 0

class Game:
    def __init__(self):
        self.player = Player()
        self.walls = []
        self.enemies = []
        self.coins = []
        self.projectiles = []
        self.score = 0
        self.coins_collected = 0
        self.high_score = load_high_score()
        self.current_level = 0
        self.level_config = levels[self.current_level]
        self.game_state = 'menu'  # menu, playing, game_over
        self.last_wall_spawn = 0
        self.last_enemy_spawn = 0
        self.last_coin_spawn = 0
        self.frame_count = 0
        self.clock = pygame.time.Clock()
        
    def start_game(self):
        self.player.reset()
        self.walls = []
        self.enemies = []
        self.coins = []
        self.projectiles = []
        self.score = 0
        self.coins_collected = 0
        self.current_level = 0
        self.level_config = levels[self.current_level]
        self.game_state = 'playing'
        self.last_wall_spawn = pygame.time.get_ticks()
        self.last_enemy_spawn = pygame.time.get_ticks()
        self.last_coin_spawn = pygame.time.get_ticks()
        self.frame_count = 0
        try:
            mixer.music.play(-1)
        except:
            pass
    
    def check_level_up(self):
        if self.current_level < len(levels) - 1:
            next_level = levels[self.current_level + 1]
            if self.score >= next_level['required_score']:
                self.current_level += 1
                self.level_config = levels[self.current_level]
    
    def spawn_wall(self):
        gap_height = self.level_config['wall_gap']
        min_gap_y = 100
        max_gap_y = SCREEN_HEIGHT - gap_height - 100
        gap_y = random.randint(min_gap_y, max_gap_y)
        wall = Wall(SCREEN_WIDTH, gap_y, gap_height, self.level_config['wall_speed'])
        self.walls.append(wall)
    
    def spawn_enemy(self):
        enemy = Enemy(self.level_config)
        self.enemies.append(enemy)
    
    def spawn_coin(self):
        coin = Coin(self.level_config)
        self.coins.append(coin)
    
    def update(self):
        if self.game_state != 'playing':
            return
        
        self.frame_count += 1
        current_time = pygame.time.get_ticks()
        
        # Spawn walls
        if current_time - self.last_wall_spawn > self.level_config['wall_spawn_interval']:
            self.spawn_wall()
            self.last_wall_spawn = current_time
        
        # Spawn enemies
        if current_time - self.last_enemy_spawn > self.level_config['enemy_spawn_interval']:
            self.spawn_enemy()
            self.last_enemy_spawn = current_time
        
        # Spawn coins
        if current_time - self.last_coin_spawn > self.level_config['coin_spawn_interval']:
            self.spawn_coin()
            self.last_coin_spawn = current_time
        
        # Update player
        self.player.update()
        
        # Update walls
        for wall in self.walls[:]:
            wall.update()
            
            # Check if player passed the wall
            if not wall.passed and wall.x + wall.width < self.player.x:
                wall.passed = True
                self.score += game_settings['score_per_wall']
                self.check_level_up()
            
            # Check collision
            if wall.collides_with(self.player):
                self.game_over()
            
            # Remove off-screen walls
            if wall.is_off_screen():
                self.walls.remove(wall)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.frame_count)
            
            # Check if enemy should shoot
            if enemy.can_shoot(current_time, self.player):
                projectile = enemy.shoot(self.player)
                self.projectiles.append(projectile)
                if enemy_sound:
                    enemy_sound.play()
            
            # Check collision
            if enemy.collides_with(self.player):
                if enemy_sound:
                    enemy_sound.play()
                self.enemies.remove(enemy)
                self.score += game_settings['score_per_enemy']
                self.check_level_up()
            
            # Remove off-screen enemies
            if enemy.is_off_screen():
                self.enemies.remove(enemy)
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update()
            
            # Check collision with player
            if projectile.collides_with(self.player):
                self.game_over()
            
            # Remove off-screen projectiles
            if projectile.is_off_screen():
                self.projectiles.remove(projectile)
        
        # Update coins
        for coin in self.coins[:]:
            coin.update(self.frame_count)
            
            # Check collision
            if coin.collides_with(self.player):
                if flap_sound:  # Use flap sound for coin collection
                    flap_sound.play()
                self.coins.remove(coin)
                self.coins_collected += 1
                self.score += game_settings['score_per_coin']
                self.check_level_up()
            
            # Remove off-screen coins
            if coin.is_off_screen():
                self.coins.remove(coin)
    
    def game_over(self):
        self.game_state = 'game_over'
        if self.score > self.high_score:
            self.high_score = self.score
            save_high_score(self.high_score)
        try:
            mixer.music.stop()
        except:
            pass
        if gameover_sound:
            gameover_sound.play()
    
    def draw(self):
        # Draw blurred background
        screen.blit(background, (0, 0))
        screen.blit(blurred_bg, (0, 0))
        
        if self.game_state == 'menu':
            self.draw_menu()
        elif self.game_state == 'playing':
            self.draw_game()
        elif self.game_state == 'game_over':
            self.draw_game()
            self.draw_game_over()
        
        pygame.display.flip()
    
    def draw_menu(self):
        # Title
        title = font_large.render('FLAPPY BIRD', True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
        title_shadow = font_large.render('FLAPPY BIRD', True, BLACK)
        screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))
        screen.blit(title, title_rect)
        
        subtitle = font_small.render('City Edition', True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(SCREEN_WIDTH // 2, 210))
        screen.blit(subtitle, subtitle_rect)
        
        # High Score
        high_score_text = font_medium.render(f'High Score: {self.high_score}', True, WHITE)
        high_score_rect = high_score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
        screen.blit(high_score_text, high_score_rect)
        
        # Start button
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 380, 200, 60)
        pygame.draw.rect(screen, (100, 200, 100), button_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_rect, 3, border_radius=10)
        
        start_text = font_medium.render('START', True, WHITE)
        start_rect = start_text.get_rect(center=button_rect.center)
        screen.blit(start_text, start_rect)
        
        # Instructions
        inst1 = font_small.render('Press SPACE or LEFT CLICK to flap', True, WHITE)
        inst2 = font_small.render('Dodge projectiles! Catch enemies and collect coins!', True, WHITE)
        screen.blit(inst1, inst1.get_rect(center=(SCREEN_WIDTH // 2, 480)))
        screen.blit(inst2, inst2.get_rect(center=(SCREEN_WIDTH // 2, 520)))
        
        return button_rect
    
    def draw_game(self):
        # Draw walls
        for wall in self.walls:
            wall.draw(screen)
        
        # Draw coins
        for coin in self.coins:
            coin.draw(screen)
        
        # Draw projectiles
        for projectile in self.projectiles:
            projectile.draw(screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # Draw player
        self.player.draw(screen)
        
        # Draw HUD
        score_text = font_medium.render(f'Score: {self.score}', True, WHITE)
        screen.blit(score_text, (10, 10))
        
        level_text = font_small.render(f'Level: {self.level_config["name"]}', True, WHITE)
        screen.blit(level_text, (10, 60))
        
        # Coin counter with icon
        coin_text = font_small.render(f'Coins: {self.coins_collected}', True, (255, 215, 0))
        screen.blit(coin_text, (10, 100))
        
        high_score_text = font_small.render(f'High: {self.high_score}', True, WHITE)
        high_score_rect = high_score_text.get_rect(topright=(SCREEN_WIDTH - 10, 10))
        screen.blit(high_score_text, high_score_rect)
    
    def draw_game_over(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(150)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_text = font_large.render('GAME OVER', True, (255, 100, 100))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = font_medium.render(f'Final Score: {self.score}', True, WHITE)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 280))
        screen.blit(score_text, score_rect)
        
        # High score
        if self.score == self.high_score and self.score > 0:
            new_high = font_small.render('NEW HIGH SCORE!', True, (255, 215, 0))
            new_high_rect = new_high.get_rect(center=(SCREEN_WIDTH // 2, 330))
            screen.blit(new_high, new_high_rect)
        else:
            high_text = font_small.render(f'High Score: {self.high_score}', True, WHITE)
            high_rect = high_text.get_rect(center=(SCREEN_WIDTH // 2, 330))
            screen.blit(high_text, high_rect)
        
        # Restart button
        button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 60)
        pygame.draw.rect(screen, (100, 200, 100), button_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, button_rect, 3, border_radius=10)
        
        restart_text = font_medium.render('RESTART', True, WHITE)
        restart_rect = restart_text.get_rect(center=button_rect.center)
        screen.blit(restart_text, restart_rect)
        
        # Menu button
        menu_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 480, 200, 60)
        pygame.draw.rect(screen, (200, 100, 100), menu_button_rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, menu_button_rect, 3, border_radius=10)
        
        menu_text = font_medium.render('MENU', True, WHITE)
        menu_rect = menu_text.get_rect(center=menu_button_rect.center)
        screen.blit(menu_text, menu_rect)
        
        return button_rect, menu_button_rect
    
    def handle_click(self, pos):
        if self.game_state == 'menu':
            button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 380, 200, 60)
            if button_rect.collidepoint(pos):
                self.start_game()
        elif self.game_state == 'playing':
            self.player.flap()
        elif self.game_state == 'game_over':
            restart_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 400, 200, 60)
            menu_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, 480, 200, 60)
            if restart_rect.collidepoint(pos):
                self.start_game()
            elif menu_rect.collidepoint(pos):
                self.game_state = 'menu'
    
    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_click(event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_state == 'playing':
                            self.player.flap()
                        elif self.game_state == 'menu':
                            self.start_game()
            
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = Game()
    game.run()

