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
  Serial.println((rcv));    // sizeof(rcv)=1, only sees 1 byte at a time
  
  rpl = 1;
  SPDR = rpl;             // transfers rpl back up MISO
  
  received = true;                    
}

// ISSUE: sends rpl byte, then starts repeating back the rcv bytes
// CHECK: storing rcv byte in SPDR? -> stores second byte in SPDR ??
//        probably need to research into more

// ISSUE: want to store/send rcv and rpl bytes as connected array
// SOLVE: possibly use iteration to store into array? need to understand how SPDR works

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
