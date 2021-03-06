from kivy.app import App
from kivy.config import Config
# disabilitazione del multitouch
Config.set('input', 'mouse', 'mouse,multitouch_on_demand')
# impostazione width e height della finestra
Config.set('graphics', 'width',  800)
Config.set('graphics', 'height', 800)


""" ---import del root widget --- """
from RootWidget import RootWidget

# Classe root principale
class rootWidget(RootWidget):
    pass

class mainApp(App):
    def build(self):
        return rootWidget()

if __name__ == "__main__":
    mainApp().run()