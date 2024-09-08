

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
width = 64 #
height = 64
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt=  RendererRT(screen)

#crear materiales y asignar a cada uno de las esferas
brick = Material(diffuse = [1.0, 0.2, 0.2], spec = 128,Ks= 0.25)
grass = Material(diffuse = [0.2, 1.0, 0.2],spec = 64,Ks= 0.2)

#crear luces
rt.lights.append(DirectionalLight(direction = [-1,-1,-1], intensity = 0.8 ) )
rt.lights.append(DirectionalLight(direction = [0.5,-0.5,-1], intensity = 0.6, color =[0,0,1] ) )

rt.lights.append(AmbientLight(intensity = 0.1) )


rt.scene.append(Sphere(position = [0,0,-5], radius = 1.5, material = brick))
rt.scene.append(Sphere(position = [1,1,-3], radius = 0.5, material = grass))
#con la especularidad se suele usarpotenciasde2

#rt.scene.append(Sphere(position = [2,-3, -10], radius = 0.5, material = grass))

rt.glRender()


isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                isRunning = False
               
   
    pygame.display.flip()
    clock.tick(60)


pygame.quit()