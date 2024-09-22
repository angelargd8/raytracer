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
from Mathlib import *

OPAQUE = 0
REFLECTIVE = 1
TRANSPARENT = 2

class Material(object):
    def __init__(self, diffuse, spec= 1.0, Ks= 0.0, texture= None, matType = OPAQUE):
        self.diffuse = diffuse
        self.spec = spec
        self.Ks = Ks
        self.texture = texture
        self.matType = matType
       
    def GetSurfaceColor(self, intercept, rendered, recursion = 0):
        #phong reflection model
        # LightColors = LightColors(incluye la ambiental) + Specular
        # FinalColor = DiffuseColor * LightColors (diffuse * el color de la iluminacion)
        lightColor =[0,0,0]
        reflectColor = [0,0,0]
        finalColor = self.diffuse

        if self.texture and intercept.texCoords:
            textureColor =self.texture.getColor(intercept.texCoords[0], intercept.texCoords[1])
            finalColor = [(finalColor[i] * textureColor[i]) for i in range(3)]

        for light in rendered.lights: 
            if light.lightType == "Directional":
                lightDir = [-i for i in light.direction]
                #origen, direccion de la luz, 
                shadowIntercept = rendered.glCastRay(intercept.point, lightDir, intercept.obj)
                
            if shadowIntercept == None: 
                lightColor=[(lightColor[i] + light.GetSpecularColor(intercept, rendered.camera.translate)[i]) for i in range(3)]
                
                if self.matType == OPAQUE:
                    lightColor = [(lightColor[i] + light.GetLightColor(intercept)[i]) for i in range(3)]


        if self.matType == REFLECTIVE:
            rayDir = [-i for i in intercept.rayDirection]
            reflect = reflectVector(intercept.normal, rayDir)
            reflectIntercept = rendered.glCastRay(intercept.point, reflect, intercept.obj, recursion + 1)
            if reflectIntercept != None:
                reflectColor = reflectIntercept.obj.material.GetSurfaceColor(reflectIntercept, rendered, recursion + 1)
            else:
                reflectColor = rendered.glEnvMapColor(intercept.point, reflect)
            

        
        finalColor = [(finalColor[i] * (lightColor[i]+reflectColor[i])) for i in range(3)]
        finalColor= [min(1,finalColor[i]) for i in range(3)]

        return finalColor