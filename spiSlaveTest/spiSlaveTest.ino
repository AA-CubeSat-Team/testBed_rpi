# include <SPI.h>

volatile boolean received;
volatile byte rcv;
volatile byte rpl;

void setup() {
  Serial.begin(115200);   // standard serial monitor set up

  pinMode(MISO,OUTPUT);   // sends output through "slave out" pin

  SPCR |= _BV(SPE);       // puts SPI Control Register in slave mode
  received = false;

  SPI.attachInterrupt();  // if data received from master, interrupt is triggered
  Serial.println("Setup complete");
}


ISR (SPI_STC_vect) {      // interrupt service routine
  rcv = SPDR;   // byte from transfer                
  Serial.println(rcv);
  
  rpl = 7;
  SPDR = rpl;             // transfers rpl back up MISO
  
  received = true;                    
}

// ISSUE: not triggering interrupt
// CHECK: wiring/pins, interrupt configured correctly, RPi transferrring correctly,
//        compatibility of signals, 5V vs 3.3V

void loop() {
/*  
  if(received) {                           // logic to SET LED ON OR OFF depending upon the value recerived from master
    if (rcv == 1) {              // "1" is the contents of the SPI transfer
        Serial.println("Slave LED ON");
    }
    else {
        Serial.println("Slave LED OFF");
    }    
    delay(1000);
  }
  Serial.println(received);
*/  
}
