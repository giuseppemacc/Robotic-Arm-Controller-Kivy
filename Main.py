import kivy
from kivy.config import Config
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
Config.set('graphics', 'width',  1000)
Config.set('graphics', 'height', 800)


from kivy.app import App
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.graphics import Color
from kivy.graphics import Rectangle
from kivy.graphics.opengl import *
from obj3D import Object3D
from all_Object import Dic_All_Obj
import time
import serial 

kivy.require('1.9.0')


master = True
ser_open = False
ser = serial.Serial()
#port = 'COM3'#input("Inserisci la porta seriale> ")
ser.port = ''
ser.baudrate = 9600
ser.timeout = 1
#provo ad aprire e metto ser_open a true altrimenti ser_open a false
try:
    ser.open()
except:
    ser_open = False

all_obj = Dic_All_Obj("modello3d.obj")   

angles = { "S_BASE":0,  
          "S_NODO1":0, 
          "S_NODO2":0, 
          "S_NODO3":0, 
          "S_PINZA_BASE":0, 
          "S_PINZA":0} 
counter = 0
all_rot_angle = 0
all_rot_speed = 0

class All_Obj(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.Base = all_obj.get("Base")
        self.S_Base = all_obj.get("S_Base") 
        self.S_Nodo1 = all_obj.get("S_Nodo1") 
        self.Braccio1 = all_obj.get("Braccio1") 
        self.S_Nodo2 = all_obj.get("S_Nodo2") 
        self.Braccio2 = all_obj.get("Braccio2") 
        self.S_Nodo3 = all_obj.get("S_Nodo3") 
        self.S_Pinza_Base = all_obj.get("S_Pinza_Base")
        self.S_Pinza = all_obj.get("S_Pinza")
        self.Pinza_1 = all_obj.get("Pinza_1")
        self.Pinza_2 = all_obj.get("Pinza_2")
        
        self.add_widget(self.Base)
        self.add_widget(self.S_Base)
        self.add_widget(self.S_Nodo1)
        self.add_widget(self.Braccio1)
        self.add_widget(self.S_Nodo2)
        self.add_widget(self.Braccio2)
        self.add_widget(self.S_Nodo3)
        self.add_widget(self.S_Pinza_Base)
        self.add_widget(self.S_Pinza)
        self.add_widget(self.Pinza_1)
        self.add_widget(self.Pinza_2)
        self.rot = 0
        self.size_context = [0,0]
        
        Clock.schedule_interval(self.rotate, 1 / 60)
        Clock.schedule_interval(self.rotate_all, 1 / 60)
        Clock.schedule_interval(self.update_size_context, 1 / 60)
        Clock.schedule_interval(self.translate_all, 1/60)
        
    def translate_all(self,dt):
        tras = self.size_context[0]/1000-0.5
        self.Base.tras.x = tras
        self.S_Base.tras.x = tras 
        self.S_Nodo1.tras.x = tras 
        self.Braccio1.tras.x = tras 
        self.S_Nodo2.tras.x = tras 
        self.Braccio2.tras.x = tras 
        self.S_Nodo3.tras.x = tras 
        self.S_Pinza_Base.tras.x = tras 
        self.S_Pinza.tras.x = tras 
        self.Pinza_1.tras.x = tras 
        self.Pinza_2.tras.x = tras 
    
    def update_size_context(self,dt):
        for key in all_obj.keys():
            all_obj[key].size_context = self.size_context
        
    def rotate_all(self,dt):    
        self.rot += all_rot_speed
    
    def rotate(self,dt):
        self.R_S_Base(self.Base)
        self.R_S_Base(self.S_Base)
        self.R_S_Nodo1(self.S_Nodo1)
        self.R_Braccio1(self.Braccio1)
        self.R_S_Nodo2(self.S_Nodo2)
        self.R_Braccio2(self.Braccio2)
        self.R_S_Nodo3(self.S_Nodo3)
        self.R_S_Pinza_Base(self.S_Pinza_Base)
        self.R_S_Pinza(self.S_Pinza)
        self.R_Pinza(self.Pinza_1,self.Pinza_2)

    def R_S_Base(self,obj):
        obj.rot.axis = (0,1,0)
        obj.rot.origin = (0,0,0)
        obj.rot.angle = self.rot + all_rot_angle
        
    def R_S_Nodo1(self,obj):
        self.R_S_Base(obj)
        
        obj.rot1.axis = (0,1,0)
        obj.rot1.origin = (0,0,0)
        obj.rot1.angle = angles.get("S_BASE")-180
    
    def R_Braccio1(self,obj):
        
        self.R_S_Nodo1(obj)
        
        obj.rot2.axis = (1,0,0)
        obj.rot2.origin = tuple(self.S_Nodo1.Punto_Medio())
        obj.rot2.angle = angles.get("S_NODO1")-90
    
    def R_S_Nodo2(self,obj):
        
        self.R_Braccio1(obj)
        
    def R_Braccio2(self,obj):
        
        self.R_S_Nodo2(obj)
        
        obj.rot3.axis = (1,0,0)
        obj.rot3.origin = tuple(self.S_Nodo2.Punto_Medio())
        obj.rot3.angle = angles.get("S_NODO2")-90  
        
    def R_S_Nodo3(self,obj):
        
        self.R_Braccio2(obj)
        
    def R_S_Pinza_Base(self,obj):
        
        self.R_S_Nodo3(obj)
        
        obj.rot4.axis = (1,0,0)
        obj.rot4.origin = tuple(self.S_Nodo3.Punto_Medio())
        obj.rot4.angle = angles.get("S_NODO3")-90
        
    def R_S_Pinza(self,obj):
        
        self.R_S_Pinza_Base(obj)
        
        obj.rot5.axis = (0,1,0)
        obj.rot5.origin = tuple(self.S_Pinza_Base.Punto_Medio())
        obj.rot5.angle = angles.get("S_PINZA_BASE")-180
        
    def R_Pinza(self,obj1,obj2):
        
        self.R_S_Pinza(obj1)
        self.R_S_Pinza(obj2)
        
        obj1.rot6.axis = (1,0,0)
        obj1.rot6.origin = tuple(self.S_Pinza.Punto_Medio())
        obj1.rot6.angle = angles.get("S_PINZA")  
        
        obj2.rot6.axis = (1,0,0)
        obj2.rot6.origin = tuple(self.S_Pinza.Punto_Medio())
        obj2.rot6.angle = -angles.get("S_PINZA") 

class Slide_angles(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursor_image = 'slide.png'
        self.min = 0
        self.max = 180
        self.value = 90
        Clock.schedule_interval(self.get_value, 1/60)
    def get_value(self,dt):
        global angles
        global counter 
        keys = [*angles.keys()]
        if(master == True):
            angles[keys[counter]]=self.value
        else:
            self.value = angles[keys[counter]]
        counter+=1
        if(counter == 6):
            counter = 0 
             
class RootWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.counter = 0
        self.objs = All_Obj()
        #self.objs.size_hint = [.5,1] 
        self.add_widget(self.objs)
        Clock.schedule_interval(self.set_angles, 10/1000 )#30 #10
        Clock.schedule_interval(self.send_master, 100/1000 )#20 #100
        #Clock.schedule_interval(self.change_master,  5)
        Clock.schedule_interval(self.write_angles, 1)
        Clock.schedule_interval(self.print_size,1/60)
        
    
    def print_size(self,dt):
        self.objs.size_context = self.size
        #print(self.objs.size)
    #scrivi angles in un file ogni 1 secondo  
    def write_angles(self,dt):
        with open("angles.txt",'w') as file:
            for d in angles.items():
                file.write(
                    d[0]+" > "+str(d[1])+"\n"
                )    
    
    #cambia il valore di master ogni 10 secondi
    def change_master(self,dt): 
        if ser_open == True:
            global master
            master = not master
            #ser.close()
            #ser.open()
    
    #invia il valore di master ad arduino nel formato b'0'/b'1' ogni 1/60 secondi
    def send_master(self,dt):
        if ser_open == True:
            value_m = None

            if master == True:
                value_m = b'T'
            else:
                value_m = b'F'

            ser.write(value_m)
                
    #setta il valore di angles in base a master ogni 0.000001 secondi
    def set_angles(self,dt):
        if ser_open == True:
            #master == False riceve i valori da arduino e modifica angles
            if master == False:
                global angles
                read = []
                name = ""
                value = 0
                try:
                    read = (str(ser.readline())[2:-5]).split(">")
                    try:
                        name = (read[0]).upper()
                        try:
                            value = float(read[1])
                            if(name in angles.keys()):
                                angles[name] = value
                            else:
                                print("ERRORE|Key not found")
                        except:
                            print("ERRORE|Unable to get value")
                    except:
                        print("ERRORE|Unable to get name")
                except:
                    print("ERRORE|Invalid value") 

            #master == True invia i valori da arduino 
            elif master == True:
                value = str(int([*(angles.values())][self.counter]))
                if len(value) == 3:
                    pass
                elif len(value) == 2:
                    value = value + "?"
                elif len(value) == 1:
                    value = value +"??"
                send = ('|'+str(self.counter)+'>'+value).encode()
                ser.write(send)    
                self.counter+=1
                if(self.counter==6):
                    self.counter = 0         
   
class Slide_speed(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cursor_image = 'slide.png'
        Clock.schedule_interval(self.set_speed, 1/60)
        
    def set_speed(self,dt):
        global all_rot_speed
        all_rot_speed = self.value
        
class Slide_rotate(Slider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self.value_track= True
        #self.value_track_color = [1,0,0,1]
        #self.value_track_width = 1
        self.cursor_image = 'slide.png'
        
        Clock.schedule_interval(self.set_rotate, 1/60)
        
    def set_rotate(self,dt):
        global all_rot_angle
        all_rot_angle = self.value

class TextInputPort(TextInput):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.multiline = False
        #questo valore deve essere messo in port 
        # e deve essere visualizzato in texinput
    def on_text_validate(self): 
        global ser
        global ser_open
        #provo a modificare la porta e se si apre setto ser_open a true altrimenti ser_open a false 
        try:
            ser.port = self.text
            ser.open()
            ser_open = True
            print("OK")
        except:
            ser_open = False
        
class LabelPort(Label):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.refresh,1)   
        
    def refresh(self,dt):
        if ser_open == True:
            self.text = 'ON '
        else:
            self.text = 'OFF'
        
class CheckBoxMaster(CheckBox):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.active = True
        Clock.schedule_interval(self.refresh,1/60)
    def refresh(self,dt):
        global master
        if self.active == True:
            master = True
        else:
            master = False
    def on_release(self):
        if ser_open == True:
            ser.close()
            ser.open()
        
                
class App3D(App):
    def build(self):
        return RootWindow()
    
if __name__ == "__main__":
    App3D().run() 