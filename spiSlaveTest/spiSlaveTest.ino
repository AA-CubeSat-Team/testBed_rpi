
volatile boolean process;
int reqArr[5];
int kk;
int pp;
volatile byte req;
volatile byte rpl;

void setup (void){ 
  Serial.begin(115200);
  
  pinMode(MISO, OUTPUT);  // output thru "slave out" pin

  SPCR |= _BV(SPE);     // turn on SPI in slave mode  
  SPCR |= _BV(SPIE);    // turn on interrupts

  SPDR = 1;
  kk = 0;
  
  process = false;

  Serial.println("Setup complete");
}  // end of setup


// SPI interrupt routine 
ISR (SPI_STC_vect){
  req = SPDR;
  Serial.println(pp++);
  
  if (kk < 4){
    reqArr[kk] = req;
    Serial.println("first");
    kk++;
  }
  
  if (false){
    reqArr[kk] = req;
    process = true;
    Serial.println("kk=4");
  }
  
  rpl = req;
  SPDR = rpl;               // need to create mechanism to store req bytes in an array

}  // end of interrupt service routine (ISR) SPI_STC_vect

void loop (void){
  if(process){
    Serial.println(kk);
    Serial.println(sizeof(reqArr));
    kk = 0;
    process = false;
  }
}  // end of loop
