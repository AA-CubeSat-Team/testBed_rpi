/**
 *     1. Plug your Arduino to your computer with USB cable, open terminal, then type 1 to send max throttle to every ESC to enter programming mode
 *     2. Power up your ESCs. You must hear "beep1 beep2 beep3" tones meaning the power supply is OK
 *     3. After 2sec, "beep beep" tone emits, meaning the throttle highest point has been correctly confirmed
 *     4. Type 0 to send min throttle
 *     5. Several "beep" tones emits, which means the quantity of the lithium battery cells (3 beeps for a 3 cells LiPo)
 *     6. A long beep tone emits meaning the throttle lowest point has been correctly confirmed
 *     7. Type 2 to launch test function. You then have three seconds to prescribe a motor output between 1 and 180. 
 *        Start with a value of about 5 or 3, then slowly try to work your way up to 25-ish. If the esc kills throttle to the motor,
 *        send 0 to the serial monitor to reset the esc. then send 2 to the serial monitor, and try again until the motors spin fast
 *        enough to syncronize with the esc.
 */
// ---------------------------------------------------------------------------
#include <Servo.h>
// ---------------------------------------------------------------------------
#define MIN_PULSE_LENGTH 1000 // Minimum pulse length in µs
#define MAX_PULSE_LENGTH 2000 // Maximum pulse length in µs
// ---------------------------------------------------------------------------
Servo mot1, mot2, mot3, mot4;
char data;
int command;
const int hallPinA = 7;
const int hallPinB = 12;
const int hallPinC = 13;
int z = 0;
const int hallSampleTime = 250*10^3; //milli seconds
unsigned long t0 = 0;
unsigned long t1 = 0;
unsigned long deltaMillis = 0;
int flag1 = 0;
int flag2 = 0;
//int rpm = 0;
unsigned long rpm = 0;

 volatile byte third_revolutions_mot1;
 unsigned long rpm_mot1;
 unsigned long timeold_mot1;

 volatile byte third_revolutions_mot4;
 unsigned long rpm_mot4;
 unsigned long timeold_mot4;


// ---------------------------------------------------------------------------

/**
 * Initialisation routine
 */
void setup() {
    Serial.begin(115200);
    
    mot1.attach(11, MIN_PULSE_LENGTH, MAX_PULSE_LENGTH);
    mot2.attach(10, MIN_PULSE_LENGTH, MAX_PULSE_LENGTH);
    mot3.attach(9, MIN_PULSE_LENGTH, MAX_PULSE_LENGTH);
    mot4.attach(8, MIN_PULSE_LENGTH, MAX_PULSE_LENGTH);

    pinMode(hallPinA,INPUT);
    pinMode(hallPinB,INPUT);
    pinMode(hallPinC,INPUT);
    
    displayInstructions();

   attachInterrupt(0, rpm_fun_mot1, RISING);
   digitalWrite(2, HIGH);
   third_revolutions_mot1 = 0;
   rpm_mot1 = 0;
   timeold_mot1 = 0;
   
   attachInterrupt(1, rpm_fun_mot4, RISING);
   digitalWrite(3, HIGH);
   third_revolutions_mot4 = 0;
   rpm_mot4 = 0;
   timeold_mot4 = 0;
}

/**
 * Main function
 */
void loop() {
    if (Serial.available()) {
        data = Serial.read();

        switch (data) {
            // 0
            case 48 : Serial.println("Sending minimum throttle");
                      mot1.writeMicroseconds(MIN_PULSE_LENGTH);
                      mot2.writeMicroseconds(MIN_PULSE_LENGTH);
                      mot3.writeMicroseconds(MIN_PULSE_LENGTH);
                      mot4.writeMicroseconds(MIN_PULSE_LENGTH);
            break;

            // 1
            case 49 : Serial.println("Sending maximum throttle");
                      mot1.writeMicroseconds(MAX_PULSE_LENGTH);
                      mot2.writeMicroseconds(MAX_PULSE_LENGTH);
                      mot3.writeMicroseconds(MAX_PULSE_LENGTH);
                      mot4.writeMicroseconds(MAX_PULSE_LENGTH);
            break;

            // 2
            case 50 : Serial.print("Running max in 3");
                      test();
            break;
        }
    }
    
  /*Serial.print(mot4.read());
  Serial.print("      ");
  Serial.println(mot1.read()); */
  
  /*if (third_revolutions >= 90) { 
     //Update RPM every 20 counts, increase this for better RPM resolution,
     //decrease for faster update
     rpm = 20.0*1000000.0/(micros() - timeold)*third_revolutions;
     timeold = micros();
     third_revolutions = 0;
     Serial.print("RPM is ");
     Serial.println(rpm,DEC);
   }*/

  if (third_revolutions_mot1 >= 90) { 
     Serial.print("RPM motor 1 = ");
     print_rpm(third_revolutions_mot1, timeold_mot1);
     timeold_mot1 = micros();
     third_revolutions_mot1 = 0;
   }

   if (third_revolutions_mot4 >= 90) { 
     Serial.print("RPM motor 4 = ");
     print_rpm(third_revolutions_mot4, timeold_mot4);
     timeold_mot4 = micros();
     third_revolutions_mot4 = 0;
   }

   
  //get_rpm();
}

/**
 * Test function: send min throttle to max throttle to each ESC.
 * Customizing to test motor at constant max
 */
void test() {

    Serial.println("Give test command");
    delay(3000);
    if (Serial.available()) {
      command = Serial.parseInt();
    mot1.write(command);
    /*mot2.write(150);
    mot3.write(60); */
    mot4.write(command);
    }
}

/**
 * Displays instructions to user
 */
void displayInstructions()
{  
    Serial.println("READY - PLEASE SEND INSTRUCTIONS AS FOLLOWING :");
    Serial.println("\t0 : Send min throttle");
    Serial.println("\t1 : Send max throttle");
    Serial.println("\t2 : Run test function\n");
}

/*void get_rpm() {
  z = digitalRead(hallPinA);
  Serial.println(z);
  if(z == 1 && flag1 == 0) {
    t0 = millis();
    flag1 = 1;
    Serial.println("pass check 1");
  }
  if (flag1 == 1 && z == 0) {
    flag2 = 1;
    Serial.println("pass check 2");
  }
  if(flag1 == 1 && flag2 == 1 && z == 1) {
    t1 = millis();
    deltaMillis = (t1 - t0);
    flag1 = 0;
    flag2 = 0;
    Serial.print("Time Difference in Millis ");
    Serial.println(deltaMillis);
    rpm = (1/(deltaMillis*10^3))*60*(1/3);
    Serial.print("RPM is ");
    Serial.println(rpm);
    Serial.println("pass check 3");
  }
}*/

 void print_rpm(volatile byte third_revolutions, unsigned long timeold) {
     rpm = 20.0*1000000.0/(micros() - timeold)*third_revolutions;
     Serial.println(rpm,DEC);
 }

 void rpm_fun_mot1()
 {
   third_revolutions_mot1++;
   //Each rotation, this interrupt function is run twice
 }

  void rpm_fun_mot4()
 {
   third_revolutions_mot4++;
   //Each rotation, this interrupt function is run twice
 }

