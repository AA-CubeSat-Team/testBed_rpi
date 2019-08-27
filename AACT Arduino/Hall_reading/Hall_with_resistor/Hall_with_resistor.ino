/* Hall with interrupts, external resistor
 *  Can this be replicated using internal pullup resistor?
 *  RPM calculations need some work still
 *  Need to work in a second sensor
 */
#include <Servo.h>

//CMG/ESC declerations
Servo CMG;//create an object for the CMG
int PWM_pin = 5;//have the PWM signal for the ESC sent to pin 5
int button = 8;//use a button on pin 8 to control the PWM signal
int pressed = 0;
int potPin = A0;
int duty;

//Hall declerations
 volatile byte third_revolutions;
 float rpm, lpm;
 unsigned long timeold;
 
 void setup()
 {
   Serial.begin(115200);

   pinMode(button, INPUT);//assign the button pin to an input  
   CMG.attach(PWM_pin, 1000, 2000);//attach the PWM pin to the cmg object
   
   attachInterrupt(0, magnet_detect, RISING);  //Initialize the interrupt pin (Arduino digital pin 2)
   third_revolutions = 0;
   rpm = 0;
   timeold = 0;
 }
 void loop()//Measure RPM
 {
  driver();
   if (third_revolutions >= 18) { 
     rpm = float(third_revolutions*60*1000000)/float((micros() - timeold)*3);
     timeold = micros();
     third_revolutions = 0;
     Serial.println(rpm);
     Serial.print("PWM = ");
     Serial.println(duty);

   }
 }


void driver(){
  int potReading = analogRead(potPin);
  duty = map(potReading, 0, 1023, 0, 175.5);
  //Serial.print(duty);
  if(digitalRead(button)){
   CMG.write(0);
   Serial.println("pressed");
   pressed = 1;
 }//if
 else if(pressed == 1){
  CMG.write(duty);
 }
 else{
    CMG.write(180);
    Serial.println("High");
 }//else
}
 
 void magnet_detect()  //This function is called whenever a magnet/interrupt is detected by the arduino
 {
   third_revolutions++;
 }
