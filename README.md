# Utilizando Técnicas de Aprendizaje por Refuerzo para enseñar a un agente a jugar el videojuego "Galaga"
 
 **Autor:** John Alexander Guzmán Moyano\
 **Código de Estudiante:** 201713338
 
 Proyecto de Grado\
 Universidad de los Andes\
 Departamento de Ingeniería Electríca y Electrónica
 
 ## Requerimientos
 - Python 3.10.2
 - PyGame
 - TensorFlow
 - Stable Baselines3
 - Pillow
 - Scikit-Image
 - Gym
 - Numpy
 - Pandas
 - Matplotlib
 
## Instrucciones Para Ejecutar el Proyecto
#### Instalar python 3.10.2
Dirigirse a la [pagina oficial de Python](https://www.python.org/), en la pestaña de **Downloads** dirigirse a **All releases**, buscar la versión 3.10.2 y descargarla

#### Instalar virtualenv
    pip install virtualenv
    
#### Crear un entrono virtual 
    python -m venv "env"
    
#### Activar el entorno virtual
    env\Scripts\activate.bat
    
#### Instalar las dependencias desde requirements.txt
    pip install -r requirements.txt
    
#### Ejecutar el proyecto corriendo el archivo main.py
    python main.py
 
#### Vizualizar resultados del entrenamiento en TensorBoard
Se debe ejecutar el comando en consola:

    tensorboard dev upload --logdir ./results/{nombre_modelo}  --name "{Titulo}" --description "{Descripcion}"
