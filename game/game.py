from random import choice, random
import pygame

from game.bullet import Bullet
from game.ship import Ship
from game.alien import Alien, Boss

class Game:
    def __init__(self, screen_width, screen_height, lvl):

        self.lvl = lvl

        #Ship setup
        ship_sprite = Ship((screen_width//2, screen_height - 40), screen_width, screen_height, 6)
        self.ship = pygame.sprite.GroupSingle(ship_sprite)

        #Lives and Score setup
        self.lives = 3
        self.live_surface = pygame.image.load("graphics/ship.png").convert_alpha()
        self.live_x_start_pos = screen_width - (self.live_surface.get_size()[0] * 2 + 20)

        self.score = 0
        self.font = pygame.font.Font("font/Pixeled.ttf", 20)

        #Aliens setup
        self.aliens = pygame.sprite.Group()
        self.alien_setup(4, 10)

        self.alien_bullets = pygame.sprite.Group()

        #Boss setup
        self.bosses = pygame.sprite.Group()
        self.boss_setup()

        self.screen_height = screen_height
        self.finished = False
        self.max_score = 3880
        self.change = (0, 0)

    def alien_setup(self, rows, cols, x_distance = 32, y_distance = 26):
        for row_index in range(rows):
            for col_index in range(cols):
                x = col_index * x_distance + 69
                y = row_index * y_distance + 109

                speed_x = col_index - (cols//2)
                if col_index >= 5:
                    speed_x += 1
                
                speed_y = row_index

                if self.lvl == 4:
                    speed_x *= 2

                if 0 <= row_index <= 1:
                    if col_index != 0 and col_index != 9:
                        alien_sprite = Alien("red" , x, y, speed_x ,speed_y, self.lvl)
                        self.aliens.add(alien_sprite)
                else:
                    alien_sprite = Alien("blue", x, y,speed_x,speed_y, self.lvl)
                    self.aliens.add(alien_sprite)
    
    def boss_setup(self, x_distance = 32):
        for i in range(4):
            x = i*x_distance + 160
            y = 71

            speed_x = i - (4//2)
            if i >= 2:
                speed_x += 1

            if self.lvl == 4:
                speed_x *= 2

            boss_sprite = Boss(2,x,y,speed_x, 0, lvl= self.lvl)
            self.bosses.add(boss_sprite)

    def alien_shoot(self):
        if self.aliens.sprites():
            random_alien = choice(self.aliens.sprites())
            bullet_sprite = Bullet(random_alien.rect.center, 8, self.screen_height, self.ship.sprite.rect.centerx, self.ship.sprite.rect.centery, "alien")
            self.alien_bullets.add(bullet_sprite)
        if self.bosses.sprites():
            random_boss = choice(self.bosses.sprites())
            bullet_sprite = Bullet(random_boss.rect.center, 8, self.screen_height, self.ship.sprite.rect.centerx, self.ship.sprite.rect.centery, "alien")
            self.alien_bullets.add(bullet_sprite)

    def collisions(self):
        if self.ship.sprite.bullets:
            for bullet in self.ship.sprite.bullets:
                alien_score = 0
                #Bullet-Alien
                aliens_hit = pygame.sprite.spritecollide(bullet, self.aliens, True)
                if aliens_hit:
                    bullet.kill()
                    for alien in aliens_hit:
                        self.score += alien.value
                        alien_score += alien.value
                if alien_score > 0: 
                    self.change = (1, alien_score)
                    if self.score >= self.max_score:
                            self.finished = True

                #Bullet-Boss
                boss_score = 0
                boss_hit = pygame.sprite.spritecollide(bullet, self.bosses, True)
                if boss_hit:
                    bullet.kill()
                    for boss in boss_hit:
                        if boss.lives == 1:
                            self.score += boss.value
                            boss_score += boss.value
                        else:
                            self.bosses.add(Boss(1,boss.x, boss.y, boss.speed_x, boss.speed_y, boss.support))
                    if boss_score > 0:
                        self.change = (1, boss_score + alien_score)
                        if self.score >= self.max_score:
                            self.finished = True
                    else:
                        self.change = (2, 25)
        
        if self.alien_bullets:
            for bullet in self.alien_bullets:
                #Bullet-Ship
                if pygame.sprite.spritecollide(bullet, self.ship, False):
                    for bullet_2 in self.alien_bullets:
                        bullet_2.kill()
                    self.lives -= 1
                    self.change = (3, -1) 
                    if self.lives <= 0:
                        self.finished = True
                    else:
                        self.ship.sprite.rect.centerx = 224
                    break
                
        
        if self.aliens:
            for alien in self.aliens:
                #Alien-Ship
                if pygame.sprite.spritecollide(alien, self.ship, False):
                    alien.kill() 
                    print("F")

    def show_lives(self, screen):
        for live in range(self.lives - 1):
            x = (live*(self.live_surface.get_size()[0] + 5)) + 10
            screen.blit(self.live_surface, (x,self.screen_height-35))
    
    def show_score(self, screen):
        score_surf = self.font.render(f"score: {self.score}", False, "white")
        score_rect = score_surf.get_rect(topleft = (10, -10))
        screen.blit(score_surf, score_rect)

    def run(self, screen):

        self.ship.sprite.bullets.draw(screen)
        self.ship.draw(screen)

        self.aliens.draw(screen)
        self.bosses.draw(screen)
        if self.lvl == 3 or self.lvl == 4 or self.lvl == 2:
            self.alien_bullets.draw(screen)

        self.show_lives(screen)
        self.show_score(screen)


    def step(self, action, duration):
        self.change = (0, 0)
        self.ship.update(action, duration)
        self.aliens.update()
        self.bosses.update()

        if self.lvl == 3 or self.lvl == 4 or self.lvl == 2:
            self.alien_bullets.update()

        self.collisions()
        
        if self.lvl == 2:
            if random() <= 0.01:
                self.alien_shoot()

        elif self.lvl == 3:
            if random() <= 0.02:
                self.alien_shoot()

        elif self.lvl == 4:
            if random() <= 0.03:
                self.alien_shoot()