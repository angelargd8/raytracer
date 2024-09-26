from re import S
import struct
from tkinter import SEL
from typing import Self #para generar tipo de variables con el tamaño especifico
from camara import Camara
import numpy as np
from math import tan, pi, isclose, atan2, acos
from Mathlib import barycentricCoords, normalizarVector
import pygame
import random

#funciones para asegurar el tamaño: 
def char(c): #lo que sea de tipo char, lo va a convertir en 1 byte
	#para crear una variable que ocupe 1 byte
	return struct.pack("=c", c.encode("ascii")) #"=c" que sea de tipo char

def word(w): #lo que sea de tipo word, lo va a convertir en 2 bytes
	#para crear una variable que ocupe 2 bytes
	return struct.pack("=h", w) #"=h" que sea de tipo short

def dword(d): #lo que sea de tipo dword, lo va a convertir en 4 bytes
	#para crear una variable que ocupe 4 bytes
	return struct.pack("=l", d) #"=l" que sea de tipo long


POINTS = 0
LINES = 1
TRIANGLES = 2
MAX_RECURSION_DEPTH = 3

class RendererRT(object):
	def __init__(self, screen):
		
		self.screen = screen
		_, _, self.width, self.height = screen.get_rect()
		
		self.camera = Camara()
		self.glViewport(0,0, self.width, self.height)
		self.glProjection()
		
	
		self.glColor(1,1,1)
		self.glClearColor(0,0,0)
		self.glClear()

		self.scene = [] #listado de objetos en la escena
		self.lights = [] #listado de luces en la escena, para escenas con multiples luces
		self.envMap = None

		
	def glCastRay(self, orig, direction, sceneObj = None, recursion = 0): 
		
		#para ya no seguir gnerando rayos
		if recursion >= MAX_RECURSION_DEPTH: 
			return None
		
		intercept = None #revisar si hay objeto o no 
		hit = None  #el que se regresa definitivamente
		depth= float('inf') #profundidad infinita
		
		#se va a recorrer cada objeto en la escena
		for obj in self.scene:
			if obj != sceneObj:
				intercept = obj.ray_intersect(orig, direction)
				#si hay interseccion
				if intercept != None: 
					if intercept.distance < depth:
						hit = intercept
						depth = intercept.distance
		return hit
	
	def glRender(self): 
		indices = [(i, j) for i in range(self.vpWidth) for j in range(self.vpHeight)]
		random.shuffle(indices)
		
		for i, j in indices:
			x = i + self.vpX
			y= j+ self.vpY

			if 0<= x < self.width and 0 <= y < self.height:
				#cooderdenadas normalizadas
				#que van de -1 a 1
				#valor del pixel en x
				pX  = ((x + 0.5 - self.vpX ) /self.vpWidth ) * 2 - 1
				#valor del pixel en y, se le suma 0.5 para que este en el centro 
				pY = ((y +0.5  - self.vpY ) /self.vpHeight ) * 2 - 1
					
				pX *= self.rightEdge 
				pY *= self.topEdge
					
				#se necesita origen y direccion para dibujar un rayo
				orig = self.camera.translate #origen de la camara
				dir = [pX, pY, -self.nearPlane] #direccion de la camara
				#la direccion su magnitud es 1, por eso se normaliza
				dir = normalizarVector(dir)
				#ya hay un origen y una direccion por pixel

				intercept = self.glCastRay(self.camera.translate, dir)
				
				color = [0,0,0]
				
				#generar el radio por cada uno de los pixeles
				#si el intercepto es valido se dibuja la superficie si no el envmaap
				if intercept!= None:
					color = intercept.obj.material.GetSurfaceColor(intercept, self)
				else: 
					color = self.glEnvMapColor(self.camera.translate, dir)
				
				self.glPoint(x, y, color)	
				pygame.display.flip()


	def glViewport(self, x, y, width, height):
		self.vpX = int(x) #posicion en x
		self.vpY = int(y) #posicion en y
		self.vpWidth = width #ancho
		self.vpHeight = height #alto
			
	def glProjection(self, n = 0.1, f = 1000, fov = 60): # n es el near, f es el far, fov = angulo de vista y esta en grados	
		self.nearPlane = n
		self.farPlane = f
		self.fov = fov  * pi / 180
		
		aspectRatio = self.vpWidth / self.vpHeight
		self.topEdge = tan(self.fov/2) * self.nearPlane
		self.rightEdge = self.topEdge * aspectRatio
		

	def glColor(self, r, g, b):
		r = min(1, max(0, r))
		g = min(1, max(0, g))		
		b = min(1, max(0, b))	
		
		self.currColor = [r,g,b]
		

	def glClearColor(self, r, g, b):
		r = min(1, max(0, r))
		g = min(1, max(0, g))		
		b = min(1, max(0, b))	
		
		self.clearColor = [r,g,b]
		

	def glClear(self):
		color = [int(i * 255) for i in self.clearColor] #convertir a entero
		self.screen.fill(color)
		
		self.frameBuffer = [[self.clearColor for y in range(self.height)]
							for x in range(self.width)]
		
		# self.zbuffer = [[float('inf') for y in range(self.height)]
		# 			   for x in range(self.width)]

	def glEnvMapColor(self, orig, dir):
		if self.envMap: 
			x = (atan2(dir[2], dir[0])/ (2 * pi) + 0.5)
			y = acos(-dir[1]) / pi 

			return self.envMap.getColor(x,y)

			
		return self.clearColor
	

	def glPoint(self, x, y, color = None):
		# Pygame empieza a renderizar desde la esquina
		# superior izquierda. Hay que voltear el valor y
		x = round(x)
		y = round(y)
		
		if (0<=x<self.width) and (0<=y<self.height):
			# Pygame recibe los colores en un rango de 0 a 255
			color = [int(i * 255) for i in (color or self.currColor)]
			self.screen.set_at((x, self.height - 1 - y), color)
			
			self.frameBuffer[x][y] = color
	
			
