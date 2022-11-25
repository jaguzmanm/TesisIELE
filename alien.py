from turtle import speed
import pygame

class Alien(pygame.sprite.Sprite):
    def __init__(self, color, x, y, speed_x, speed_y):
        super().__init__()
        
        self.support = 69
        self.speed_support = -5

        path = "graphics/" + color + ".png"
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))
        self.speed_x = speed_x
        self.speed_y = speed_y

        self.direction_time = pygame.time.get_ticks()
        self.direction_cooldown = 350
 
        if color == "red": self.value = 80
        else: self.value = 50

    def change_direction(self):
        if self.support <= 0 or self.support >= 69:
            self.speed_x *= -1
            self.speed_y *= -1
            self.speed_support *= -1

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.support += self.speed_support
        self.change_direction()


class Boss(pygame.sprite.Sprite):
    def __init__(self, lives, x, y, speed_x, speed_y, support = 69):
        super().__init__()

        self.support = support
        self.speed_support = -5

        path = "graphics/boss" + str(lives) + ".png"
        self.image = pygame.image.load(path).convert_alpha()
        self.rect = self.image.get_rect(topleft = (x, y))
        self.lives = lives
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y

        if lives == 1: self.value = 400
        else: self.value = 0

    def change_direction(self):
        if self.support <= 0 or self.support >= 69:
            self.speed_x *= -1
            self.speed_y *= -1
            self.speed_support *= -1

    def attack(self):
        self.speed_x = 3
        self.speed_y = 3
    
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        self.support += self.speed_support
        self.change_direction()