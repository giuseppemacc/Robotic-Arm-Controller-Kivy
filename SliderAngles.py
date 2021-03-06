""" --- import da kivy --- """
from kivy.uix.slider import Slider
from kivy.uix.widget import Widget
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.clock import Clock

# import del RootWidget
import RootWidget as root
from kivy.graphics.context_instructions import Color
from kivy.graphics.vertex_instructions import Rectangle

class SliderAnglesBox(BoxLayout):

    def __init__(self,axis = [],**kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        # axis contiene nome e [max e min] delli slider da creare
        self.axis = axis
        # nAxis è il numero di assi di rotazione
        self.nAxis = len(self.axis)
        
        # nameAxis indica i nome degli assi
        self.nameAxis = []
        
        # min_maxAxis contiene i massimi e minimi di ogni asse
        self.min_maxAxis = []
        for asse in self.axis:
            self.nameAxis.append(asse[0])
            self.min_maxAxis.append(asse[1])       

        # slider contiene l'insieme degli slider che sono tanti quanti nAxis
        self.sliders = []
        for n in range(self.nAxis):
            slide = Slider(min=self.min_maxAxis[n][0],max=self.min_maxAxis[n][1])
            self.sliders.append(slide)

        # aggiunte grafiche
        self.slide_name_label = []
        self.angles_label = Angles_Label()

        for name in self.nameAxis:
            self.slide_name_label.append(Label(text=name))

        for i in range(self.nAxis):
            box = BoxLayout()
            self.slide_name_label[i].size_hint = [.2,1]
            self.angles_label.labels[i].size_hint = [.1,1]
            self.sliders[i].size_hint = [.7,1]
            box.add_widget(self.slide_name_label[i])
            box.add_widget(self.angles_label.labels[i])
            box.add_widget(self.sliders[i])
            self.add_widget(box)
        
        Clock.schedule_interval(self.set_values,1/60)
 
    def set_values(self,dt):
        # slide_angles contiene i valori degli slider
        slide_angles = [slide.value for slide in self.sliders]

        if root.RootWidget.master:
            # imposta angles contenuto nel RootWidget con quello degli slider
            root.RootWidget.angles = slide_angles
        else:
            # imposta il valori degli slider con quello di angles contenuto nel RootWidget
            i = 0
            for slide in self.sliders:
                slide.value = root.RootWidget.angles[i]
                i+=1

# questa classe contiene dei label con il valore di ogni angles
class Angles_Label():
    def __init__(self):
        self.labels = []
        for i in range(len(root.RootWidget.axis)):
            self.labels.append(Label())
        Clock.schedule_interval(self.refresh,1/60)

    def refresh(self,dt):
        if len(root.RootWidget.angles) != 0:
            for i in range(len(root.RootWidget.axis)): 
                try:              
                    self.labels[i].text = str(int(root.RootWidget.angles[i]))
                except:
                    pass
