#include <Wire.h>
#include <OneWire.h>
#include <Servo.h>

// #define DHTPIN A0
// #define DHTTYPE DHT22
// DHT dht(DHTPIN, DHTTYPE);

int servoPin = 9;       // light servo connected to pin 9
int heatPin = 12;      // Heater connected to digital pin 12
int rainPin1 = 10;       // Rain sensor 2 to digital pin 11
int rainPin2 = 11;       // Rain sensor 1 to digital pin 10
int pos = 0;
int inPos = 90;
int outPos = 45;
int servoDelay = 10;

Servo myservo;


void setup(void) {
  Serial.begin(9600);
  //myservo.attach(servoPin);  // attaches the servo on pin 9 to the servo object
  pinMode(rainPin1, INPUT_PULLUP);
  pinMode(rainPin2, INPUT_PULLUP);
  Serial.println("Pins attached");


}

void checkRainSensor1(){
      int status = digitalRead(rainPin1);
      Serial.println(status);
      if (status == 0){
        Serial.println("rain1 = True");
        }
      else{
        Serial.println("rain1 = False");
        }
      return;
}

void checkRainSensor2(){
      int status = digitalRead(rainPin2);
      Serial.println(status);
      if (status == 0){
        Serial.println("rain2 = True");
        }
      else{
        Serial.println("rain2 = False");
        }
      return;
}

void setFilterIn(){
      if (pos != inPos){
        myservo.attach(servoPin);     // attach to the servo
        delay(1000);      // wait for the servo to attach
        for (pos = outPos; pos <= inPos; pos += 1) { // goes from 0 degrees to 180 degrees
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(servoDelay);                       // waits 15ms for the servo to reach the position
        }
        delay(1500);
        pos = inPos;
    }
    myservo.detach();     // detach from the servo
    return;
}

void setFilterOut(){
   if (pos != outPos){
      myservo.attach(servoPin);     // attach to the servo
      delay(1000);      // wait for the servo to attach
      for (pos = inPos; pos >= outPos; pos -= 1) { // goes from 180 degrees to 0 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(servoDelay);                       // waits 15ms for the servo to reach the position
      }
      delay(1500);
      pos = outPos;
   }
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
      case 'r':
         checkRainSensor1();
         break;
      case 't':
         checkRainSensor2();
         break;
        }
    }
}
