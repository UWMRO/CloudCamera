#include <Wire.h>
#include <OneWire.h>
#include <Servo.h>


int servoPin = 9;       // light servo connected to pin 9
int heatPin = 13;      // Heater connected to digital pin 13
int dsPin = 10;
int pos = 0;
int inPos = 80;
int outPos = 42;
int servoDelay = 10;

#define ONE_WIRE_BUS dsPin
OneWire oneWire(ONE_WIRE_BUS);
OneWire  ds(dsPin);

Servo myservo;


void setup(void) {
  Serial.begin(9600);
  //myservo.attach(servoPin);  // attaches the servo on pin 9 to the servo object
  Serial.println("past here");

}

void setFilterIn(){
      if (pos != inPos){
        myservo.attach(servoPin);     // attach to the servo
        delay(1000);      // wait for the servo to attach
        myservo.write(inPos);              // tell servo to go to position in variable 'pos'
        delay(servoDelay);                       // waits 15ms for the servo to reach the position
        }  
        delay(1500);
        pos = inPos;
    myservo.detach();     // detach from the servo
    return;
}

void setFilterOut(){
   if (pos != outPos){
      myservo.attach(servoPin);     // attach to the servo
      delay(1000);      // wait for the servo to attach
      myservo.write(outPos);              // tell servo to go to position in variable 'pos'
      delay(servoDelay);                       // waits 15ms for the servo to reach the position
      }
      delay(1500);
      pos = outPos;
   myservo.detach();       // detach from the servo
   return;
 }

void test(void){
  Serial.println("test routine");
}

void loop(void) {
  if (Serial.available() > 0) {
    int inByte = Serial.read();
    switch (inByte) {
      case 'i':
        setFilterIn();
        break;
      case 'o':
        setFilterOut();
        break;
      case 'y':
         test();
         break;
        }
    }
}
