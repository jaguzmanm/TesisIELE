import pygame
from bullet import Bullet

class Ship(pygame.sprite.Sprite):
    def __init__(self, pos, limit_x, limit_y, speed):
        super().__init__()
        self.image = pygame.image.load("graphics/ship.png").convert_alpha()
        self.rect = self.image.get_rect(midbottom = pos)
        self.speed = speed
        self.max_x = limit_x
        self.max_y = limit_y

        self.ready = True
        self.bullet_time = 0
        self.cooldown = 15

        self.bullets = pygame.sprite.Group()

    def get_input(self, action):
        if action == 1:
            self.rect.x -= self.speed
        elif action == 2:
            self.rect.x += self.speed
        # elif action == 3 and self.ready:
        #     self.shoot()
        #     self.ready = False
        #     self.bullet_time = duration
        # elif action == 4 and self.ready:
        #     self.rect.x -= self.speed
        #     self.shoot()
        #     self.ready = False
        #     self.bullet_time = duration
        # elif action == 5 and self.ready:
        #     self.rect.x += self.speed
        #     self.shoot()
        #     self.ready = False
        #     self.bullet_time = duration
    
    def shoot(self, duration):
        if self.ready:
            self.bullets.add(Bullet(self.rect.center, 22, self.max_y, self.rect.centerx, 0, "ship"))
            self.ready = False
            self.bullet_time = duration

    def recharge(self, duration):
        if not self.ready:
            current_time = duration
            if current_time - self.bullet_time >= self.cooldown:
                self.ready = True

    def limit_move(self):
        if self.rect.right >= self.max_x:
            self.rect.right = self.max_x
        elif self.rect.left <= 0:
            self.rect.left = 0
    
    def update(self, action, duration):
        self.get_input(action)
        self.limit_move()
        self.shoot(duration)
        self.recharge(duration)
        self.bullets.update()

