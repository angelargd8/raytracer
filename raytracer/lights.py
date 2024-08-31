from Mathlib import *
class Light(object):
    def __init__(self, color = [1,1,1], intensity = 1.0, lightType= "None"):
        self.color= color
        self.intensity = intensity
        
    def GetLightColor(self,intercept= None):
        return [(i * self.intensity) for i in self.color]
    
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
            lightColor = [(i * intensity) for i in lightColor]
        return lightColor       
        
