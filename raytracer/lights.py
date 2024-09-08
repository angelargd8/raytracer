from Mathlib import *
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
            spectColor = [(i)* specularity for i in specColor]
            
            
        return specColor
        