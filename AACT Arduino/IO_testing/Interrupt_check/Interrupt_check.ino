/*The purpose of this file is to check if a given pin
 * can have an interrupt attached to it
 */
int PUT = 3;
int light = 2;//a pin that is known to be usable with int's should be used

void setup() {
  pinMode(PUT, INPUT_PULLUP);
  pinMode(light, OUTPUT);
  attachInterrupt(digitalPinToInterrupt(PUT), func, RISING);

}

void loop() {
  digitalWrite(light, LOW);
  delay(2000);
}

void func(){
  digitalWrite(light, HIGH);
}
