/**
 *     1. Plug your Arduino to your computer with USB cable, open terminal, then type 1 to send max throttle to every ESC to enter programming mode
 *     2. Power up your ESCs. You must hear "beep1 beep2 beep3" tones meaning the power supply is OK
 *     3. After 2sec, "beep beep" tone emits, meaning the throttle highest point has been correctly confirmed
 *     4. Type 0 to send min throttle
 *     5. Several "beep" tones emits, which means the quantity of the lithium battery cells (3 beeps for a 3 cells LiPo)
 *     6. A long beep tone emits meaning the throttle lowest point has been correctly confirmed
 *     7. Type 2 to launch test function. This will send min to max throttle to ESCs to test them
 */
// ---------------------------------------------------------------------------
#include <Servo.h>
// ---------------------------------------------------------------------------
#define MIN_PULSE_LENGTH 1040 // Minimum pulse length in µs
#define MAX_PULSE_LENGTH 2000 // Maximum pulse length in µs
// ---------------------------------------------------------------------------
Servo mot1, mot2, mot3, mot4;
char data;
// ---------------------------------------------------------------------------

/**
 * Initialisation routine
 */
void setup() {
    Serial.begin(115200);
    
    mot1.attach(51, MIN_PULSE_LENGTH, MAX_PULSE_LENGTH);
    mot2.attach(49, MIN_PULSE_LENGTH, MAX_PULSE_LENGTH);
    mot3.attach(47, MIN_PULSE_LENGTH, MAX_PULSE_LENGTH);
    mot4.attach(48, MIN_PULSE_LENGTH, MAX_PULSE_LENGTH);
    
    displayInstructions();
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
                     // mot1.writeMicroseconds(MIN_PULSE_LENGTH);
                     // mot2.writeMicroseconds(MIN_PULSE_LENGTH);
                      mot3.writeMicroseconds(MIN_PULSE_LENGTH);
                     // mot4.writeMicroseconds(MIN_PULSE_LENGTH);
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
    

}

/**
 * Test function: send min throttle to max throttle to each ESC.
 * Customizing to test motor at constant max
 */
void test()
{
    Serial.println("max");
    /*mot1.write(50);
    mot2.write(150);*/
    mot3.write(60);
    //mot4.write(60);
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
