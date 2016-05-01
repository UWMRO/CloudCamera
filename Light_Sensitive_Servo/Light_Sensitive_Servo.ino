/* Sweep
 by BARRAGAN <http://barraganstudio.com>
 This example code is in the public domain.

 modified 8 Nov 2013
 by Scott Fitzgerald
 http://www.arduino.cc/en/Tutorial/Sweep
*/

#include <Servo.h>

Servo myservo;  // create servo object to control a servo
// twelve servo objects can be created on most boards

int pos = 0;    // variable to store the servo position


#include "DHT.h"

#define DHTPIN A0     // what pin we're connected to

// Uncomment whatever type you're using!
//#define DHTTYPE DHT11   // DHT 11 
#define DHTTYPE DHT22   // DHT 22  (AM2302)
//#define DHTTYPE DHT21   // DHT 21 (AM2301)

// Connect pin 1 (on the left) of the sensor to +5V
// Connect pin 2 of the sensor to whatever your DHTPIN is
// Connect pin 4 (on the right) of the sensor to GROUND
// Connect a 10K resistor from pin 2 (data) to pin 1 (power) of the sensor

DHT dht(DHTPIN, DHTTYPE);

#include <Wire.h>
#include <Digital_Light_TSL2561.h>

void setup() {
  myservo.attach(9);  // attaches the servo on pin 9 to the servo object
 
  Wire.begin();
  Serial.begin(9600);
  TSL2561.init();

  Serial.begin(2400); 
  Serial.println("DHTxx test!");

  dht.begin();

  ( pos = 0 );
}

void loop() {

   // Reading temperature or humidity takes about 250 milliseconds!
    // Sensor readings may also be up to 2 seconds 'old' (its a very slow sensor)
    float h = dht.readHumidity();
    float t = dht.readTemperature();

    // check if returns are valid, if they are NaN (not a number) then something went wrong!
    if (isnan(t) || isnan(h)) 
    {
        Serial.println("Failed to read from DHT");
    } 
    else 
    {
        Serial.print("Humidity: "); 
        Serial.print(h);
        Serial.print(" %\t");
        Serial.print("Temperature: "); 
        Serial.print(t);
        Serial.println(" *C");
    }
    
  Serial.print("The Light value is: ");
  Serial.println(TSL2561.readVisibleLux());
  delay(10);

  if (TSL2561.readVisibleLux() > 10){
    if (pos != 115){
      for (pos = 45; pos <= 115; pos += 1) { // goes from 0 degrees to 180 degrees
        // in steps of 1 degree
        myservo.write(pos);              // tell servo to go to position in variable 'pos'
        delay(300);                       // waits 15ms for the servo to reach the position
      }
      pos = 115;
    }
  }

 if (TSL2561.readVisibleLux() <= 10){
  if (pos != 45){
      for (pos = 115; pos >= 45; pos -= 1) { // goes from 180 degrees to 0 degrees
      myservo.write(pos);              // tell servo to go to position in variable 'pos'
      delay(300);                       // waits 15ms for the servo to reach the position
      }
     pos = 45;
   }
 }

 delay(1000);  
   
}
