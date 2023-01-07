import sys
import pygame

from CustomEnv import CustomEnv
from stable_baselines3 import DQN



def get_action():
    keys = pygame.key.get_pressed()
    action = 0
    if keys[pygame.K_a]:
        action = 1
    elif keys[pygame.K_d]:
        action = 2
    return action

screen_width = 448
screen_height = 586
nivel = 4

env = CustomEnv([screen_width, screen_height, nivel])

# check_env(env)
# print("TO DO GUD")

# model = DQN("MlpPolicy", env, learning_starts=10000, exploration_final_eps=0.1, verbose=1, tensorboard_log="./results/prueba_6")

# model = DQN("CnnPolicy", env, learning_starts=150000, verbose=1, tensorboard_log="./results/dqn_galaga_final")
# model.learn(total_timesteps=15000000)
# print("YA ENTRENO!!")
# model.save("./models/dqn_galaga_final")

# buffer_size=10000,

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    action = get_action()

    # calculate one step
    observation, reward, done, info = env.step(action)


    if reward != 0:
        print(reward)   

    if done:
        print("GAME OVER")
        print("reward:", reward)
        pygame.quit()
        sys.exit()
