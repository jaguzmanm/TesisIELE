import sys
import numpy as np
import pygame

from CustomEnv import CustomEnv
from stable_baselines3 import A2C, DQN
from stable_baselines3.common.env_checker import check_env

from PIL import Image


def get_action():
    keys = pygame.key.get_pressed()
    action = 0
    if keys[pygame.K_a]:
        action = 1
    elif keys[pygame.K_d]:
        action = 2

    # keys = pygame.key.get_pressed()
    
    # if keys[pygame.K_SPACE]:
    #     action += 3

    return action



env = CustomEnv()

check_env(env)
print("TO DO GUD")

# model = DQN("MlpPolicy", env, buffer_size=15000, learning_starts=25000, exploration_final_eps=0.1, verbose=1, tensorboard_log="./results/prueba_5")
# model.learn(total_timesteps=500000)
# print("YA ENTRENO!!")
# model.save("./models/prueba_5")


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