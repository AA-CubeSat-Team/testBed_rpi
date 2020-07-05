#include<SPI.h>  

volatile byte reqArr[9];
volatile byte rplArr[4] = {9,8,7,6};
volatile byte reqB;
volatile byte rplB;
volatile bool flag;
volatile byte kk;

// CURRENT STATE: returns manipulated request in correct form
// NEXT STEP: needs to be robust to changes in request length, eventually build in constant 0x7Es
void setup (void){
  Serial.begin (115200);
  
  pinMode(MISO, OUTPUT);

  Serial.print("SPE: ");           // SPCR is 1 byte, 8 bits, where each bit controls something
  Serial.println(SPE, BIN);
  SPCR = SPCR | bit(SPE);           // sets SPE bit in SPCR to 1, enabling SPI
  SPCR = SPCR | bit(SPIE);          // sets SPIE bit in SPCR to 1, enabling SPI interrupts
  Serial.print("SPCR: ");
  Serial.println(SPCR, BIN);
  
  SPDR = 0;
  flag = false;
  kk = 0;

  Serial.println("Setup complete");
  Serial.println(bit(SPIE));
}  

ISR (SPI_STC_vect){
  reqB = SPDR;
  
  reqArr[kk] = reqB;
  kk++;
  
  if (reqB == 126){
    SPI.detachInterrupt();
    flag = true;
    Serial.println("flag");
  }

  if (reqB == 8){
    SPI.detachInterrupt();
    flag = true;
    Serial.println("flag");
  }
  
  rplB = reqB+2;                     // finishes ISR even after interrupt is detached
  SPDR = rplB;
}
                                      // cannot execute void loop() until done receiving bytes

void loop (void){
  if (flag == true){
    Serial.print("req: ");
    for (int jj = 0; jj < sizeof(reqArr); jj++){
      Serial.print(reqArr[jj]);
      Serial.print(" ");
      reqArr[jj] = 0;
    }
    Serial.println();
    SPDR = 0;
    flag = false;
    kk = 0;
    delay(500);                      // interrupt flag is set even when interrupts are detached
    //SPIF |= 1;
    SPI.attachInterrupt();            // retriggers interrupt before transmission is over
  }
}
