#matriz x matriz
#matriz x vector
#nomalizar un vector
#magnitud de un vector
#mtriz de identidad
#inversa de una matriz
import re
from tkinter import N
import numpy as np
from math import e, pi, sin, cos, sqrt, isclose


def TranslationMatrix(x,y,z): 
   return  [[1,0,0,x],
            [0,1,0,y],
            [0,0,1,z],
            [0,0,0,1]]
                     

def ScaleMatrix(x,y,z):
   return  [[x,0,0,0],
            [0,y,0,0],
            [0,0,z,0],
            [0,0,0,1]]
  

def RotationMatrixX(pitch, yaw, roll):
   #convertir a radianes
   pitch *= pi/180
   yaw *= pi/180
   roll *= pi/180
   
   #creamos la matriz de toracion para eje
   pitchMat = [[1,0,0,0],
                [0,cos(pitch),-sin(pitch),0],
                [0,sin(pitch),cos(pitch),0],
                [0,0,0,1]]
   
   yawMat = [[cos(yaw),0,sin(yaw),0],
                [0,1,0,0],
                [-sin(yaw),0,cos(yaw),0],
                [0,0,0,1]]
   
   rollMat = [[cos(roll),-sin(roll),0,0],
            [sin(roll),cos(roll),0,0],
                [0,0,1,0],
                [0,0,0,1]]
   
   resul = multiplicacionMatrices(pitchMat, yawMat)
   resul = multiplicacionMatrices(resul, rollMat)
   return resul 

#multiplicacion de matrices
def multiplicacionMatrices(a, b):
    try:   
        n_filas= len(a)
        n_columnas= len(b[0])
        n_comun = len(b) #n de columns de a y filas de b
   
        resultadoM = [[0 for x in range(n_columnas)] for y in range(n_filas)] #crea la matriz con 0's
        for i in range(n_filas):
            for j in range(n_columnas):
                for k in range(n_comun):
                    resultadoM[i][j] += a[i][k] * b[k][j]
        
        return resultadoM
    except Exception: 
        print("")

#multiplicacion de elementos en la misma posicion xd
def multiplicacionElementos(a, b):
    try:
        n = len(a)
        n2 = len(b)
        if n != n2:
            print("No se pueden multiplicar los elementos")
            return 0
        else:
            resultado = [[0 for x in range(len(a[0]))] for y in range(n)]
            for i in range(n):
                for j in range(len(a[0])):
                    resultado[i][j] = a[i][j] * b[i][j]                   
            return resultado
    except Exception: 
        print("no se puede multiplicar")
        

def multiplicacionMatrizVector(matriz, vector):
   try: 
       n_filas = len(matriz)
       n_columnas = len(matriz[0])
       if n_columnas != len(vector):
           print("No se pueden multiplicar")
           return 0
       else: 
            resultado = [0 for x in range(n_filas)]
            for i in range(n_filas):
                for j in range(len(vector)):
                        resultado[i] += matriz[i][j] * vector[j]
            return resultado
   except Exception: 
       print("no se puede multiplicar")
       return None


def tolist(array):
    try:
        return list(array)
    except Exception: 
        print("")
        
def MatrizIdentidad(n):
    I = [[float(i == j) for i in range(n)] for j in range(n)]
    return I

def MatrizInversa(matriz): 
    n = len(matriz)
    #creamos la matriz identidad
    I= [[float(i == j) for i in range(n)] for j in range(n)]
    #matriz aumentada 
    AI = [matriz[i] + I[i] for i in range(n)]
    #gauss jordan
    
    for i in range(n):
        factor = AI[i][i]
        for j in range(2*n):
            AI[i][j] /= factor
            
        #hacer 0 los elementos de la columna
        for k in range(n):
            if k != i:
                factor = AI[k][i]
            
                for j in range(2*n):
                    AI[k][j] -= AI[i][j] * factor
    #extraer la matriz inversa
    #inversa = [AI[i][n:] for i in range(n)]
    inversa= [row[n:] for row in AI]
    return inversa
    
    
