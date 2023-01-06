import pygame
import pandas as pd
from stable_baselines3 import DQN

from CustomEnv import CustomEnv

n_tests = 1000
df = pd.DataFrame(columns=("reward", "duration", "remaining_lives", "final_state"))

env = CustomEnv()
model = DQN.load("./models/dqn_galaga_final.zip")
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
        lives = env.game.lives
        # print("Recompensa obtenida para para el episodio de prueba " + str(i + 1) + " es: " + str(total_reward))
        # print("La duracion del episodio de prueba " + str(i + 1) + " fue: " + str(duracion))
        # print("El intento de prueba " + str(i+1) + " termino en: " + str(state))

        test_sumary = [total_reward, duracion, lives, state]
        df.loc[len(df)] = test_sumary 

        i += 1
        total_reward = 0
df.to_csv('./tests_results/test_lvl_3.csv') 
pygame.quit()