from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.clock import Clock

import RootWidget as root

# kivy3
from kivy3 import Renderer, Scene
from kivy3 import PerspectiveCamera
from kivy3.light import Light
from kivy3.loaders import OBJLoader

# geometry
from kivy3.extras.geometries import BoxGeometry
from kivy3 import Material, Mesh

# import da altri file
from glContext.Object import Object
from glContext.Objects import Objects_list

import kivy3.objects.mesh as mesh
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle
mesh.DEFAULT_MESH_MODE = "triangles"


class glContext(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        with self.canvas.before:
            # sfondo
            Color(0,0,0)
            self.background = Rectangle()
            # colore del modello
            Color(.9,.9,1)

        # renderer
        self.renderer = Renderer(shader_file="glContext\\simple.glsl")

        # scene
        self.scene = Scene()

        # objects
        self.objects = Objects_list()
        self.object_father = self.objects.get()

        # adding objects to scene
        self.scene.add(self.object_father)

        # camera
        self.camera = PerspectiveCamera(
            fov=75,    # distance from the screen
            aspect=0,  # "screen" ratio
            near=1,    # nearest rendered point
            far=100     # farthest rendered point
        )

        # rendering
        self.renderer.render(self.scene, self.camera)
        self.renderer.bind(size=self._adjust_aspect)
        self.add_widget(self.renderer) 


    def _adjust_aspect(self, *args):
        rsize = self.renderer.size
        aspect = rsize[0] / float(rsize[1])
        self.renderer.camera.aspect = aspect
        # adjust background
        self.background.pos = self.pos
        self.background.size = self.size
        

