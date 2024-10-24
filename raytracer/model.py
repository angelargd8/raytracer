#aqui se va a guardar la informacion 
from obj import Obj
from Mathlib import *
from texture import Texture

class Model(object):
    def __init__(self, filename):
        objFile = Obj(filename)
        
        self.vertices = objFile.vertices
        self.textCoords= objFile.textcoords
        self.faces = objFile.faces
        self.normals = objFile.normals
        
        self.texture = None
        self.vertexShader = None
        self.fragmentShader = None

        
        #self.textcoords = objFile.textcoords
        self.translate = [0,0,0]
        self.rotate = [0,0,0]
        self.scale  = [1,1,1]
        
        self.texture = None
    
    def LoadTexture(self, filename):
        self.texture = Texture(filename)

    def GetModelMatrix(self):
        traslateMat = TranslationMatrix(self.translate[0],
                                        self.translate[1],
                                        self.translate[2])
        
        rotateMat = RotationMatrixX(self.rotate[0],
                                    self.rotate[1],
                                    self.rotate[2])
        
        scaleMat = ScaleMatrix(self.scale[0],
                               self.scale[1],
                                self.scale[2])
        
        #multiplicar los elementos
        res= multiplicacionMatrices(traslateMat, rotateMat)
        res= multiplicacionMatrices(res, scaleMat)
        return res #res de resultado xd

    