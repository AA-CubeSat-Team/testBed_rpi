#include<SPI.h>  

byte reqArr[4];
volatile byte reqB;
volatile byte rplB;
volatile bool flag;
volatile byte kk;

void setup (void){
  Serial.begin (115200);
  
  pinMode(MISO, OUTPUT);

  SPCR |= _BV(SPE);  
  SPCR |= _BV(SPIE);

  flag = false;
  kk = 0;
}  

ISR (SPI_STC_vect){
  reqB = SPDR;
  
  reqArr[kk] = reqB;
  kk++;
  
  if (kk == 4){
    flag = true;
  }

  rplB = reqB + 10;
  SPDR = rplB;
}


void loop (void){
  if (flag == true){
    for (int jj = 0; jj < 4; jj++){
      Serial.print(reqArr[jj]);
      Serial.print(" ");
    }
    Serial.println();
    flag = false;
    kk = 0;
  }
}
