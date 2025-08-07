import pygame
import sys
import random

# --- Game Settings ---
WIDTH, HEIGHT = 640, 480
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (50, 50, 220)

PLAYER_COLOR = BLUE
ENEMY_COLOR = RED

BAR_WIDTH = 200
BAR_HEIGHT = 20

# --- Fighter Class ---
class Fighter:
    def __init__(self, name, x, y, color):
        self.name = name
        self.max_health = 30
        self.health = 30
        self.attack = 8
        self.defense = 3
        self.x = x
        self.y = y
        self.color = color
        self.width = 60
        self.height = 100
        self.is_attacking = False
        self.attack_anim_frame = 0

    def draw(self, screen):
        # Draw fighter
        rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, rect)
        # Draw health bar
        health_ratio = self.health / self.max_health
        bar_x = self.x
        bar_y = self.y - 30
        pygame.draw.rect(screen, BLACK, (bar_x, bar_y, BAR_WIDTH, BAR_HEIGHT))
        pygame.draw.rect(screen, GREEN, (bar_x, bar_y, int(BAR_WIDTH * health_ratio), BAR_HEIGHT))
        # Draw name
        font = pygame.font.SysFont(None, 28)
        name_surf = font.render(self.name, True, BLACK)
        screen.blit(name_surf, (self.x, self.y - 55))

    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0

    def deal_damage(self, other):
        base_damage = self.attack - other.defense
        if base_damage < 1:
            base_damage = 1
        damage = base_damage + random.randint(-2, 2)
        if damage < 1:
            damage = 1
        other.take_damage(damage)
        return damage

    def is_alive(self):
        return self.health > 0

    def animate_attack(self):
        self.is_attacking = True
        self.attack_anim_frame = 0

    def update_attack_anim(self):
        if self.is_attacking:
            self.attack_anim_frame += 1
            if self.attack_anim_frame > 10:
                self.is_attacking = False
                self.attack_anim_frame = 0

# --- Game Functions ---
def draw_text(screen, text, x, y, size=36, color=BLACK):
    font = pygame.font.SysFont(None, size)
    surf = font.render(text, True, color)
    rect = surf.get_rect(center=(x, y))
    screen.blit(surf, rect)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("2D Fighting Game")
    clock = pygame.time.Clock()

    # Create fighters
    player = Fighter("Player", 100, HEIGHT//2, PLAYER_COLOR)
    enemy = Fighter("Enemy", WIDTH-160, HEIGHT//2, ENEMY_COLOR)

    turn = 'player'  # 'player' or 'enemy'
    game_over = False
    result = ''
    action_cooldown = 0
    attack_damage = 0
    show_damage = False
    damage_timer = 0

    while True:
        screen.fill(WHITE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if not game_over:
            # Draw fighters
            player.draw(screen)
            enemy.draw(screen)

            # Player turn
            if turn == 'player' and not player.is_attacking and not show_damage:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_a]:
                    player.animate_attack()
                    attack_damage = player.deal_damage(enemy)
                    show_damage = True
                    damage_timer = pygame.time.get_ticks()
                    turn = 'enemy'
            # Player attack animation
            if player.is_attacking:
                player.x += 8 if player.attack_anim_frame < 5 else -8
                player.update_attack_anim()
            # Enemy turn
            if turn == 'enemy' and not enemy.is_attacking and not show_damage:
                pygame.time.delay(500)
                enemy.animate_attack()
                attack_damage = enemy.deal_damage(player)
                show_damage = True
                damage_timer = pygame.time.get_ticks()
                turn = 'player'
            # Enemy attack animation
            if enemy.is_attacking:
                enemy.x -= 8 if enemy.attack_anim_frame < 5 else -8
                enemy.update_attack_anim()
            # Show damage text
            if show_damage:
                if turn == 'enemy':
                    draw_text(screen, f"-{attack_damage}", enemy.x + 30, enemy.y - 40, 32, RED)
                else:
                    draw_text(screen, f"-{attack_damage}", player.x + 30, player.y - 40, 32, RED)
                if pygame.time.get_ticks() - damage_timer > 600:
                    show_damage = False
            # Check win/lose
            if not player.is_alive():
                game_over = True
                result = 'You Lose!'
            elif not enemy.is_alive():
                game_over = True
                result = 'You Win!'
        else:
            draw_text(screen, result, WIDTH//2, HEIGHT//2, 64, RED)
            draw_text(screen, 'Press R to Restart or Q to Quit', WIDTH//2, HEIGHT//2+60, 32, BLACK)
            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                main()
            if keys[pygame.K_q]:
                pygame.quit()
                sys.exit()

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == '__main__':
    main()