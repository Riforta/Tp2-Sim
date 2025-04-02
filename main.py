import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import random

seed = 42
random.seed(seed)


def generar_numeros(distribucion, n, parametros):
    arrayDatos = []
    if distribucion == 'uniforme':
        # Obtener los valores de a y b de los parametros
        a, b = parametros 
        for i in range(n):
            # Generacion de un random entre (0, 1) y escalado a (a, b)
            arrayDatos.append(a + random.random() * (b - a))
        # Devolucion del array, redondeado a 4 decimales
        return np.round(arrayDatos, 4)

    elif distribucion == 'exponencial':
        # Obtener el valor de lambda de los parametros
        lambd = parametros[0]

        for i in range(n):
            # Generacion de un random entre (0, 1) y escalado a (0, inf)
            arrayDatos.append(-np.log(1 - random.random()) / lambd)
        return np.round(arrayDatos, 4)
    
    elif distribucion == 'normal':
        media, desviacion = parametros

        # Box-Muller transformation 
        for i in range(n):
            r1, r2 = random.random(), random.random()

            z0 = np.sqrt(-2 * np.log(r1)) * np.sin(2 * np.pi * r2)
            z1 = np.sqrt(-2 * np.log(r1)) * np.cos(2 * np.pi * r2)
            arrayDatos.append(z0 * desviacion + media)
            arrayDatos.append(z1 * desviacion + media)
        
        return np.round(arrayDatos, 4)

    else:
        raise ValueError("Distribución no válida")

def calcular_histograma(datos, num_intervalos, limite_inferior, limite_superior):
    # Calcular histograma con los límites definidos por el usuario
    frecuencias, bins = np.histogram(datos, bins=num_intervalos, range=(limite_inferior, limite_superior))

    # Crear los intervalos correctamente alineados con los límites dados
    intervalos = []
    for i in range(len(bins) - 1):
        intervalo = (round(bins[i], 4), round(bins[i + 1], 4))
        intervalos.append(intervalo)

    # Crear la tabla de frecuencias
    tabla_frecuencias = pd.DataFrame({'Intervalo': intervalos, 'Frecuencia': frecuencias})

    return tabla_frecuencias, bins, frecuencias


def graficar_histograma(datos, num_intervalos, limite_inferior, limite_superior):
    plt.figure(figsize=(10, 6))
    
    # Asegurar que se usan los mismos límites del histograma
    plt.hist(datos, bins=num_intervalos, range=(limite_inferior, limite_superior), edgecolor='black', alpha=0.7)

    plt.xlabel('Valores')
    plt.ylabel('Frecuencia')
    plt.title(f'Histograma de la muestra con {num_intervalos} intervalos')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

if __name__ == "__main__":
    
    # Seleccion del usuario de la distribucion
    
    distribucion = input("Seleccione la distribución (uniforme, exponencial, normal): ").strip().lower()
    while distribucion not in ['uniforme', 'exponencial', 'normal']:
        distribucion = input("Distribución no válida. Seleccione la distribución (uniforme, exponencial, normal): ").strip().lower()

    # Seleccion del usuario del tamaño de la muestra
    n = int(input("Ingrese el tamaño de la muestra (máx. 1.000.000): "))
    while n <= 0 or n > 1000000:
        n = int(input("Tamaño de la muestra no válido. Ingrese un número entre 0 y 1.000.000:un "))
    
    # Seleccion del usuario de los parametros de la distribucion
    if distribucion == 'uniforme':
        a = float(input("Ingrese el valor del limite inferior: "))
        b = float(input("Ingrese el valor del limite superior: "))
        while a >= b:
            a = float(input("El limite inferior debe ser menor que el limite superior. Ingrese el valor del limite inferior: "))
            b = float(input("Ingrese el valor del limite superior: "))
            
        parametros = (a, b)

    elif distribucion == 'exponencial':
        lambd = float(input("Ingrese el valor de lambda: "))
        parametros = (lambd,)
        a = 0  # Para la exponencial, el límite inferior es 0
    elif distribucion == 'normal':
        media = float(input("Ingrese la media: "))
        desviacion = float(input("Ingrese la desviación estándar: "))
        parametros = (media, desviacion)

    else:
        print("Distribución no válida.")
        exit()
    
    # Generado de numeros aleatorios
    datos = generar_numeros(distribucion, n, parametros)

    if distribucion == 'exponencial':
        a = 0
        b = max(datos)
    elif distribucion == 'normal':
        a = media - 3 * desviacion
        b = media + 3 * desviacion

    num_intervalos = int(input("Seleccione el número de intervalos (10, 15, 20, 30): "))
    while num_intervalos not in [10, 15, 20, 30]:
        num_intervalos = int(input("Número de intervalos no válido. Seleccione entre 10, 15, 20 o 30: "))
    

    tabla_frecuencias, bins, frecuencias = calcular_histograma(datos, num_intervalos, a, b)

    print(tabla_frecuencias)
    
    graficar_histograma(datos, num_intervalos, a, b)
