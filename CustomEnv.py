import gym
from gym.spaces import Discrete, Box
from PIL import Image

from skimage import transform, img_as_ubyte

import pygame
import numpy as np
import gym


from game import Game

screen_width = 448
screen_height = 586

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
        self.kills = 0
        self.init_render()
        self.game = Game(screen_width, screen_height)

        ## ACTIONS:
        #  - 0: STAY
        #  - 1: LEFT
        #  - 2: RIGHT
        #  - 3: SHOOT
        #  - 4: LEFT + SHOOT
        #  - 5: RIGHT + SHOOT
        self.action_space = Discrete(3)

        self.observation_space = Box(low=0, high=255, shape=(150, 150, 1), dtype=np.uint8)


    def init_render(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        

    def reset(self):
        self.duration = 0
        self.kills = 0
        self.init_render()
        self.game = Game(screen_width, screen_height)
        return self.get_obs()

    def step(self, action):
        #Execute step in game
        self.game.step(action, self.duration)
        self.screen.fill("black")
        self.game.run(self.screen)
        self.duration += 1


        self.clock.tick(300000)
        pygame.display.flip()

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
            if self.game.lives <= 0:
                reward = -1000
            else:
                reward = 1000
            # reward = self.game.score + self.game.lives*500

        #Observation
        observation = self.get_obs()

        return observation, reward, done, {}
    
    def get_obs(self):
        rgb = pygame.surfarray.array3d(self.screen)
        img_rgb = Image.fromarray(rgb)
        img_gray = img_rgb.convert('L')
        img_gray_array = np.array(img_gray)
        img_gray_resize = img_as_ubyte(transform.resize(img_gray_array, (150, 150)))
        # img_gray.save("testgrey2.png")
        final_obs = img_gray_resize.reshape(img_gray_resize.shape + (1,))
        return final_obs

    def render(self):
        pass