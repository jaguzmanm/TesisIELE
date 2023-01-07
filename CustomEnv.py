import gym
from gym.spaces import Discrete, Box
from PIL import Image

from skimage import transform, img_as_ubyte

import pygame
import numpy as np
import gym

from game.game import Game

def get_action():
    keys = pygame.key.get_pressed()
    left = 0
    right = 0
    shoot = 0
    if keys[pygame.K_a]:
        left = 1
    elif keys[pygame.K_d]:
        right = 1

    if keys[pygame.K_SPACE]:
        shoot = 1
    return np.array([left, right, shoot])



class CustomEnv(gym.Env):
    def __init__(self,env_config={}):
        self.duration = 0
        self.final_state = -1
        self.screen_width = env_config[0]
        self.screen_height = env_config[1]
        self.lvl = env_config[2]
        self.init_render()
        self.game = Game(self.screen_width, self.screen_height, self.lvl)

        ## ACTIONS:
        #  - 0: STAY
        #  - 1: LEFT
        #  - 2: RIGHT
        #  - 3: SHOOT
        #  - 4: LEFT + SHOOT
        #  - 5: RIGHT + SHOOT
        self.action_space = Discrete(3)

        self.observation_space = Box(low=0, high=255, shape=(120, 120, 1), dtype=np.uint8)


    def init_render(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.clock = pygame.time.Clock()
        

    def reset(self):
        self.duration = 0
        self.final_state = -1
        self.init_render()
        self.game = Game(self.screen_width, self.screen_height, self.lvl)
        return self.get_obs()

    def step(self, action):
        #Execute step in game
        self.game.step(action, self.duration)
        self.screen.fill("black")
        self.game.run(self.screen)
        self.duration += 1


        self.clock.tick(30)
        pygame.display.flip()

        if self.duration >= 1050:
            done = True
        else:
            done = self.game.finished
        change = self.game.change

        ### Calculate reward
        if not done:
            reward = 0
            if change[0] == 1:
                #Extra reward for killing an enemy
                reward = change[1]
                # reward = 5
                # self.kills += 1
            elif change[0] == 2:
                #Extra reward for hitting a boss
                reward = change[1]
                # reward = 1
            if change[0] == 3:
                #Penalty for losing a live
                reward = -1000
        else:
            #Se acabaron las vidas
            if self.game.lives <= 0:
                reward = -1000
                self.final_state = 1
            #Se exedió el limite de tiempo
            elif self.duration >= 1050:
                reward = -500
                self.final_state = 2
            #Completó el nivel satisfactoriamente
            else:
                reward = 2000 - self.duration
                self.final_state = 3
            # reward = self.game.score + self.game.lives*500

        #Observation
        observation = self.get_obs()

        return observation, reward, done, {}
    
    def get_obs(self):
        rgb = pygame.surfarray.array3d(self.screen)
        img_rgb = Image.fromarray(rgb)
        img_gray = img_rgb.convert('L')
        img_gray_array = np.array(img_gray)
        img_gray_resize = img_as_ubyte(transform.resize(img_gray_array, (120, 120)))
        # img_gray.save("testgrey2.png")
        final_obs = img_gray_resize.reshape(img_gray_resize.shape + (1,))
        return final_obs

    def render(self):
        pass