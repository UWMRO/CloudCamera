#include <Wire.h>
#include <OneWire.h>

// #define DHTPIN A0
// #define DHTTYPE DHT22
// DHT dht(DHTPIN, DHTTYPE);

int heatPin = 12;      // Heater connected to digital pin 12
int rainPin1 = 10;       // Rain sensor 2 to digital pin 11
int rainPin2 = 11;       // Rain sensor 1 to digital pin 10

int sleepcount = 1;     // sleep time between sensor checks, 0.1 sec per int
int numReadings = 300;
int readings[300];      // the readings from the analog input
int readIndex = 0;              // the index of the current reading
float total = 0;                  // the running total
float average = 0;                // the average

float status1 = 0;      // Rain Sensor status
float status2 = 0;
int rainStatus = 0;     //Reported rain value
int heatStatus = 0;       // Binary heater status

int rainCheck = 0;
float rainCount = 0;      // Track positive rain checks
float rainCountTotal = 0;       // Tracks number of rain checks




void setup(void) {
  Serial.begin(9600);
  pinMode(rainPin1, INPUT_PULLUP);      //Require a pull-up voltage for a positive measure on rain
  pinMode(rainPin2, INPUT_PULLUP);
  pinMode(heatPin, OUTPUT);
  Serial.println("Pins attached");
}

int heatOn(){
       if (digitalRead(heatPin) == HIGH){
          heatStatus = 1;
          //Serial.println("heat=1");
          }
       else{
          digitalWrite(heatPin, HIGH);
          heatStatus = 1;
          //Serial.println("heat=1");
          }  
      return 1;
}

int heatOff(){
       if (digitalRead(heatPin) == LOW){
          //Serial.println("heat=0");
          heatStatus = 0;
          }
       else{
          digitalWrite(heatPin, LOW);
          heatStatus = 0;
          //Serial.println("heat=0");
          }  
      return 0;
}

int checkHeat(){
      if (digitalRead(heatPin) == LOW){
          heatStatus = 0;
      } 
      else if (digitalRead(heatPin) == HIGH){
          heatStatus = 1;
      }
      else{
          heatOff();
          heatStatus = 0;
      }
      return heatStatus;
}
int checkRainSensor1(){
      int status = digitalRead(rainPin1);     //Read rain sensor pin
      if (status == 0){                       //If the voltage is zero, there was a positive rain reading
        //Serial.println("rain1 = True");
        return 1;
        }
      else{
        //Serial.println("rain1 = False");
        return 0;
        }
}

int checkRainSensor2(){
      int status = digitalRead(rainPin2);
      if (status == 0){
        //Serial.println("rain2 = True");
        return 1;
        }
      else{
        //Serial.println("rain2 = False");
        return 0;
        }
}

int checkRain(){
      status1 = checkRainSensor1();
      status2 = checkRainSensor2();
      if (status1 == 1.0 || status2 == 1.0){
        rainCheck = 100;
      }
      else{
        rainCheck = 0;
      }
      total = total - readings[readIndex];    // subtract the last reading:
      readings[readIndex] = rainCheck;        // read from the sensor:
      total = total + readings[readIndex];    // add the reading to the total:
      readIndex = readIndex + 1;              // advance to the next position in the array:
    
      if (readIndex >= numReadings) {         // if we're at the end of the array...
        readIndex = 0;                        // ...wrap around to the beginning:
      }
    
      average = float(total) / float(numReadings);          // calculate the average:
      //Serial.print("rain=");
      //Serial.print(average);
      //delay(1);        // delay in between reads for stability
      return float(average);
}


void test(void){
  Serial.println("test routine");
}

void loop(void) {
  if (Serial.available() > 0) {
    int inByte = Serial.read();
    switch (inByte) {
      case 'y':
         test();
         break;
      case 'h':
          heatOn();
          break;
      case 'l':
          heatOff();
          break;
      case 's':
          Serial.print("heat=");
          Serial.print(checkHeat());
          Serial.print(",rain=");
          Serial.println(checkRain());
          break;
      }
    }
    checkRain();
    //Serial.println(checkRain());
    delay(100*sleepcount);
  }
