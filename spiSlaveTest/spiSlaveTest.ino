
volatile boolean received;
byte reqByte;
byte rpl;

void setup (void){ 
  Serial.begin(115200);
  
  pinMode(MISO, OUTPUT);  // output thru "slave out" pin

  SPCR |= _BV(SPE);     // turn on SPI in slave mode  
  SPCR |= _BV(SPIE);    // turn on interrupts
  
  received = false;

  Serial.println("Setup complete");
}  // end of setup


// SPI interrupt routine (triggers once for each byte in request)
ISR (SPI_STC_vect){
  reqByte = SPDR;               //sizeof(reqByte) = 1, reads a single byte at a time
  Serial.println(reqByte);
  Serial.println("interrupt");
  rpl = reqByte;
  SPDR = rpl;
  
  received = true; 
}  // end of interrupt service routine (ISR) SPI_STC_vect

void loop (void){
  if(received){
  }
}  // end of loop
