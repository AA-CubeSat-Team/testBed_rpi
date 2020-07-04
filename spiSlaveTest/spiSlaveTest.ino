
volatile boolean process;
byte reqArr[4];
byte kk;
byte pp;
volatile byte reqB;
volatile byte rplB;

void setup (void){ 
  Serial.begin(115200);
  
  pinMode(MISO, OUTPUT);  // output thru "slave out" pin

  SPCR |= _BV(SPE);     // turn on SPI in slave mode  
  SPCR |= _BV(SPIE);    // turn on interrupts

  SPDR = 1;
  kk = 0;
  pp = 1;
  
  process = false;

  Serial.println("Setup complete");
} 


// SPI interrupt routine 
ISR (SPI_STC_vect){
  reqB = SPDR;
  
  if (kk < 3){
    reqArr[kk] = kk+2;
    kk++;
  }
  
  if (kk = 3){
    reqArr[kk] = kk+3;
    process = true;
  }
  
  rplB = reqB + 10;
  SPDR = rplB;               

}  

void loop (void){
  if(process){
    Serial.println("New Request");
    Serial.println(kk);                 // triggers twice for each 4 byte request
    Serial.println(sizeof(reqArr));     // contains 8 elements, both times
    for(int i = 0; i < sizeof(reqArr); i++){
      Serial.println(reqArr[i]);
      reqArr[i] = 0;
    }
    kk = 0;
    process = false;
  }
}  
