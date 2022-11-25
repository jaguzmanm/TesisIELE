import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed, max_y, target_x, target_y):
        super().__init__()
        self.image = pygame.image.load("graphics/bullet.png").convert_alpha()
        self.rect = self.image.get_rect(center = pos)
 
        self.x = pos[0]
        self.y = pos[1]

        angle = math.atan2(target_y-self.y, target_x-self.x)

        self.dx = math.cos(angle)*speed
        self.dy = math.sin(angle)*speed

        self.speed = speed
        self.max_y = max_y

    def destroy(self):
        if self.rect.y <= -50 or self.rect.y >= self.max_y + 50:
            self.kill()

    def update(self):
        self.x += self.dx
        self.y += self.dy
        self.rect.x = int(self.x)
        self.rect.y = int(self.y)
        self.destroy()
