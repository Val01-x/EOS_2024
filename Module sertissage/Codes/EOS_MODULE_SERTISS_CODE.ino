//LIBRAIRIES

#include "Servo.h"
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>


//OLED DISPLAY SIZE

#define SCREEN_WIDTH 128 
#define SCREEN_HEIGHT 64 


// Declaration for an SSD1306 display connected to I2C (SDA, SCL pins)
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);


//RELAY PIN
const int digPin = 2;


//INITIAL CLOSING DURATION

int duration = 30;


//SERVOS PIN

Servo servod; 
Servo servog; 


void setup() {
 	
 	Serial.begin(9600);
 	Serial.println(F("Initialize System"));
 	

  //PIN MODE

 	pinMode(digPin, OUTPUT);
  pinMode(3, INPUT);
  pinMode(4, INPUT);
  pinMode(5, INPUT);

  
  //WE OPEN THE REALY - HEATING WIRE

  digitalWrite(digPin, HIGH);


  //WE OPEN THE HATCH
  servod.attach(7);
  servog.attach(8);
  servod.write(80); 
  servog.write(90); 
  
  delay(1000);

  servod.detach(); 
  servog.detach(); 


  //WE INITIALIZE THE OLED DISPLAY

  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) { // Address 0x3D for 128x64
    Serial.println(F("SSD1306 allocation failed"));
    for(;;);
  }
  delay(2000);
  display.clearDisplay();
  display.clearDisplay();
  display.setTextSize(4);
  display.setTextColor(WHITE);
  display.setCursor(0, 10);
  // Display static text
  display.println(duration);
  display.display();
  
}



void loop() {

  
  //WE READ THE STATE OF THE BUTTONS

  byte buttonStateSignal = digitalRead(4);
  byte buttonStateMinus = digitalRead(12);
  byte buttonStatePlus = digitalRead(11);

   
  //IF THE MINUS BUTTON IS PRESSED WE DECREASE THE DURATION
  //IF THE PLUS BUTTON IS PRESSED WE INCREASE THE DURATION
  //STEP = 1 SEC

  if (buttonStateMinus == LOW) {
    duration -= 1;
    display.clearDisplay();
    display.setTextSize(4);
    display.setTextColor(WHITE);
    display.setCursor(0, 10);
    // Display static text
    display.println(duration);
    display.display();
  }
  if (buttonStatePlus == LOW) {
    duration += 1;
    display.clearDisplay();
    display.setTextSize(4);
    display.setTextColor(WHITE);
    display.setCursor(0, 10);
    // Display static text
    display.println(duration);
    display.display();
  }
  

  //IF THE START BUTTON IS PRESSED WE CLOSE THE HATCH AND START SEALING THE BAG FOR THE ENTERED DURATION

  if (buttonStateSignal == LOW) {
      servod.attach(7);
      servog.attach(8);
      servod.write(170); 
      servog.write(0); 
      delay(1000);
      servod.detach(); 
      servog.detach(); 
      delay(duration*1000-2000);
      servod.attach(7);
      servog.attach(8);
      servod.write(80); 
      servog.write(90); 
      delay(1000);
      servod.detach(); 
      servog.detach(); 
  }
  
  delay(100);
  
}




