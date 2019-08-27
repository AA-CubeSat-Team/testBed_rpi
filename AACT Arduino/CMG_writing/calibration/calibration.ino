/*
This program is designed to calibrate the ESC and run the CMG at max throttle

When the ESC is calibrating it expects to see the highest point at power on, and then see the lowest point after

he ESC will cause the motor to emit some sounds, if you don't hear these the ESC is not calibrating
*/
#include <Servo.h>
Servo CMG;//create an object for the CMG

int PWM_pin = 7;//have the PWM signal for the ESC sent to pin A0
int button = 8;//use a button on pin 5 to control the PWM signal
int pressed = 0;

void setup() {
  pinMode(button, INPUT);//assign the button pin to an input  
  CMG.attach(PWM_pin, 1000, 2000);//attach the PWM pin to the cmg object
  Serial.begin(9600);
}//void setup

void loop() {

 if(digitalRead(button)){
   CMG.write(90);
   Serial.println("pressed");
   pressed = 1;
 }//if
 else if(pressed == 1){
  CMG.writeMicroseconds(150);
  Serial.println("150");
 }
 else{
    CMG.writeMicroseconds(180);
    Serial.println("High");
 }//else

}//void loop