#Generacion del frame buffer				
	def glGenerateFrameBuffer(self, filename):
		
		with open(filename, "wb") as file:
			# Header
			# signature (2 bytes) | file size (4 bytes) | reserved (4 bytes) | offset (4 bytes)
			file.write(char("B")) #1 byte
			file.write(char("M")) #1 byte
			#info header 40 bytes
			file.write(dword(14 + 40 + (self.width * self.height * 3)))
			#reserved
			file.write(dword(0))
			#offset
			file.write(dword(14 + 40))
			
			# Info Header
			#size
			file.write(dword(40))
			#width
			file.write(dword(self.width))
			#height
			file.write(dword(self.height))
			#planes
			file.write(word(1))
			# bits per pixel
            #depende de cuanto bits le diga, este va a interpretar el interpretador de imagenes cuantos bits representan un pixel, aca es donde va la profundidad
			file.write(word(24)) # (rgb) = (8,8,8) bits 8+8+8=24 = 1pixel
			#compression
			file.write(dword(0))#0 para decirle que no tiene compression
			#image size
			file.write(dword(self.width * self.height * 3))
			#todaslasdemas tienen 4 bytes, realmente no importan
			file.write(dword(0))
			file.write(dword(0))
			file.write(dword(0))
			file.write(dword(0))
			
			#color table, donde se va a guardar todos los colores
            #recorre la cuadricula entera
            #pasa en cada x y y y agarra el color del lugar y se escribe en el archivo
			for y in range(self.height):
				for x in range(self.width):
					color = self.frameBuffer[x][y]
					color = bytes([color[2],
								   color[1],
								   color[0]])
					
					file.write(color)
													


	def glDrawPrimitives(self, buffer, vertexOffset):
		# El buffer es un listado de valores que representan
		# toda la informacion de un vertice (posicion, coordenadas
		# de textura, normales, color, etc.). El VertexOffset se
		# refiere a cada cuantos valores empieza la informacion
		# de un vertice individual
		# Se asume que los primeros tres valores de un vertice
		# corresponden a Posicion.
				
		if self.primitiveType == POINTS:
			
			# Si son puntos, revisamos el buffer en saltos igual
			# al Vertex Offset. El valor X y Y de cada vertice
			# corresponden a los dos primeros valores.
			for i in range(0, len(buffer), vertexOffset):
				x = buffer[i]
				y = buffer[i + 1]
				self.glPoint(x, y)
				
		elif self.primitiveType == LINES:
			
			# Si son lineas, revisamos el buffer en saltos igual
			# a 3 veces el Vertex Offset, porque cada trio corresponde
			# a un triangulo. 
			for i in range(0, len(buffer), vertexOffset * 3):
				for j in range(3):
					# Hay que dibujar la linea de un vertice al siguiente
					x0 = buffer[ i + vertexOffset * j + 0]
					y0 = buffer[ i + vertexOffset * j + 1]					
					
					# En caso de que sea el ultimo vertices, el siguiente
					# seria el primero
					x1 = buffer[ i + vertexOffset * ((j + 1)%3) + 0]
					y1 = buffer[ i + vertexOffset * ((j + 1)%3) + 1]
				
					self.glLine( (x0, y0), (x1, y1) )
					

				
				


		