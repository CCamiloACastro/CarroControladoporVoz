import numpy as np

np.random.seed(100)

#crea una matriz de 50 enteros aleatorios entre 0 y 10
var1 = np.random.randint(0, 10, 50)

#crear una matriz correlacionada positivamente con algo de ruido aleatorio
var2 = var1 + np.random.normal (0, 10, 50)

#calcular la correlación entre las dos matrices
correlacion = np.corrcoef(var1, var2)
print(correlacion)

