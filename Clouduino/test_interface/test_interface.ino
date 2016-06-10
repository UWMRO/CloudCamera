
void setup(void)
{
  // start serial port
  Serial.begin(9600);
  // Start up the library
}

void printLine(void)
{
    Serial.println("Called Test Function");
}

void loop(void)
{ 
  if (Serial.available() >0){
     int inByte= Serial.read();
  switch (inByte){
    case 's':
      printLine();
      
    }
  }
}

