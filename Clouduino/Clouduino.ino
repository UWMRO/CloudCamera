#include <Wire.h>
#include <OneWire.h>
#include <DallasTemperature.h>
#include <Servo.h>
#include <Digital_Light_TSL2561.h>
#include "DHT.h"

#define DHTTYPE DHT22 
#define DHTPIN A0
DHT dht(DHTPIN, DHTTYPE);

int servoPin = 9;       // light servo connected to pin 9
int heatPin = 13;      // Heater connected to digital pin 13
int dsPin = 10;
int pos = 0;

#define ONE_WIRE_BUS dsPin
OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);
OneWire  ds(dsPin);

Servo myservo;

DeviceAddress therm1 = { 0x28, 0xCC, 0x44, 0x5D, 0x06, 0x00, 0x00, 0x9E };

void setup(void) {
  Serial.begin(9600);
  myservo.attach(servoPin);  // attaches the servo on pin 9 to the servo object
  TSL2561.init();            // light Sensor
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
      if (pos != 115){
      for (pos = 45; pos <= 115; pos += 1) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(300);                       // waits 15ms for the servo to reach the position
      }
      pos = 115;
    }
}

void setFilterOut(){
   if (pos != 45){
      for (pos = 115; pos >= 45; pos -= 1) { // goes from 180 degrees to 0 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(300);                       // waits 15ms for the servo to reach the position
      }
     pos = 45;
   }
 }

void getDomeMet(){
     float h = dht.readHumidity();
    float t = dht.readTemperature();

    // check if returns are valid, if they are NaN (not a number) then something went wrong!
    if (isnan(t) || isnan(h)) 
    {
        Serial.println("Failed to read from DHT");
    } 
    else 
    {
        Serial.print(h);
        Serial.print(","); 
        Serial.println(t);
    }
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
        }
    }
}
