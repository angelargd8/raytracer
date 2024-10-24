from http.client import REQUEST_TIMEOUT
from Mathlib import *
from intercept import Intercept
from math import cos, pi
class Light(object):
    def __init__(self, color = [1,1,1], intensity = 1.0, lightType= "None"):
        self.color= color
        self.intensity = intensity
        self.lightType = lightType
        
    def GetLightColor(self,intercept= None):
        return [(i * self.intensity) for i in self.color]
    
    def GetSpecularColor(self, intercept, viewpos): #viewpos = vista dela camara
            return [0,0,0] #no hay color especular, color negro
            #la luz mbintal no tiene especulridad
        
class AmbientLight(Light):
    def __init__(self, color = [1,1,1], intensity = 1.0):
        super().__init__(color, intensity , "Ambient")
        
    
class DirectionalLight(Light):
    def __init__(self, color = [1,1,1], intensity = 1.0, direction = [0,-1,0]):
        super().__init__(color, intensity, "Directional")
        self.direction = normalizarVector(direction)
        
    def GetLightColor(self, intercept =None):
        lightColor =  super().GetLightColor()
        
        if intercept: 
            dir= [(i*-1) for i in self.direction]
            intensity = ProductoPunto(intercept.normal, dir  ) #intensidad de la luz
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.Ks)
            lightColor = [(i * intensity) for i in lightColor]
        return lightColor       
        
    def GetSpecularColor(self, intercept, viewpos):
        specColor = self.color
        
        if intercept:
            dir = [(i*-1) for i in self.direction]
            reflect = reflectVector(intercept.normal, dir)

            viewDir = subtract(viewpos, intercept.point)
            viewDir = normalizarVector(viewDir)
            #specular = ((V .R )^n)* Ks
            specularity = max(0,ProductoPunto(viewDir, reflect)) ** intercept.obj.material.spec
            specularity *= intercept.obj.material.Ks
            specularity *= self.intensity
            specColor = [(i)* specularity for i in specColor]
            
            
        return specColor
        

class PointLight(Light): 
    def __init__(self, color = [1,1,1], intensity = 1.0, position = [0,0,0]):
        super().__init__(color, intensity)
        self.position = position
        self.lightType = "Point"
        

    def GetLightColor(self, intercept = None):
        lightColor = super().GetLightColor(intercept)
        
        if intercept: 
            dir = subtract(self.position, intercept.point)
            R= magnitudVector(dir) #np.linalg.norm(dir)
            dir = normalizarVector(dir) #dir/ R
             
            intensity = ProductoPunto(intercept.normal, dir)
            intensity = max(0, min(1, intensity))
            intensity *= (1 - intercept.obj.material.Ks)
                        
            # ley de cuadrados inversos
            # attenuation = intensity / (R^2)
            # mientras r aumenta la atenuacion disminuye
            # r es la distancia del punto intercepto a la luz punto
            
            if R!= 0:
                intensity /= (R**2)
                
            lightColor = [(i * intensity) for i in lightColor]

        return lightColor
    
    def GetSpecularColor(self, intercept, viewpos):
        specColor = self.color
        
        if intercept:
            dir = subtract(self.position, intercept.point)
            R= magnitudVector(dir) #np.linalg.norm(dir)
            dir = normalizarVector(dir) #dir/ R
            
            reflect = reflectVector(intercept.normal, dir)

            viewDir = subtract(viewpos, intercept.point)
            viewDir = normalizarVector(viewDir)
            
            #specular = ((V .R )^n)* Ks
            specularity = max(0,ProductoPunto(viewDir, reflect)) ** intercept.obj.material.spec
            specularity *= intercept.obj.material.Ks
            specularity *= self.intensity
            
            if R!= 0:
                specularity /= (R**2)


            specColor = [(i)* specularity for i in specColor]
            
            
        return specColor
    
class SpotLight(PointLight):
    def __init__(self, color = [1,1,1], intensity = 1.0, position = [0,0,0], direction = [0,-1,0], innerAngle = 50, outerAngle = 50 ):
        super().__init__(color, intensity, position)
        self.direction = direction
        self.direction = normalizarVector(self.direction)
        self.innerAngle = innerAngle
        self.outerAngle = outerAngle
        self.lightType = "Spot"

    def GetLightColor(self, intercept= None): 
        lightColor = super().GetLightColor(intercept)
        
        if intercept == None:
            lightColor = [i * self.SpotlightAttenution(intercept) for i in lightColor]
        return lightColor
        
    def GetSpecularColor(self, intercept, viewpos):
        specularColor=  super().GetSpecularColor(intercept, viewpos)
        if intercept == None:
            specularColor = [i * self.SpotlightAttenution(intercept) for i in specularColor]
        return specularColor

    def SpotlightAttenution(self, intercept= None):
        if intercept == None:
            return 0
        
        wi = subtract(self.position, intercept.point)
        wi = normalizarVector(wi)
        
        innerAngleRads =self.innerAngle * (pi/180)
        outerAngleRads =self.outerAngle * (pi/180)

        attenuation =( (-ProductoPunto( self.direction,wi)) - cos(outerAngleRads)/ cos(innerAngleRads) - cos(outerAngleRads) )
        
        attenuation = min(1, max(0, attenuation))
        
        return attenuation