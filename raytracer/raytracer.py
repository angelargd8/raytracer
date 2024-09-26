

import pygame
from pygame.locals import *
from pygame.mask import MaskType
from gl import *
from model import Model
from figures import *
from material import *
from lights import *
from texture import Texture

#traslacion: mover un objeto de un punto a otro, x, y,z
#escala: tamanio del objeto, x, y, z
#rotacion: rotar un objeto en x, y, z

# width = 960
# height = 960
width = 256 #256#64
height = 256
screen = pygame.display.set_mode((width, height), pygame.SCALED)
clock = pygame.time.Clock()

rt=  RendererRT(screen)
rt.envMap = Texture('textures/streetNight.bmp')
#rt.glClearColor(0.5,0.0,0.0)
rt.glClear()

#crear materiales y asignar a cada uno de las esferas
brick = Material(diffuse = [1.0, 0.2, 0.2], spec = 128,Ks= 0.25)
grass = Material(diffuse = [0.2, 1.0, 0.2],spec = 64,Ks= 0.2)

mirror = Material(diffuse=[0.5,0.5,0.5], spec =128 ,  Ks=0.2, matType= REFLECTIVE )
blueMirror = Material(diffuse=[0.5,0.5,1.0], spec =128 ,  Ks=0.2, matType= REFLECTIVE )

# #textures
elote = Material(texture = Texture('textures/elote.bmp'), spec= 64, Ks = 0.1, matType= OPAQUE)
sandia = Material(texture = Texture('textures/sandia.bmp'), spec= 64, Ks = 0.1, matType= OPAQUE)

ground = Material(texture = Texture('textures/ground.bmp'), spec= 128, Ks = 0.2, matType= REFLECTIVE)
library = Material(texture = Texture('textures/library.bmp'), spec= 128, Ks = 0.2, matType= REFLECTIVE)
metal = Material(texture = Texture('textures/metal.bmp'), spec= 128, Ks = 0.2, matType= REFLECTIVE)
marble = Material(texture = Texture('textures/marble2.bmp'), spec= 64, Ks = 0.2, matType= REFLECTIVE)
steel = Material(texture = Texture('textures/steel.bmp'), spec= 128, Ks = 0.2, matType= REFLECTIVE)

plastic = Material(texture = Texture('textures/plastic.bmp'), spec= 128, Ks = 0.3, matType= TRANSPARENT)
water = Material(texture = Texture('textures/waterR2.bmp'), spec= 128, Ks = 0.3, matType= TRANSPARENT)
glass = Material(spec= 128, Ks= 0.2 , ior = 1.5, matType=TRANSPARENT)

#crear luces
rt.lights.append(DirectionalLight(direction = [-1,-1,-1], intensity = 0.4 ) )
# rt.lights.append(DirectionalLight(direction = [1,-0.5,-1], intensity = 0.4, color =[0,0,0] ) )
# rt.lights.append(DirectionalLight(direction = [0.5,-0.5,-1], intensity = 0.8, color =[1,1,1] ) )
rt.lights.append(AmbientLight(intensity = 0.3) )

# rt.scene.append(Sphere(position = [0,0,-5], radius = 1.5, material = glass)) #2.5
rt.scene.append(Sphere(position = [-3,1.5,-11], radius = 1, material = elote))
rt.scene.append(Sphere(position = [-3,-1.5,-11], radius = 1, material = sandia))
rt.scene.append(Sphere(position = [0,1.5,-10], radius = 1, material = plastic))
rt.scene.append(Sphere(position = [0,-1.5,-10], radius = 1, material = water))
rt.scene.append(Sphere(position = [3,1.5,-11], radius = 1, material = steel))
rt.scene.append(Sphere(position = [3,-1.5,-11], radius = 1, material = marble)) 

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