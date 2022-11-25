import sys
import numpy as np
import pygame

from CustomEnv import CustomEnv
from stable_baselines3 import A2C, DQN
from stable_baselines3.common.env_checker import check_env


def get_action():
    keys = pygame.key.get_pressed()
    action = 0
    if keys[pygame.K_a]:
        action = 1
    elif keys[pygame.K_d]:
        action = 2

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_SPACE]:
        action += 3

    return action



env = CustomEnv()

# check_env(env)
# print("TO DO GUD")

model = DQN("CnnPolicy", env, buffer_size=5000, verbose=1)
model.learn(total_timesteps=100000)
print("YA ENTRENO!!")
model.save("dqn_galaga")


# while True:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             sys.exit()

#     action = get_action()

#     # calculate one step
#     observation, reward, done, info = env.step(action)
#     if reward != 0:
#         print(reward)   
#     if done:
#         print("GAME OVER")
#         print("reward:", reward)
#         pygame.quit()
#         sys.exit()

# pygame.quit()
# sys.exit()