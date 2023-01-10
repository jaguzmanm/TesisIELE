import sys
import pygame
import pandas as pd

from CustomEnv import CustomEnv
from stable_baselines3 import DQN


screen_width = 448
screen_height = 586

def get_action():
    keys = pygame.key.get_pressed()
    action = 0
    if keys[pygame.K_a]:
        action = 1
    elif keys[pygame.K_d]:
        action = 2
    return action

def train_agent(nivel, n_steps, nombre_archivo):
    politica = "CnnPolicy"
    tasa_aprendizaje = 0.0001
    tamanio_memoria = 1000000
    tamanio_minibatch = 32
    gamma = 0.99
    tasa_exploracion = 0.05

    env = CustomEnv([screen_width, screen_height, nivel, 300000])

    model = DQN(policy=politica, env=env,learning_rate=tasa_aprendizaje, batch_size=tamanio_minibatch,
        buffer_size=tamanio_memoria, gamma=gamma, exploration_final_eps=tasa_exploracion,
        learning_starts=150000, verbose=1, tensorboard_log="./test_results/{}".format(nombre_archivo))
    model.learn(total_timesteps=n_steps)
    model.save("./models/{}.zip".format(nombre_archivo))

def play_game(env):
    total_reward = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        action = get_action()

        # calculate one step
        observation, reward, done, info = env.step(action)
        total_reward += reward
        if done:
            print("GAME OVER")
            print("reward:", total_reward)
            pygame.quit()
            sys.exit()


def test_agent(nombre_modelo, niveles, n_tests, mostrar_resumen, nombre_prueba, velocidad):
    model = DQN.load("./models/{}.zip".format(nombre_modelo))

    for nivel in niveles:
        env = CustomEnv([screen_width, screen_height, int(nivel), velocidad])
        df = pd.DataFrame(columns=("reward", "duration", "remaining_lives", "final_state"))

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
                lives = env.game.lives
                obs = env.reset()
                if mostrar_resumen == 1:
                    print("Recompensa obtenida para para el episodio de prueba " + str(i + 1) + " en el nivel " + nivel +  " es: " + str(total_reward))
                    print("La duracion del episodio de prueba " + str(i + 1) + " en el nivel " + nivel + " fue: " + str(duracion))
                    print("El intento de prueba " + str(i+1) + " en el nivel " + nivel + " termino en: " + str(state))

                i += 1
                test_sumary = [total_reward, duracion, lives, state]
                df.loc[len(df)] = test_sumary 

                total_reward = 0
        df.to_csv('./tests_results/{}_lvl_{}.csv'.format(nombre_prueba,nivel)) 
        pygame.quit()


menu = """\n====================================================================\n
Escoga la opción que desee ejecutar 
    1) Entrenar nuevo modelo
    2) Probar modelo existente
    3) Ejecutar el juego como jugador
    4) Salir\n
====================================================================\n"""

opcion = int(input(menu))
if opcion == 1:
    nombre_archivo = input("Ingrese el nombre del modelo: ")
    nivel = int(input("Ingrese el nivel sobre el cual desea entrenar el agente: "))
    n_steps = int(input("Ingrese la cantidad de timesteps de entrenamiento: "))

    train_agent(nivel, n_steps,nombre_archivo)
elif opcion == 2:
    nombre_prueba = input("Ingrese el nombre de la prueba: ")
    nombre_modelo = input("Ingrese el nombre del modelo a probar: ")
    niveles = input("Ingrese los nivel que desea probar (separados por comas): ").split(",")
    n_tests = int(input("Ingrese el numero de pruebas a ejecutar: "))
    esoger_vel = int(input("Desea maximizar los cuadros por segundo (1) o limitar a velocidad normal (2): "))
    mostrar_resumen = int(input("Desea imprimir en consola el resumen de cada prueba (1: si y 2: no): "))

    velocidad = 3000000

    if esoger_vel == 2:
        velocidad = 30

    test_agent(nombre_modelo, niveles, n_tests, mostrar_resumen, nombre_prueba, velocidad)

elif opcion == 3:
    nivel = int(input("Ingrese el nivel que desea jugar: "))
    env = CustomEnv([screen_width, screen_height, nivel, 30])
    play_game(env)

else:
    sys.exit()



