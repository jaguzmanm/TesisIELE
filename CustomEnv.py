import gym
from gym.spaces import Discrete, Dict, Box, Tuple

import pygame
import numpy as np
import gym
import sys

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
        self.init_render()
        self.game = Game(screen_width, screen_height)

        ## ACTIONS:
        #  - 0: STAY
        #  - 1: LEFT
        #  - 2: RIGHT
        #  - 3: SHOOT
        #  - 4: LEFT + SHOOT
        #  - 5: RIGHT + SHOOT
        self.action_space = Discrete(6)
        self.observation_space = Box(low=0, high=255, shape=(screen_width, screen_height, 3), dtype=np.uint8)

        # low_aliens=np.array([[0, 0, 109], [0, 0, 109], [0, 0, 109], [0, 0, 109], [0, 0, 109], [0, 0, 109], 
        #                     [0, 0, 109], [0, 0, 109], [0, 0, 109],[0, 0, 109], [0, 0, 109],[0, 0, 109], 
        #                     [0, 0, 109], [0, 0, 109], [0, 0, 109],[0, 0, 109], [0, 0, 109],[0, 0, 109], 
        #                     [0, 0, 109], [0, 0, 109], [0, 0, 109],[0, 0, 109], [0, 0, 109],[0, 0, 109], 
        #                     [0, 0, 109], [0, 0, 109], [0, 0, 109],[0, 0, 109], [0, 0, 109],[0, 0, 109], 
        #                     [0, 0, 109], [0, 0, 109], [0, 0, 109],[0, 0, 109], [0, 0, 109],[0, 0, 109]])

        # high_aliens=np.array([[1, screen_width, 187], [1, screen_width, 187],[1, screen_width, 187], [1, screen_width, 187], [1, screen_width, 187],[1, screen_width, 187], 
        #                     [1, screen_width, 187], [1, screen_width, 187],[1, screen_width, 187], [1, screen_width, 187], [1, screen_width, 187],[1, screen_width, 187], 
        #                     [1, screen_width, 187], [1, screen_width, 187],[1, screen_width, 187], [1, screen_width, 187], [1, screen_width, 187],[1, screen_width, 187], 
        #                     [1, screen_width, 187], [1, screen_width, 187],[1, screen_width, 187], [1, screen_width, 187], [1, screen_width, 187],[1, screen_width, 187], 
        #                     [1, screen_width, 187], [1, screen_width, 187],[1, screen_width, 187], [1, screen_width, 187], [1, screen_width, 187],[1, screen_width, 187], 
        #                     [1, screen_width, 187], [1, screen_width, 187],[1, screen_width, 187], [1, screen_width, 187], [1, screen_width, 187],[1, screen_width, 187]])
        
        # low_bosses=np.array([[ 112, -1], [ 112, -1],[ 112, -1], [ 112, -1]])
        
        # high_bosses=np.array([[ 336, 1], [ 336, 1],[ 336, 1], [ 336, 1]])

        # low_bullets=np.array([[0, 71], [0, 71], [0, 71], [0, 71], [0, 71],
        #                      [0, 71], [0, 71], [0, 71], [0, 71], [0, 71],
        #                      [0, 71], [0, 71], [0, 71], [0, 71], [0, 71]])

        # high_bullets=np.array([[screen_width, screen_height], [screen_width, screen_height], [screen_width, screen_height], [screen_width, screen_height], [screen_width, screen_height],
        #                       [screen_width, screen_height], [screen_width, screen_height], [screen_width, screen_height], [screen_width, screen_height], [screen_width, screen_height],
        #                       [screen_width, screen_height], [screen_width, screen_height], [screen_width, screen_height], [screen_width, screen_height], [screen_width, screen_height]])

        # self.observation_space = Dict (
        #     {
        #         "score": Discrete(self.game.max_score+1),
        #         "lives": Discrete(self.game.lives),
        #         "agent": Discrete(screen_width),
        #         "aliens": Box(low=low_aliens, high=high_aliens, shape=(36, 3), dtype=np.uint8),
        #         "bosses": Box(low=low_bosses, high=high_bosses, shape=(4, 2), dtype=np.uint8),
        #         "bullets": Box(low=low_bullets, high=high_bullets, shape=(15,2), dtype=np.uint8)
        #     }
        # )
        

    def init_render(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        self.clock = pygame.time.Clock()
        

    def reset(self):
        self.duration = 0
        self.init_render()
        self.game = Game(screen_width, screen_height)
        return self.get_obs()

    def step(self, action):
        #Execute step in game
        self.game.step(action, self.duration)
        self.screen.fill("black")
        self.game.run(self.screen)
        self.duration += 1


        self.clock.tick(100000)
        pygame.display.flip()

        done = self.game.finished
        change = self.game.change

        ### Calculate reward
        if not done:
            reward = 1
            if change == 1:
                #Extra reward for killing an enemy
                reward = 100
            elif change == 2:
                #Extra reward for hitting a boss
                reward = 20
            if change == 3:
                #Penalty for losing a live
                reward = -1000
        else:
            reward = self.game.score + self.game.lives*500

        #Observation
        observation = self.get_obs()

        return observation, reward, done, {}
    
    def get_obs(self):
        rgb = pygame.surfarray.array3d(self.screen)
        return rgb

    def render(self):
        # self.screen.fill("black")
        # self.game.run(self.screen)
        pass