#include <SoftwareSerial.h>

#PWM Variables/Definitions
unsigned long esc_timer = 0, zero_timer = 0, tcal = 0;
unsigned long tc1 = 0, tmax = 0;
#END PWM DEFINITIONS


#ESC Variables
bool cal = true;
bool full_cal;
double mot = 0;  # Motor "thrust" level
const byte escPin = 11;
const byte escRx = 0;
const byte escTx = 1; # Not used, but necessary to define for software serial

# Hall Sensor Variables
const int hallAPin = 2;
const int hallBPin = 3;
const int hallCPin = 4;
const unsigned long sampleTime = 1000;

# Virtual Serial Port
SoftwareSerial escSerial (escRx,escTx);

void setup() 
  # put your setup code here, to run once:

  full_cal = false;

  # ESC Setup
  # Set pin to output
  pinMode(escPin,OUTPUT);
  
  # Start Serial Monitor
  Serial.begin(115200);
  Serial.println("Starting Serial Output...");

  # Start Virtual Serial Port for ESC telemetry reception
  escSerial.begin(57600);
  Serial.println("Starting Virtual Serial Port for ESC Telemetry...");

  # Warn to power ESC (remove when arduino and esc are powered simultaneously
  Serial.println("Connect ESC Now");
  delay(3000);

  # Set timers
  tcal = micros();  # Timer for ESC Calibration


void loop() 
  # Start control loop timer
  zero_timer = micros();  

  # ESC Calibration
  if (cal == true && full_cal == false) 
    esc_cal_fast();
  else if (cal == false) 
    #  Set motor commands here - just a constant signal
    mot = 1500;

    # Query the hall sensors and print RPMS
    int rpms[] = 0,0,0;
    getRPMs(rpms);
    char tempstr[50];
    sprintf(tempstr,"%i,%i,%i\n",rpms[0],rpms[1],rpms[2]);
    Serial.write(tempstr);
  

  # Ensure consistend loop time of ~5500us (not necessary?)
  #while(micros() - zero_timer)
  
  # Send motor command to ESC via manual PWM 
  pwm_to_esc(mot);
  


void pwm_to_esc(double mot) 
  # Note that the zero_timer is set at the start of main loop (also have a secondary timer loop_timer)

  # Set PWM Limits on Controlled Outputs
  /* Max Speed: 1950 #Prevents power supply from hitting overcurrent switch, and restarting. This can likely be changed for battery powered systems.
     Min Speed: 1000 #Motor will stop completely */

  if (mot > 1950) 
    mot = 1950;
  
  else if (mot < 1000 && full_cal == false) 
    mot = 1000;
  

  # 1. PULSE START #
  # Note this is done here as it is better to perform the calculation while the pulse is active
  # preventing it from overrunning the 2000us PWM pulse timing.

  zero_timer = micros();  # Resets timer zeropoint

  digitalWrite(escPin,HIGH);   # Sets escPin to High

  # 2. LENGTH OF PULSE CALCULATED #
  # Commands for ESC's governing motor 1/motor 2/motor 3/motor 4, scale of m1/m2/m3/mot[3]dictated by controller
  #(Port)   (Arduino Pin)
  tc1 = mot + zero_timer; # End of the pulse
  tmax = 2000 + zero_timer; # Maximum pulse time 2000us, will end pulse regardless of command function


  # 3. SEND PULSE TO ESC AND WAIT FOR 2000us PULSE DURATION FOR PWM#
  # Look for when all ESC's have finished communicating

  while (micros() < tmax)    #runs if any port on PORTD is active
    esc_timer = micros();
    
    # Pulse end
    if (tc1 <= esc_timer) 
      digitalWrite(escPin,LOW);
    
  

  # Ensure pins are pulled low
  digitalWrite(escPin,LOW);
  ## PWM MANUAL PULSE COMPLETED ##
  return;


void esc_cal_fast() 
  # After short duration, run at "0" throttle and allow for ESC to calibrate like normal.
  if ((micros() - tcal) < 8000000) 
    mot = 1000;
  
  else if ((micros() - tcal) >= 8000000) 
    if (micros() - tcal <= 8001000) 
      Serial.println("ESC Ready! Running motors at low RPM");
    
    else 
      # Run motor at low RPM to test for around 1 seconds
      mot = 1100;
      
      if (micros() - tcal >= 9000000) 
        cal = false;
        tcal = 0;            # clears calibration variables
      
    
  

  return;


void getRPMs(int rpms[]) 
   int countA = 0;
   int countB = 0;
   int countC = 0;
   int numPoles = 6;
   boolean countFlagA = LOW;
   boolean countFlagB = LOW;
   boolean countFlagC = LOW;
   unsigned long currentTime = 0;
   unsigned long startTime = millis();

   # Loop for the sample time, and increment counter 
   while (currentTime <= sampleTime) 
    # Hall A
    if (digitalRead(hallAPin) == HIGH) 
      countFlagA = HIGH;
    
    if (digitalRead(hallAPin) == LOW && countFlagA == HIGH) 
      countA++;
      countFlagA = LOW;
    

    # Hall B
    if (digitalRead(hallBPin) == HIGH) 
      countFlagB = HIGH;
    
    if (digitalRead(hallBPin) == LOW && countFlagB == HIGH) 
      countB++;
      countFlagB = LOW;
    

    # Hall C
    if (digitalRead(hallCPin) == HIGH) 
      countFlagC = HIGH;
    
    if (digitalRead(hallCPin) == LOW && countFlagC == HIGH) 
      countC++;
      countFlagC = LOW;
    
    
    currentTime = millis() - startTime;
   

  # Correct counts
  countA = countA/numPoles;
  countB = countB/numPoles;
  countC = countC/numPoles;

  # Calculate RPM
  rpms[0] = int(60000/float(sampleTime))*countA;   
  rpms[1] = int(60000/float(sampleTime))*countB;
  rpms[2] = int(60000/float(sampleTime))*countC;

