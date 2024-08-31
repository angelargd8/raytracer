#el material determina como se comporta la luz al interactuar con la superficie de un objeto
#diffuse: color base del objeto/el color de la superdicie
#specular: brillo del objeto
#albedo: brillo del objeto
#reflactance: reflejo del objeto
#refractance: refraccion del objeto
#roughness: rugosidad del objeto
#metallic: metalico del objeto
#ior: indice de refraccion del objeto
#transparency: transparencia del objeto
#emissive: emision del objeto
#normal: normal del objeto
#scene: escena del objeto
#rayDirection: direccion del rayoq
#rayOrigin: origen del rayo
from lights import *

class Material(object):
    def __init__(self, diffuse):
        self.diffuse = diffuse
       
    def GetSurfaceColor(self, intercept, rendered):
        #phong reflection model
        # LightColors = LightColors(incluye la ambiental) + Specular
        # FinalColor = DiffuseColor * LightColors (diffuse * el color de la iluminacion)
        lightColor =[0,0,0]
        finalColor = self.diffuse
        
        for light in rendered.lights: 
            currentLightColor= light.GetLightColor(intercept)
            lightColor=[(lightColor[i] +currentLightColor[i]) for i in range(3)]
            
        finalColor= [(finalColor[i] * lightColor[i]) for i in range(3)]
        
        finalColor = [min(1, finalColor[i]) for i in range(3)]
        return finalColor