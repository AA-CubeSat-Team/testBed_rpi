# include <SPI.h>

volatile boolean received;
volatile byte Slavereceived;
volatile byte Slavesend;

void setup() {
  Serial.begin(115200);   // standard serial monitor set up

  pinMode(MISO,OUTPUT);   // sends output through "slave out" pin

  SPCR |= _BV(SPE);       // puts SPI Control Register in slave mode
  received = false;

  SPI.attachInterrupt();  // if data received from master, interrupt is triggered
}


ISR (SPI_STC_vect) {      // interrupt service routine
  Slavereceived = SPDR;   // byte from transfer                
  received = true;                       
}


void loop() {
  if(received) {                           // logic to SET LED ON OR OFF depending upon the value recerived from master
    if (Slavereceived == 1) {              // "1" is the contents of the SPI transfer
        Serial.println("Slave LED ON");
    }
    else {
        Serial.println("Slave LED OFF");
    }
/*
    buttonvalue = digitalRead(buttonpin);  // reads the status of the pin 2
      
      if (buttonvalue == HIGH) {           // logic to set the value of x to send to master
        x = 1;
      }  
      else {
        x = 0;
      }
      
    Slavesend = x;                             
    SPDR = Slavesend;                      // sends the x value to master via SPDR 
*/    
    delay(1000);
  }

  
}
