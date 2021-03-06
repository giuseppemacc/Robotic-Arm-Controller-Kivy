from kivy3.loaders import OBJLoader
from kivy3.core.object3d import Object3D

from kivy3.extras.geometries import BoxGeometry
from kivy3 import Material, Mesh

from kivy.clock import Clock

# è la classe che gestisce gli object quindi per avere l'instanza bisogna
# accedere self.obj mentre gli altri metodi servono per gestire quell'object 
class Object():
    def __init__(self, source_file):
        self.obj = OBJLoader().load(f"glContext\\models\\{source_file}.obj")
        self.obj.name = source_file
        self._origin = [0,0,0]
        self._pos = [0,0,0]

        self._set_origin()
        self._set_pos()

    def get(self):
        return self.obj

    
    def set_rotation(self, axis, angle):
        if axis == "x":
            self.obj.rot.x = angle
        elif axis == "y":
            self.obj.rot.y = angle
        elif axis == "z":
            self.obj.rot.z = angle
        
        

    def set_pos(self,point):

        self._pos[0] = point[0]
        self._pos[1] = point[1] 
        self._pos[2] = point[2]

        self._set_pos()

    def get_pos(self):
        return self._pos

    def set_origin(self,point):

        self._origin[0] = point[0]
        self._origin[1] = point[1] 
        self._origin[2] = point[2]

        self._set_origin()
    
    def _set_origin(self):

        pos = self.obj.pos

        # mette l'opposto della posizione iniziale quindi mette l'origine al centro
        new_p = [-pos[0],-pos[1],-pos[2]]

        # mette l'orgine su point
        new_p[0]+=self._origin[0]
        new_p[1]+=self._origin[1]
        new_p[2]+=self._origin[2]

        for axis in ["x","y","z"]:
            self.obj._rotors[axis].origin = new_p

    def _set_pos(self):

        self.obj.pos.x = self._pos[0]
        self.obj.pos.y = self._pos[1]
        self.obj.pos.z = self._pos[2]


    def print_state(self):
        print(f"pos: {self.obj.pos}  origin: {self._origin}  rotation: {self.get().rotation}")
    