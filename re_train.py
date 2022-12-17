import pygame

from stable_baselines3 import DQN

from CustomEnv import CustomEnv

env = CustomEnv()

model = DQN.load("model_fixed_exp_rate.zip", tensorboard_log="./results_fixed_exp_rate")
model.set_env(env)

model.learn(total_timesteps=100000)
print("YA ENTRENO!!")
model.save("model_fixed_exp_rate_2")
