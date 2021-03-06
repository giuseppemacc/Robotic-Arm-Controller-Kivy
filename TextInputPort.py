from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

# import di Serial
import Serial as ser

class TextInputPort(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # textInput è un TextInput
        self.textInput = TextInput()
        self.textInput.multiline = False
        self.textInput.on_text_validate = self.on_enter

        # aggiunte grafiche
        self.text = Label(text="Porta")
        self.add_widget(self.text)
        self.add_widget(self.textInput)
        self.state_ser = Label()
        self.add_widget(self.state_ser)
        Clock.schedule_interval(self.refresh_state_ser,1/60)

    def on_enter(self):
        ser.Serial.port = self.textInput.text
        ser.Serial().open_communication()
    
    def refresh_state_ser(self,dt):
        self.textInput.font_size = self.textInput.height/2
        if ser.Serial.ser_open:
            self.state_ser.text = "Connected"
        else:
            self.state_ser.text = "Disconnected"