#include<SPI.h>  

byte reqArr[5];
volatile byte reqB;
volatile byte rplB;
volatile bool flag;
volatile byte kk;

// CURRENT STATE: returns manipilated request in correct form
// NEXT STEP: needs to be robust to changes in request length, eventually build in constant 0x00s
void setup (void){
  Serial.begin (115200);
  
  pinMode(MISO, OUTPUT);

  SPCR |= _BV(SPE);  
  SPCR |= _BV(SPIE);

  flag = false;
  kk = 0;

  Serial.println("Setup complete");
}  

ISR (SPI_STC_vect){
  reqB = SPDR;
  
  reqArr[kk] = reqB;
  kk++;
  
  if (kk == 5){
    flag = true;
  }

  rplB = reqB + 10;
  SPDR = rplB;
}


void loop (void){
  if (flag == true){
    for (int jj = 0; jj < 5; jj++){
      Serial.print(reqArr[jj]);
      Serial.print(" ");
    }
    Serial.println();
    flag = false;
    kk = 0;
  }
}
