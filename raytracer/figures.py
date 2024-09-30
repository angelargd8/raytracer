from re import T
from Mathlib import *
import numpy as np
from intercept import Intercept
from math import atan, atan2, acos, pi, isclose
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
    

class Plane(Shape):
    def __init__(self, position, normal, material):
        super().__init__(position, material)
        self.normal = normal 
        normalizarVector(self.normal)
        self.type = "Plane"
    
    def ray_intersect(self, orig, dir):
        # distancia = ((planePos - rayOrig) o normal)/ (rayDir o normal)
        denom = ProductoPunto(dir, self.normal) #denominador
        
        if isclose(0, denom): 
            return None
        
        num = ProductoPunto(subtract(self.position, orig), self.normal)  #numerador
        
        t = num / denom

        if t<0 :
            return None
        
        # P = orig + dir * t0
        P = sumVectors(orig, multiplyVectorScalar(dir, t))
        
        return Intercept(point = P, 
                         normal = self.normal,
                         distance = t,
                         texCoords=None,
                         rayDirection= dir, 
                         obj = self)
        
        

class Disk(Plane):
    def __init__(self, position, normal, radius, material):
        super().__init__(position, normal ,material)
        self.radius = radius
        self.type = "Disk"
        
    def ray_intersect(self, orig, dir): 
        planeIntercept = super().ray_intersect(orig, dir)
        
        if planeIntercept is None:
            return None
        
        
        contact = magnitudVector(subtract(planeIntercept.point, self.position))
        
        if contact > self.radius:
            return None

        return planeIntercept
    
class AABB(Shape): #cubo -- estas figuras carecen de rotacion
    # axis aligned bounding box - alineado de los ejes - bounding box caja sin limites
    def __init__(self, position, sizes, material):
        super().__init__(position, material)
        self.sizes = sizes
        self.type = "AABB"

        #planos
        self.planes = []
            
        rightPlane = Plane([self.position[0] + sizes[0]/2, self.position[1], self.position[2]], [1,0,0], material)
        leftPlane = Plane([self.position[0] - sizes[0]/2, self.position[1], self.position[2]], [-1,0,0], material)

        
        upPlane = Plane([self.position[0], self.position[1] + sizes[1]/2, self.position[2]], [0,1,0], material)
        downPlane = Plane([self.position[0], self.position[1] - sizes[1]/2, self.position[2]], [0,-1,0], material)

        
        frontPlane = Plane([self.position[0], self.position[1], self.position[2] + sizes[2]/2], [0,0,1], material)
        backPlane = Plane([self.position[0], self.position[1] , self.position[2] - sizes[2]/2], [0,0,-1], material)


        self.planes.append(rightPlane)
        self.planes.append(leftPlane)
        self.planes.append(upPlane)
        self.planes.append(downPlane)
        self.planes.append(frontPlane)
        self.planes.append(backPlane)
            
        #bounds
        self.boundsMin = [0,0,0]
        self.boundsMax = [0,0,0]
            
        epsilon = 0.001
            
        for i in range(3):
            self.boundsMin[i] = position[i] - (epsilon + sizes[i]/2)
            self.boundsMax[i] = position[i] + (epsilon + sizes[i]/2)
        
    def ray_intersect(self, orig, dir):
        
        intercept = None
        t = float("inf")

        for plane in self.planes:
            planeIntercept = plane.ray_intersect(orig, dir)

            if planeIntercept is not None:
                planePoint = planeIntercept.point

                if self.boundsMin[0] <= planePoint[0] <= self.boundsMax[0]:
                    if self.boundsMin[1] <= planePoint[1] <= self.boundsMax[1]:
                        if self.boundsMin[2] <= planePoint[2] <= self.boundsMax[2]:

                            if planeIntercept.distance < t:
                                t = planeIntercept.distance
                                intercept = planeIntercept

        if intercept == None:
            return None
        
        u, v = 0, 0
        
        if abs( intercept.normal[0]) > 0:
            #mapeat las uvs para el eje x, usando las coordenadas Y y Z
            u = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]
            

        if abs( intercept.normal[1]) > 0:
            #mapeat las uvs para el eje y, usando las coordenadas X y Z
            u = (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[2] - self.boundsMin[2]) / self.sizes[2]
             

        if abs( intercept.normal[2]) > 0:
            #mapeat las uvs para el eje y, usando las coordenadas X y Z
            u =  (intercept.point[0] - self.boundsMin[0]) / self.sizes[0]
            v = (intercept.point[1] - self.boundsMin[1]) / self.sizes[1]
            

        u = min(0.999, max(0, u))
        v = min(0.999, max(0, v))

        return Intercept(point=intercept.point,
                         normal=intercept.normal,
                         distance=t, 
                         texCoords=[u,v],
                         rayDirection=dir,
                         obj=self)
