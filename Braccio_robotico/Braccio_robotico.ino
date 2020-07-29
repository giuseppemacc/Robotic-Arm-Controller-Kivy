#include <Servo.h>

float angles[6] = {0,0,0,0,0,0};
bool master = true;

Servo S_Base;
Servo S_Nodo1;
Servo S_Nodo2;
Servo S_Nodo3; 
Servo S_Pinza_Base;
Servo S_Pinza;

const int p1=A0;
const int p2=A1;
const int p3=A2;
const int p4=A3;
const int p5=A4;
const int p6=A5;

const int pot_pins[] = {p1,p2,p3,p4,p5,p6};

const String index_names[6] = {   
  "S_Base",
  "S_Nodo1",
  "S_Nodo2",
  "S_Nodo3",
  "S_Pinza_Base",
  "S_Pinza",
};



void setup() {
  S_Base.attach(12);  
  S_Nodo1.attach(11);
  S_Nodo2.attach(10);
  S_Nodo3.attach(9);
  S_Pinza_Base.attach(8);
  S_Pinza.attach(7);
  
  pinMode(p1,INPUT);
  pinMode(p2,INPUT);
  pinMode(p3,INPUT);
  pinMode(p4,INPUT);
  pinMode(p5,INPUT);
  pinMode(p6,INPUT);
  pinMode(13,OUTPUT);
  Serial.begin(9600);
}

void set_master(int start_byte){ 
    // il programma invia master ogni 100ms
    int r = start_byte;
    if(r=='F'){
      master = true;
    }else if(r=='T'){
      master = false;
    }

    if(master==true){
      digitalWrite(13,1);
    }else if(master == false){
      digitalWrite(13,0);
    }
}

int nnn(int n1, int n2, int n3){
    if(n1 != '?' && n2 != '?' && n3 != '?'){
        n1-=48;
        n2-=48;
        n3-=48;
        return (n1*100 + n2*10 + n3*1);
    }else if(n1 != '?' && n2 != '?' && n3 == '?'){
        n1-=48;
        n2-=48;
        return (n1*10 + n2*1); 
    }else if(n1 != '?' && n2 == '?' && n3 == '?'){
        n1-=48;
        return (n1);
    }
}

void set_angles(int start_byte){
  //il delay di chi inivia deve essere maggiore di chi riceve
  // i valori dal programma vengono inviati e ricevuti con un delay di 10ms
  int value;
  
  if(master == false){
    bool disponibile = Serial.available()>0;
    int index,n1,n2,n3;
    
    delay(5);
    
    if(disponibile && start_byte=='|'){
        
      if(disponibile){
        index = Serial.read();

        if(disponibile && Serial.read()=='>'){

          if(disponibile){
            n1 = Serial.read();

            if(disponibile){
              n2 = Serial.read();

              if(disponibile){
                n3 = Serial.read();

                index -= 48;

                value = nnn(n1,n2,n3);
                
                angles[index] = value;

              }
            }
          }
        }
      }
    }
  }else if(master == true){
    for(int i = 0; i < 6; i++){
      value = map(analogRead(pot_pins[i]), 0,1023, 0,180);
      angles[i] = value;
      Serial.println(index_names[i]+">"+value);
      delay(15);
    }
  }  
} 

void set_servo(){
  S_Base.write( angles[0] );

  S_Nodo1.write( angles[1] );
  
  S_Nodo2.write( angles[2] ); 
  
  S_Nodo3.write( angles[3] );

  S_Pinza_Base.write( angles[4] );

  S_Pinza.write( angles[5] );  
}

void loop() {
  int primo_valore = Serial.read(); /* legge il primo byte disponibile e lo invia come parametro a set_angles e set_master */

  set_master(primo_valore);  /* legge il valore corrente nel buffer seriale e se legge 'T' imposta master su false altrimenti se trova 'F' imposta master su true. */
  
  set_angles(primo_valore);  /* modifica il valore di angles in base ai due stati di master:
                     ► master == true:  invia valori e indici di angles al programma nel formato index_name>value
                       index_name corrisponde al nome del servomotore.                             
                     ► master == false: riceve un buffer seriale dal programma nel formato |index>value 
                       value viene inviato nel formato n1n2n3 in cui n indica le cifre del numero che se non esistono vengono sostituite con un '?' ( es. |1>90? ). */                           
                                                
  set_servo();   /* imposta il grado di rotazione di ogni servo a cui è associato un indice ed un valore in angles. */
  
}
