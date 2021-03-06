from kivy.uix.boxlayout import BoxLayout
from kivy.uix.checkbox import CheckBox
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.uix.textinput import TextInput

# import del RootWidget
import RootWidget as root

class MasterChecker(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # master_check è il checkerBox tramite il quale si potrà modificare root.RootWidget.master
        self.master_check = CheckBox()

        # aggiunte grafiche
        self.text = Label(text="Master")
        self.add_widget(self.text)
        self.add_widget(self.master_check)

        # default attivo
        self.master_check.active = False


        Clock.schedule_interval(self.set_master_state,1/60)


    def set_master_state(self,dt):
        root.RootWidget.master = self.master_check.active



    



