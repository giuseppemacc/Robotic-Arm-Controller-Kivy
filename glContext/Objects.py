from glContext.Object import Object
from kivy.clock import Clock

import RootWidget as root


class Objects_list():
    def __init__(self):
        super().__init__()

        self.obj_father = Object("base")
        self.obj_father.set_pos([0,-8,-40])

        self.obj_chain = [
            self.obj_father,
            Object("nodo"),
            Object("braccio"),
            Object("nodo"),
            Object("braccio"),
            Object("nodo"),
            Object("braccio"),
            Object("nodo"),
            Object("punta")
        ]

        for i in range(1,len(self.obj_chain)):
           self.obj_chain[i-1].get().add(self.obj_chain[i].get())

        for i in range(1,len(self.obj_chain)):
            pos = [0,0,0]
            origin = [0,0,0]

            if i == 1:
                pos[1] = .5
                origin[1] = 0
            elif self.obj_chain[i].get().name == "nodo":
                pos[1] = 2
                origin[1] = 0
            elif self.obj_chain[i].get().name == "braccio":
                pos[1] = 2 
                origin[1] = 0
            elif self.obj_chain[i].get().name == "punta":
                pos[1] = .5
                origin[1] = 0
            
            self.obj_chain[i].set_pos(pos)
            self.obj_chain[i].set_origin(origin)

        Clock.schedule_interval(self.rot, 1/60)

    def rot(self,dt):
        self.obj_chain[1].set_rotation("y",root.RootWidget.angles[0])
        cont = 1
        for i in range(2,len(self.obj_chain),2):
            if i == 2:
                self.obj_chain[i].set_rotation("z", root.RootWidget.angles[cont]-90)
            else:
                self.obj_chain[i].set_rotation("z",root.RootWidget.angles[cont]-90)
            cont += 1
        
    def get(self):
        return self.obj_father.get()