def normalizarVector(v):
   magnitudV = magnitudVector(v)
   return [v[i]/magnitudV for i in range(len(v))]


def magnitudVector(v):
   magnitudVector = sqrt(sum([v[i]**2 for i in range(len(v))]))
   return magnitudVector

def determinanteMatriz(matriz):
   if len(matriz) == 2:
       return matriz[0][0]*matriz[1][1] - matriz[0][1]*matriz[1][0]
   
   det = 0
   for c in range(len(matriz)):
       submatriz = [fila[:c] + fila[c+1:] for fila in (matriz[:0] + matriz[1:])]
       det += ((-1) ** c) * matriz[0][c] * determinanteMatriz(submatriz)
   return det

def ProductoCruz(v1, v2):
    c = [v1[1]*v2[2] - v1[2]*v2[1],
         v1[2]*v2[0] - v1[0]*v2[2],
         v1[0]*v2[1] - v1[1]*v2[0]]
    return c

def ProductoPunto(v1, v2):
    return sum(x * y for x,y in zip(v1, v2))

#n = numero a limitar
def clip(n, minn, maxn):
    return max(min(maxn, n), minn)


def barycentricCoords(A, B, C, P):
	
	# Se saca el area de los subtri�ngulos y del tri�ngulo
	# mayor usando el Shoelace Theorem, una f�rmula que permite
	# sacar el �rea de un pol�gono de cualquier cantidad de v�rtices.

	areaPCB = abs((P[0]*C[1] + C[0]*B[1] + B[0]*P[1]) - 
				  (P[1]*C[0] + C[1]*B[0] + B[1]*P[0]))

	areaACP = abs((A[0]*C[1] + C[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*C[0] + C[1]*P[0] + P[1]*A[0]))

	areaABP = abs((A[0]*B[1] + B[0]*P[1] + P[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*P[0] + P[1]*A[0]))

	areaABC = abs((A[0]*B[1] + B[0]*C[1] + C[0]*A[1]) - 
				  (A[1]*B[0] + B[1]*C[0] + C[1]*A[0]))

	# Si el �rea del tri�ngulo es 0, retornar nada para
	# prevenir divisi�n por 0.
	if areaABC == 0:
		return None

	# Determinar las coordenadas baric�ntricas dividiendo el 
	# �rea de cada subtri�ngulo por el �rea del tri�ngulo mayor.
	u = areaPCB / areaABC
	v = areaACP / areaABC
	w = areaABP / areaABC


	# Si cada coordenada est� entre 0 a 1 y la suma de las tres
	# es igual a 1, entonces son v�lidas.
	if 0<=u<=1 and 0<=v<=1 and 0<=w<=1 :
		return (u, v, w)
	else:
		return None
    
def subtract(x1, x2): 
    if len(x1) != len(x2):
        return None
    
    result = []
    for i in range(len(x1)):
        result.append(x1[i] - x2[i])
        
    return result 

def multiplyVectorScalar(vector, scalar):
    result = [element * scalar for element in vector]
    return result

def sumVectors(v1, v2):
    if len(v1) != len(v2):
        raise ValueError("Both vectors must have the same length")

    
    result = [v1[i] + v2[i] for i in range(len(v1))]
    
    return result

def multiplyVectorScalar(vector, scalar):
    result = [element * scalar for element in vector]
    return result

def reflectVector(normal, direccion):
    #las direcciones siempre tienen que estar normalizadas
    # normal = normalizarVector(normal)
    # direccion = normalizarVector(direccion)
    # R = 2* (N . L) * N - L #l es la luz
    reflect = 2* ProductoPunto(normal, direccion)
    reflect = multiplyVectorScalar(normal, reflect)
    reflect = subtract(reflect, direccion)
    reflect = normalizarVector(reflect)
    return reflect# subtract(direccion, multiplyVectorScalar(normal, 2 * ProductoPunto(direccion, normal)))
