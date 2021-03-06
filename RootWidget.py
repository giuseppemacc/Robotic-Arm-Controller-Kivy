from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider


""" --- import da altri file --- """
from Serial import Serial 
from glContext.glContext import glContext
from SliderAngles import SliderAnglesBox
from MasterChecker import MasterChecker
from TextInputPort import TextInputPort


class RootWidget(BoxLayout):
    # master determina il tipo di controllo di angles
    master = False
    # angles è la lista che contiene i valori degli angoli di rotazione
    angles = [] 
    # axis contiene gli assi di rotazione con nome e intervallo di valori
    axis = [
        ["Axis 1",[0,360]],
        ["Axis 2",[0,180]],
        ["Axis 3",[0,180]],
        ["Axis 4",[0,180]],
        ["Axis 5",[0,180]]
    ]
    # valore default angles
    for _ in range(len(axis)):
        angles.append(0)


    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'horizontal'

        # box dei widgets
        self.widget_box = BoxLayout()

        # self.serial è l'instanza principale di serial cui dovranno essere modificati gli attributi come port master angles
        self.serial = Serial() 

        # contesto gl
        self.gl = glContext()

        # sliderBox è il widget contenente gli sliderAngles e i Label corrispondenti
        self.sliderBox = SliderAnglesBox(axis=RootWidget.axis)

        # master_cheker è il widget contenente delle checkerBox che permette di modificare master
        self.master_cheker = MasterChecker()   

        # textInputPort è il text input dal quale viene modificata la porta in serial
        self.textInputPort = TextInputPort()

        # size dei widget         
        self.textInputPort.size_hint = [1,.05]
        self.master_cheker.size_hint = [1,.05]
        self.sliderBox.size_hint =     [1,.9 ]

        # aggiunta dei widget a widget_box
        self.widget_box.orientation = 'vertical'
        self.widget_box.add_widget(self.textInputPort)
        self.widget_box.add_widget(self.master_cheker)
        self.widget_box.add_widget(self.sliderBox)

        # size di widget_box e gl
        self.widget_box.size_hint = [.3,1]
        self.gl.size_hint = [.7,1]

        # aggiunta di widget_box e gl al BoxLayout
        self.add_widget(self.widget_box)
        self.add_widget(self.gl)


        Clock.schedule_interval(self.print_var_state,1)

    # visualizza lo stato delle variabili angles e master
    def print_var_state(self,dt):
        print("Angles> ",RootWidget.angles)
        print("----")
        print("Master> ",RootWidget.master)
        print("----")
        self.serial.print_state()
        

