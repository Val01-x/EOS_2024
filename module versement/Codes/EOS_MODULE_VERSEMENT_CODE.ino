//
//    FILE: EOS_MODULE_VERSEMENT_CODE
// PURPOSE: Versement de 100g
// Utilisation: Connecter la piéce sur un ordinateur et appuyer sur entré
//              dans le serial monitor pour demander 100g 

//---------------------------------------Begin Initialisation scale
#include "HX711.h"
HX711 scale1;
HX711 scale2;

//scale 3
uint8_t dataPin1 = 3;
uint8_t clockPin1 = 2;

//scale 4
uint8_t dataPin2 = 8;
uint8_t clockPin2 = 7;

float weight_before_opening;
float weight_after_opening;
//---------------------------------------End Initialisation scale

//---------------------------------------Begin Initialisation servo
#include <Servo.h>

Servo myservo;

int Open_servo = 90;
int Close_servo = 0;

//---------------------------------------End Initialisation scale

//---------------------------------------Begin Recever
int portion=100;
//---------------------------------------End Recever

//---------------------------------------Begin Initialisation

void setup() {
  //---------------------------------------Begin Setup Recever
  Serial.begin(9600);
  //---------------------------------------Begin Setup Recever
  
  //---------------------------------------Begin Setup servo
  myservo.attach(9);
  myservo.write(Close_servo);
  delay(5000);
  myservo.detach();
  //---------------------------------------End Setup servo

  //---------------------------------------Begin Setup scale
  scale1.begin(dataPin1, clockPin1);
  scale2.begin(dataPin2, clockPin2);

  scale1.set_offset(4294538449);
  scale1.set_scale(1029.004028);

  scale2.set_offset(4294924964);
  scale2.set_scale(1090.996459);
  //---------------------------------------End Setup servo
}


void loop() {
  //---------------------------------------Begin Loop receiver/ Waiting Sequence
  while (Serial.available()) Serial.read();
  Serial.println("do you want a portion?");
  while (Serial.available() == 0);
  //---------------------------------------End Loop receiver/ Waiting Sequence

  //---------------------------------------Begin Dosing sequence
  weight_before_opening = scale1.get_units() + scale2.get_units();
  weight_after_opening = scale1.get_units() + scale2.get_units();
  Serial.print("Before: ");
  Serial.println(scale1.get_units() + scale2.get_units());
  myservo.attach(9);
  myservo.write(Open_servo);
  while (weight_after_opening > weight_before_opening - portion + 50) {
    weight_after_opening = scale1.get_units() + scale2.get_units();
  }
  myservo.write(60);
  while (weight_after_opening > weight_before_opening - portion + 7) {
    weight_after_opening = scale1.get_units() + scale2.get_units();
  }
  myservo.write(Close_servo);
  delay(1000);
  myservo.detach();
  weight_after_opening = scale1.get_units() + scale2.get_units();
  Serial.print("delta: ");
  Serial.println(weight_before_opening - weight_after_opening);
  //---------------------------------------End Dosing sequence
}


// -- END OF FILE --
