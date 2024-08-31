
#hacer una clase obj para leer el archivo obj, parseando lainformacion
import re
class Obj(object):
    def __init__(self, filename):
        #asumiendo que el archivo es un formato .obj
        with open(filename, "r") as file: 
            lines = file.read().splitlines()
        self.vertices = []
        self.textcoords = []
        self.normals = []
        self.faces = []
        for line in lines: 
            #si la linea no cuenta con un prefijo y un valor
            #seguimos a la siguiente linea
            # Este comando elimina espacios en blanco innecesarios
            # al final de un texto
            line = line.rstrip()
                        
            try:
                prefix, value = line.split(' ', 1) 
                
            except:
                continue #que continue a la siguiente line
            
            #dependiendo del prefijo parseamos y guardams la informacion en una lista
            if prefix == 'v': #vertices
                vertice = list(map(float,filter (None, value.split(' ')) ))  #filter(None, value.split(' ')) elimina las cadenas vacías de la lista antes de convertirlas en float
                self.vertices.append(vertice)
                
            elif prefix == 'vt':
                vts = list(map(float, filter(None, value.split(' ')) ))
                self.textcoords.append([vts[0],vts[1]])
                
            elif prefix == 'vn':
                norm = list(map(float, filter(None, value.split(' ')) ))
                self.normals.append(norm)
                
            elif prefix == 'f':
                #self.faces.append([list(map(int, filter(None, face.split('/')) )) for face in value.split(' ')])
                self.faces.append([list(map(int, filter(None, re.split(r'/|//', face)))) for face in value.split(' ')])
                #face = []
                #verts = value.split(' ')
                #for vert in verts:
                #    vert = list(map(int, face.split('/'))) 
                #    face.append(vert)
                #self.faces.append(face)
     
            
        