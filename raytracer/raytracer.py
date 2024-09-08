

import pygame
from pygame.locals import *
from gl import *
from model import Model
from figures import *
from material import Material
from lights import *


#traslacion: mover un objeto de un punto a otro, x, y,z
#escala: tamanio del objeto, x, y, z
#rotacion: rotar un objeto en x, y, z

# width = 960
# height = 960
width = 480 #128 #256 #64 #480
height = 480
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt=  RendererRT(screen)

#crear materiales y asignar a cada uno de las esferas
brick = Material(diffuse = [1.0, 0.2, 0.2], spec = 256,Ks= 0.25)
grass = Material(diffuse = [0.2, 1.0, 0.2],spec = 64,Ks= 0.2)
nieve = Material(diffuse = [1.0, 1.0, 1.0], spec = 64,Ks= 0.2)
ojos = Material(diffuse = [0.0, 0.0, 0.0], spec = 1024,Ks= 1.0)
botones = Material(diffuse = [0.0, 0.0, 0.0], spec = 128,Ks= 0.5)
nariz = Material(diffuse = [1.0, 0.5, 0.0], spec = 128,Ks= 0.3)

#crear luces
rt.lights.append(DirectionalLight(direction = [-1,-1,-1], intensity = 1 ) )
rt.lights.append(DirectionalLight(direction = [0.5,-0.5,-1], intensity = 0.5, color =[0,0,1] ) )
rt.lights.append(AmbientLight(intensity = 0.1) )

#bolas de nieve
rt.scene.append(Sphere(position = [0,1.6,-4], radius = 1, material = nieve))
rt.scene.append(Sphere(position = [0,0,-5], radius = 1.5, material = nieve))
rt.scene.append(Sphere(position = [0,-2,-6], radius = 2, material = nieve))
#botones
rt.scene.append(Sphere(position = [0,-2,-4], radius = 0.4, material = botones))
rt.scene.append(Sphere(position = [0,-0.5,-3], radius = 0.25, material = botones))
rt.scene.append(Sphere(position = [0,0.1,-3], radius = 0.15, material = botones))
#cara
rt.scene.append(Sphere(position = [0,1.1,-3], radius = 0.15, material = nariz))
rt.scene.append(Sphere(position = [0.3,1.4,-3], radius = 0.1, material = ojos))
rt.scene.append(Sphere(position = [-0.3,1.4,-3], radius = 0.1, material = ojos))
rt.scene.append(Sphere(position = [-0.3,0.85,-3], radius = 0.09, material = botones))
rt.scene.append(Sphere(position = [0,0.75,-3], radius = 0.09, material = botones))
rt.scene.append(Sphere(position = [0.3,0.85,-3], radius = 0.09, material = botones))


rt.glRender()

isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
            elif event.key == pygame.K_S:
                rt.glGenerateFrameBuffer("output.bmp")
               
   
    pygame.display.flip()
    clock.tick(60)

rt.glGenerateFrameBuffer("output.bmp")
pygame.quit()