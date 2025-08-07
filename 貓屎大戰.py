import pygame
import sys
import os
from utils import load_sprite_sheet, load_sound

WIDTH, HEIGHT = 800, 480
FPS = 60

# Controls
P1_KEYS = {'left': pygame.K_a, 'right': pygame.K_d, 'up': pygame.K_w, 'down': pygame.K_s, 'attack': pygame.K_j, 'special': pygame.K_k}
P2_KEYS = {'left': pygame.K_LEFT, 'right': pygame.K_RIGHT, 'up': pygame.K_UP, 'down': pygame.K_DOWN, 'attack': pygame.K_KP1, 'special': pygame.K_KP2}

# Character States
IDLE, WALK, ATTACK, HIT, JUMP, SPECIAL = 'idle', 'walk', 'attack', 'hit', 'jump', 'special'

class Character:
    def __init__(self, name, sprite_folder, x, y, controls=None, ai=False, fallback_color=(128,128,128)):
        self.name = name
        self.x = x
        self.y = y
        self.controls = controls
        self.ai = ai
        self.state = IDLE
        self.facing = 1  # 1: right, -1: left
        self.frame = 0
        self.anim_timer = 0
        self.health = 100
        self.energy = 0
        self.max_health = 100
        self.max_energy = 100
        self.sprites = {
            IDLE: load_sprite_sheet(os.path.join(sprite_folder, 'idle'), 80, 120, fallback_color),
            WALK: load_sprite_sheet(os.path.join(sprite_folder, 'walk'), 80, 120, fallback_color),
            ATTACK: load_sprite_sheet(os.path.join(sprite_folder, 'attack'), 80, 120, fallback_color),
            HIT: load_sprite_sheet(os.path.join(sprite_folder, 'hit'), 80, 120, fallback_color),
            JUMP: load_sprite_sheet(os.path.join(sprite_folder, 'jump'), 80, 120, fallback_color),
            SPECIAL: load_sprite_sheet(os.path.join(sprite_folder, 'special'), 100, 140, fallback_color),
        }
        self.current_sprites = self.sprites[IDLE]
        self.rect = pygame.Rect(self.x, self.y, 80, 120)

    def update(self, keys, opponent):
        # Placeholder: simple state machine
        if self.ai:
            self.ai_update(opponent)
        else:
            self.player_update(keys)
        self.anim_timer += 1
        if self.anim_timer > 6:
            self.frame = (self.frame + 1) % len(self.current_sprites)
            self.anim_timer = 0

    def player_update(self, keys):
        # Movement
        if keys[self.controls['left']]:
            self.x -= 4
            self.state = WALK
            self.facing = -1
        elif keys[self.controls['right']]:
            self.x += 4
            self.state = WALK
            self.facing = 1
        else:
            self.state = IDLE
        # Attack
        if keys[self.controls['attack']]:
            self.state = ATTACK
        # Special
        if keys[self.controls['special']] and self.energy >= 50:
            self.state = SPECIAL
            self.energy -= 50
        self.current_sprites = self.sprites[self.state] if self.sprites[self.state] else self.sprites[IDLE]

    def ai_update(self, opponent):
        # Simple AI: move toward player, attack if close
        if abs(self.x - opponent.x) > 100:
            self.x += 2 if self.x < opponent.x else -2
            self.state = WALK
            self.facing = 1 if self.x < opponent.x else -1
        else:
            self.state = ATTACK
        self.current_sprites = self.sprites[self.state] if self.sprites[self.state] else self.sprites[IDLE]

    def draw(self, screen):
        img = self.current_sprites[self.frame % len(self.current_sprites)] if self.current_sprites else None
        if img:
            if self.facing == -1:
                img = pygame.transform.flip(img, True, False)
            screen.blit(img, (self.x, self.y))
        # Draw health/energy bars
        pygame.draw.rect(screen, (255,0,0), (self.x, self.y-20, 80, 10))
        pygame.draw.rect(screen, (0,255,0), (self.x, self.y-20, 80 * (self.health/self.max_health), 10))
        pygame.draw.rect(screen, (0,0,255), (self.x, self.y-10, 80 * (self.energy/self.max_energy), 5))

    def hit(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0
        self.state = HIT

    def gain_energy(self, amount):
        self.energy += amount
        if self.energy > self.max_energy:
            self.energy = self.max_energy

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('貓屎大戰')
    clock = pygame.time.Clock()

    # Load background
    bg = pygame.Surface((WIDTH, HEIGHT))
    bg.fill((200, 200, 255))
    # TODO: load actual background image

    # Load characters with different fallback colors
    p1 = Character('Player1', 'assets/sprites/player1', 100, 300, controls=P1_KEYS, fallback_color=(50, 100, 220))
    p2 = Character('Player2', 'assets/sprites/player2', 600, 300, controls=P2_KEYS, ai=True, fallback_color=(220, 80, 80))

    running = True
    while running:
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update
        p1.update(keys, p2)
        p2.update(keys, p1)

        # Simple collision/attack logic
        if p1.state == ATTACK and abs(p1.x - p2.x) < 90:
            p2.hit(5)
            p1.gain_energy(10)
        if p2.state == ATTACK and abs(p2.x - p1.x) < 90:
            p1.hit(5)
            p2.gain_energy(10)
        if p1.state == SPECIAL and abs(p1.x - p2.x) < 120:
            p2.hit(20)
        if p2.state == SPECIAL and abs(p2.x - p1.x) < 120:
            p1.hit(20)

        # Draw
        screen.blit(bg, (0,0))
        p1.draw(screen)
        p2.draw(screen)

        # Win/lose
        if p1.health <= 0 or p2.health <= 0:
            font = pygame.font.SysFont(None, 64)
            if p1.health > 0:
                msg = 'Player 1 Wins!'
            elif p2.health > 0:
                msg = 'Player 2 Wins!'
            else:
                msg = 'Draw!'
            text = font.render(msg, True, (255,0,0))
            screen.blit(text, (WIDTH//2-200, HEIGHT//2-50))
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == '__main__':
    main()