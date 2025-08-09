# mini_fighter_gameover.py
import pygame
import sys
from pygame.locals import *
pygame.init()

W, H = 800, 400
screen = pygame.display.set_mode((W, H))
clock = pygame.time.Clock()
FONT = pygame.font.SysFont(None, 24)

class Fighter:
    def __init__(self, x, y, color):
        self.init_x = x
        self.ground_y = y
        self.color = color
        self.w, self.h = 60, 80
        self.speed = 20  # 設定移動速度
        self.reset()

    def reset(self):
        self.x = self.init_x
        self.y = self.ground_y
        self.vx = 0
        self.hp = 100
        self.state = "idle"
        self.attack_cooldown = 0
        # 跳躍相關參數
        self.on_ground = True
        self.velocity_y = 0
        self.gravity = 0.5
        self.jump_power = 10

    def rect(self):
        return pygame.Rect(self.x, self.y - self.h, self.w, self.h)

    def update(self):
        self.x += self.vx
        self.x = max(0, min(W - self.w, self.x))
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        if self.attack_cooldown == 0 and self.state == "attack":
            self.state = "idle"
        # 跳躍與重力更新
        if not self.on_ground:
            self.velocity_y -= self.gravity
            self.y -= self.velocity_y
            if self.y >= self.ground_y:
                self.y = self.ground_y
                self.on_ground = True
                self.velocity_y = 0

    def draw(self, surf):
        pygame.draw.rect(surf, self.color, self.rect())
        # HP bar
        hp_w = int(self.w * (self.hp / 100))
        pygame.draw.rect(surf, (255,0,0), (self.x, self.y - self.h - 10, self.w, 6))
        pygame.draw.rect(surf, (0,255,0), (self.x, self.y - self.h - 10, hp_w, 6))

    def attack(self, other):
        if self.attack_cooldown == 0:
            self.state = "attack"
            self.attack_cooldown = 30
            attack_box = self.rect().copy()
            if self.x < other.x:
                attack_box.right = self.rect().right + 30
            else:
                attack_box.left = self.rect().left - 30
            if attack_box.colliderect(other.rect()):
                other.hp -= 10
                other.state = "hit"

    def jump(self):
        if self.on_ground:
            self.velocity_y = self.jump_power
            self.on_ground = False

player = Fighter(100, 350, (0,120,255))
enemy  = Fighter(600, 350, (255,80,80))

while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit(); sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE:
                player.attack(enemy)
            if event.key == K_w:
                player.jump()

    # 控制移動
    keys = pygame.key.get_pressed()
    player.vx = 0
    if keys[K_a]:
        player.vx = -player.speed
    if keys[K_d]:
        player.vx = player.speed

    # 敵人簡單 AI
    if enemy.x > player.x + 50:
        enemy.vx = -2
    elif enemy.x < player.x - 50:
        enemy.vx = 2
    else:
        enemy.vx = 0
        if enemy.attack_cooldown == 0:
            enemy.attack(player)

    player.update()
    enemy.update()
    screen.fill((30,30,30))
    player.draw(screen)
    enemy.draw(screen)
    txt = FONT.render("A/D: move  SPACE: attack  W: jump", True, (200,200,200))
    screen.blit(txt, (10,10))
    pygame.display.flip()
    clock.tick(60)
