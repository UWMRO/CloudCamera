#include <OneWire.h>
#include <DallasTemperature.h>

// Data wire is plugged into pin 10 on the Arduino
#define ONE_WIRE_BUS 9

// Setup a oneWire instance to communicate with any OneWire devices
OneWire oneWire(ONE_WIRE_BUS);

// Pass our oneWire reference to Dallas Temperature. 
DallasTemperature sensors(&oneWire);

DeviceAddress therm1 = { 0x28, 0x49, 0xFD, 0x5C, 0x06, 0x00, 0x00, 0xAC };
DeviceAddress therm2 = { 0x28, 0xC6, 0x9D, 0x5C, 0x06, 0x00, 0x00, 0x73 };

void setup(void)
{
  // start serial port
  Serial.begin(9600);
  // Start up the library
  sensors.begin();
  // set the resolution to 10 bit (good enough?)
  sensors.setResolution(therm1, 12);
  sensors.setResolution(therm2, 12);
}

void printTemperature(DeviceAddress deviceAddress)
{
  float tempC = sensors.getTempC(deviceAddress);
  if (tempC == -127.00) {
    Serial.print("Error getting temperature");
  } else {
    Serial.print(tempC);
    //Serial.print(" F: ");
    //Serial.print(DallasTemperature::toFahrenheit(tempC));
  }
}

void loop(void)
{ 
  if (Serial.available() >0){
     int inByte= Serial.read();

  switch (inByte){
    case 's':
      sensors.requestTemperatures();
  
      printTemperature(therm1);
      Serial.print(";");
      printTemperature(therm2);
      Serial.println();
      
  }
  }
}

