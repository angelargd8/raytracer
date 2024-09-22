from re import T
from Mathlib import *
import numpy as np
from intercept import Intercept
from math import atan, atan2, acos, pi
#figuras

class Shape(object):
    def __init__(self, position, material):
        self.position = position
        self.material = material
        self.type= "None"
        
    def ray_intersect(self, orig, dir):
        return None
    


class Sphere(Shape):
    def __init__(self, position, radius, material): 
        super().__init__( position, material)
        self.radius = radius
        self.material = material
        self.type = "Sphere"
        
    def ray_intersect(self, orig, dir): 
        L = subtract(self.position, orig) #cambiar 
        # d es el punto más cercano al centro de la esfera
        
        tca = ProductoPunto(L, dir)
        
        d = (magnitudVector(L) ** 2 - tca ** 2) ** 0.5
        
        if d > self.radius:
            return None
        
        thc = (self.radius ** 2 - d ** 2) ** 0.5 #pitagoras
        
        t0= tca - thc
        t1= tca + thc
        
        #return d<= self.radius #si d es menor o igual al radio, entonces hay intersección
        
        #cuando esta atrs de la camara
        if t0 <0:
            t0 = t1
        #esta enmedio
        if t0 <0:
            return None
        
        #puntos de contacto 
        # P0 = orig +dir * t0
        # P1 = orig +dir * t1
        p = sumVectors(orig, multiplyVectorScalar(dir, t0))
        normal = normalizarVector(subtract(p, self.position))
        
        u = (atan2(normal[2], normal[0])/(2 * pi)+0.5 )
        v= acos(-normal[1])/pi

        return Intercept(point = p, 
                         normal = normal,
                         distance = t0,
                         texCoords=[u,v],
                         rayDirection= dir, 
                         obj = self)
    


    
    