#include <Wire.h>
#include <OneWire.h>

// #define DHTPIN A0
// #define DHTTYPE DHT22
// DHT dht(DHTPIN, DHTTYPE);

int heatPin = 12;      // Heater connected to digital pin 12
int rainPin1 = 10;       // Rain sensor 2 to digital pin 11
int rainPin2 = 11;       // Rain sensor 1 to digital pin 10

float status1 = 0;      // Rain Sensor status
float status2 = 0;
int rainStatus = 0;     //Reported rain value

float rainCount = 0;      // Track positive rain checks
float rainCountTotal = 0;       // Tracks number of rain checks

int sleepcount = 20;     // 0.1 sec per int
int heatStatus = 0;       // Binary heater status

void setup(void) {
  Serial.begin(9600);
  pinMode(rainPin1, INPUT_PULLUP);      //Require a pull-up voltage for a positive measure on rain
  pinMode(rainPin2, INPUT_PULLUP);
  pinMode(heatPin, OUTPUT);
  Serial.println("Pins attached");
}

int heatOn(){
       if (heatStatus == 1){
          Serial.println("heat=1");
          }
       else{
          digitalWrite(heatPin, HIGH);
          heatStatus = 1;
          Serial.println("heat=1");
          }  
      return 1;
}

int heatOff(){
       if (heatStatus == 0){
          Serial.println("heat=0");
          }
       else{
          digitalWrite(heatPin, LOW);
          heatStatus = 0;
          Serial.println("heat=0");
          }  
      return 0;
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

int rainStatus(){
	status1 = checkRainSensor1();
    	status2 = checkRainSensor2();
    	if (status1 == 1.0 || status2 == 1.0){
      		rainCount = rainCount + 1.0;
    	}
    	rainCountTotal = rainCountTotal + 1.0;
    	//Serial.println(rainCount / rainCountTotal);
    	if (rainCountTotal == sleepcount){
      		Serial.print("heat=");
        	Serial.print(heatStatus);
      		if ((rainCount / rainCountTotal) > 0.75){
        		Serial.println(",rain=1");
        	}
      		else {
        	Serial.println(",rain=0");
        	//rainStatus = 0;
      }
      //Serial.println("Clearing previous rain data");
      rainCount = 0;
      rainCountTotal = 0;
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
      }
    }
    
    delay(sleepcount);
  }
