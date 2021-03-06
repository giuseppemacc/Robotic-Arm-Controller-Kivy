""" --- import di serial e kivy.clock --- """
import serial
from serial.tools.list_ports import comports
from kivy.clock import Clock

""" --- Classe principale Serial --- """

class Serial():
    """
    Specifiche:
        deve istanziare una comunicazione seriale
        bisogna poter modificare e aggiornare i suoi parametri 
        voglio che quando cambia la porta si aggiorni tutto
    """

    port = ""
    ser_open = False
    master = False
    angles = []
    # ser e i suoi attributi
    ser = serial.Serial()
    ser.baudrate = 9600
    ser.timeout = 1


    """ --- metodi --- """
    # visualizza lo stato della comunicazione
    def print_state(self):
        print("Comunicazione sulla porta: ",Serial.port,"  stato:",Serial.ser_open)

    # imposta self.port tramite un parametro
    def set_port(self,port):
        Serial.port = port
    
    # prova ad aprire la comunicazione impostando ser.port come self.port e modifica ser_open
    def open_communication(self):
        print("--- Apertura comunicazione sulla porta: ",Serial.ser.port," ---")
        try:
            Serial.ser.port = Serial.port
            Serial.ser.open()
            Serial.ser_open = True
            print("Comunicazione aperta")
        except Exception:
            print("Impossibile aprire la comunicazione") 
            Serial.ser_open = False
            Serial.ser.close()


       


    