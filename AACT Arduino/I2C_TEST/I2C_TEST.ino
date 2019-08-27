#include <Wire.h>

int x = 0;
void setup() {
  // put your setup code here, to run once:
  Wire.begin(9);
  Wire.onReceive(receiveEvent);
  Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  
}

void receiveEvent(int howMany){
  x = Wire.read();
  Serial.println("received");
  
}
