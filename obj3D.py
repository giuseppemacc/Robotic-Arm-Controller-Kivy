from kivy.clock import Clock
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.resources import resource_find
from kivy.graphics.transformation import Matrix
from kivy.graphics.opengl import *
from kivy.graphics import *
from objImporter import Obj
from kivy.graphics.context_instructions import Color, PopMatrix, PushMatrix, Rotate, Scale, Translate, UpdateNormalMatrix
from kivy.graphics.instructions import Callback, RenderContext
from kivy.graphics.vertex_instructions import Mesh


class Object3D(Widget):
    def __init__(self,source_file,color = [1,1,1,1],**kwargs):
        
        self.source_file = source_file
        self.color = color
        self.canvas = RenderContext(compute_normal_mat=True)
        self.canvas.shader.source = resource_find('shaders.glsl')
        self.scene = Obj(resource_find(self.source_file),self.color)
        self.size_context = [0,0]
        self.tras = 2
        super().__init__()
        
        with self.canvas:
            self.cb = Callback(self.setup_gl_context)
            PushMatrix()
            self.setup_scene()
            PopMatrix()
            self.cb = Callback(self.reset_gl_context)

        Clock.schedule_interval(self.update_glsl, 1 /60)

    def setup_gl_context(self, *args):
        glEnable(GL_DEPTH_TEST)

    def reset_gl_context(self, *args):
        glDisable(GL_DEPTH_TEST)

    def update_glsl(self, delta):
        #:
            #----questo funziona----asp = self.width / float(self.height) 

            #asp = self.get_root_window().width / self.get_root_window().height

            #print("width> ",self.width, "---  height> ",self.height)
            #print("//> ",self.width/self.height)
            #asp = 1
            #proj = Matrix().view_clip(-asp, asp, -1, 1, 1, 100, 1)
            #Matrix().view_clip()
            #----questo funziona-----proj = Matrix().view_clip(-asp, asp, -asp, asp, 1, 100, 1)    
        aspx = 1
        aspy = 1
        width_c = self.size_context[0]
        height_c = self.size_context[1]
        if width_c != 0 and height_c != 0:      
            scalefac = 1000#width_c+height_c#1/500 
            #modelMatrix.ortho( -width_c/scalefac, width_c/scalefac, -height_c/scalefac, height_c/scalefac) 
            #print("width>",width_c," height>",height_c," w/h>",width_c/height_c)
            #aspy = (1 - (height_c/width_c))
            #aspx = (1 - (width_c/height_c))
            aspx = width_c/scalefac
            aspy = height_c/scalefac
            #aspx = 0
            #aspy = 0
        else:
            width_c = 1
            height_c = 1
            
        #proj = Matrix().view_clip(-aspx,aspx, -aspy,aspy,    1,10,-1) # unsizabile
        proj = Matrix().view_clip(-width_c/height_c/2, width_c/height_c/2,  -1/2, 1/2, 1,10,1) # sizabile
        self.canvas['projection_mat'] = proj
        
        
        

    def setup_scene(self):
        #self.tras += 0.01
        #print(self.tras)
        
        PushMatrix()
        
        #Scale(0)
        
        self.tras = Translate(0,0.5,-3)
        
        self.rot  = Rotate()
        self.rot1 = Rotate()
        self.rot2 = Rotate()
        self.rot3 = Rotate()
        self.rot4 = Rotate()
        self.rot5 = Rotate()
        self.rot6 = Rotate()

        UpdateNormalMatrix()
        self.mesh = Mesh(
            vertices=self.scene.vertices,
            indices=self.scene.indices,
            fmt=self.scene.vertex_format,
            mode='triangles'
        )
        PopMatrix()
        
    def Punto_Medio(self):
        vertices = []
        for vertex_i in range(0,len(self.scene.vertices),11):
            vertices.append([
             self.scene.vertices[vertex_i  ], 
             self.scene.vertices[vertex_i+1], 
             self.scene.vertices[vertex_i+2] 
            ])
                    
        indices = self.scene.indices
        
        def Pm(p1,p2):
            return [ (p1[0]+p2[0])/2, (p1[1]+p2[1])/2, (p1[2]+p2[2])/2 ]
        
        return Pm(vertices[0],vertices[7])