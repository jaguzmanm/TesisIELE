import pygame
import pandas as pd
from stable_baselines3 import DQN

from CustomEnv import CustomEnv

n_tests = 10
df = pd.DataFrame(columns=("reward", "duration", "final_state"))

env = CustomEnv()
model = DQN.load("./models/prueba_8.zip")
obs = env.reset()

i = 0
total_reward = 0
while i < n_tests:
    action, _states = model.predict(obs, deterministic=True)
    obs, reward, done, info = env.step(action)
    
    total_reward += float(reward)

    if done:
        duracion = env.duration
        state = env.final_state
        obs = env.reset()
        # print("Recompensa obtenida para para el episodio de prueba " + str(i + 1) + " es: " + str(total_reward))
        # print("La duracion del episodio de prueba " + str(i + 1) + " fue: " + str(duracion))
        # print("El intento de prueba " + str(i+1) + " termino en: " + str(state))

        test_sumary = [total_reward, duracion, state]
        df.loc[len(df)] = test_sumary 

        i += 1
        total_reward = 0
df.to_csv('./tests_results/test_file.csv') 
pygame.quit()