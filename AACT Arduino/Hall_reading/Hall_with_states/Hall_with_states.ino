/*=================================================================================
 * The purpose of this program is to use interrupts to read inputs from the hall sensor
 * and use states to interpret the data for speed and position.
 * 
 * Since the Hall sensors require the motor to be moving at a certain speed in order to function correctly 
 * this program will also be capable of driving the ESC using PWM's
 ================================================================================*/
#include <Servo.h>

 //hall sensor declerations
int A = 2;
int B = 3;
bool phaseA = false;
bool phaseB = false;
int state = 0;
unsigned int t0, t1, tr;
double rpm;


//CMG/ESC declerations
Servo CMG;//create an object for the CMG
int PWM_pin = 5;//have the PWM signal for the ESC sent to pin 5
int button = 8;//use a button on pin 8 to control the PWM signal
int pressed = 0;
int potPin = A0;

void setup() {
  pinMode(A, INPUT);//declare phaseA as an input the hall sensor has an internal pull up resistor
  pinMode(B,INPUT);//declare phaseB as an input the hall sensor has an internal pull up resistor
  attachInterrupt(digitalPinToInterrupt(A), detectedA, RISING);//attach an interrupt to phaseA that executes detectedA on the rising edge
  attachInterrupt(digitalPinToInterrupt(B), detectedB, RISING);//attach an interrupt to phaseB that executes detectedB on the rising edge

  pinMode(button, INPUT);//assign the button pin to an input  
  CMG.attach(PWM_pin, 1000, 2000);//attach the PWM pin to the cmg object
  
  Serial.begin(115200);//begin serial communication at 115200 bits/sec
}

void loop() {
  Hall();
  driver();
}

void Hall(){
  //Serial.print(state);
  //state 0 will be used as a null state since we don't know what position the motor will be starting in
  if(state == 0){
    if(phaseA && phaseB){
      state = 3;
      phaseA = false;
      phaseB = false;
    }
    
    else if(phaseB){
      state = 2;
      phaseB = false;
    }
    
    else if(phaseA){
      state = 1;
      phaseA = false;
    }
    
    else
      state = 0;
   t0 = micros();
    
  }
  
  if(state == 1){
    if(phaseA && phaseB){
      state = 3;
      phaseA = false;
      phaseB = false;
    }
    
  }

  if(state == 2){
    if(phaseA){
      phaseB = false;
      phaseA = false;
      state = 1;
    }
  }

  if(state == 3){
    if(phaseB){
      state = 2;
      phaseB = false;
      phaseA = false;
      t1 = micros();
      tr = t1 - t0;
      t0 = t1;

      }
    }
    
  if((micros()%1600000)<700){
    rpm = 1000000/(3*tr);
    Serial.println(rpm);
  }
}



void driver(){
  int potReading = analogRead(potPin);
  int duty = map(potReading, 0, 1023, 0, 175.5);
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


void detectedA(){
  phaseA = true;
}

void detectedB(){
  phaseB = true;
}
