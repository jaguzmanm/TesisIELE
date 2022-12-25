import pygame

from stable_baselines3 import DQN
from stable_baselines3.common.env_util import make_atari_env
import matplotlib.pyplot as plt

from CustomEnv import CustomEnv

env = CustomEnv()

model = DQN.load("./models/prueba_7.zip")
obs = env.reset()

i = 0
promReward = 0
while i < 5:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    
    promReward += float(reward)
    # time.sleep(0.05)
    # env.render()
    if done:
        duracion = env.duration
        obs = env.reset()
        print("Recompensa obtenida para para el episodio de prueba " + str(i + 1) + " es: " + str(promReward))
        print("La duracion del episodio de prueba " + str(i + 1) + " fue: " + str(duracion))
        i += 1
        promReward = 0
pygame.quit()