#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Servo.h>
#include <Digital_Light_TSL2561.h>
#include "DHT.h"


#define DHTPIN A0
#define DHTTYPE DHT22 
DHT dht(DHTPIN, DHTTYPE);

int servoPin = 9;       // light servo connected to pin 9
int heatPin = 13;      // Heater connected to digital pin 13
int dsPin = 10;
int pos = 0;
int inPos = 90;
int outPos = 45;
int servoDelay = 2;

#define ONE_WIRE_BUS dsPin
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
OneWire  ds(dsPin);

Servo myservo;

DeviceAddress therm1 = { 0x28, 0xCC, 0x44, 0x5D, 0x06, 0x00, 0x00, 0x9E };

void setup(void) {
  Serial.begin(9600);
  myservo.attach(servoPin);  // attaches the servo on pin 9 to the servo object
  Wire.begin();
  TSL2561.init();            // light Sensor
  Serial.println("past here");
  sensors.begin();              // start one wire devices 
  dht.begin();
  pinMode(heatPin, OUTPUT);      // sets the digital pin as output

}

void findTempAddr(){
  byte i;
  byte present = 0;
  byte type_s;
  byte data[12];
  byte addr[8];
  
  if ( !ds.search(addr)) 
  {
    Serial.println("No more addresses.");
    Serial.println();
    ds.reset_search();
    delay(250);
    return;
  }
  
  Serial.print("ROM =");
  for( i = 0; i < 8; i++) 
  {
    Serial.write(' ');
    Serial.print(addr[i], HEX);
  }

  if (OneWire::crc8(addr, 7) != addr[7]) 
  {
      Serial.println("CRC is not valid!");
      return;
  }
  Serial.println();
}

void getTemp(DeviceAddress deviceAddress){
  float tempC = sensors.getTempC(deviceAddress);
  if (tempC == -127.00) {
    Serial.print("Error getting temperature");
  } else {
    Serial.print(tempC);
  }
}

void setHeaterOn(){
  return;  
}

void setHeaterOff(){
  return;
}

void getHeaterState(){
  return;
}

void getLux(){
  Serial.println(TSL2561.readVisibleLux());
  return;  
}

void setFilterIn(){
      if (pos != inPos){
      for (pos = outPos; pos <= inPos; pos += 1) { // goes from 0 degrees to 180 degrees
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(servoDelay);                       // waits 15ms for the servo to reach the position
      }
      pos = inPos;
    }
    return;
}

void setFilterOut(){
   if (pos != outPos){
      for (pos = inPos; pos >= outPos; pos -= 1) { // goes from 180 degrees to 0 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(servoDelay);                       // waits 15ms for the servo to reach the position
      }
     pos = outPos;
   }
   return;
 }

void getDomeMet(){
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    Serial.print(h);
    Serial.print(","); 
    Serial.println(t);
}

void test(void){
  Serial.println("test routine");
}

void loop(void) {
  if (Serial.available() > 0) {
    int inByte = Serial.read();
    switch (inByte) {
      case 'f':
        findTempAddr();
        break;
      case 't':
        getTemp(therm1);
        break;
      case 'l':
        getLux();
        break;
      case 'i':
        setFilterIn();
        break;
      case 'o':
        setFilterOut();
        break;
      case 'd':
        getDomeMet();
        break;
      case 'y':
         test();
         break;
        }
    }
}
