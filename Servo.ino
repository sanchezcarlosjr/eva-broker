#include <ax12.h>

int engine1 = 512;
int engine2 = 512;

//Declaramos la variable
char dato;
int angulo = 90;

void setup() {
  Serial.begin(9600);
  SetPosition(1, engine1);
  SetPosition(2, engine2);
}

void loop() {
  while(Serial.available()){
    dato = Serial.read();
    delay(10);
    Serial.println(dato);
    switch(dato){
      case 'd':
      //Gira servo hacia la derecha
      angulo = angulo + 2;
      SetPosition(engine1, angulo);
      break;
      
      case 'i':
      //Gira servo hacia la izquierda
      angulo = angulo - 2;
      SetPosition(engine1, angulo);
      break;
      
      case 'p':
      //Parar el servo
      angulo = angulo;
      SetPosition(engine1, angulo);
      break;
      }
   }
 }
