#include<SPI.h>  

volatile byte reqArr[9];        // robust to changes in req length, reqArr fills w 0s after flag
volatile byte rplArr[4] = {9,8,7,6};
volatile byte reqB_new;
volatile byte reqB_old;
volatile byte rplB;
volatile byte flag;
volatile byte kk;
volatile byte readReg;

// CURRENT STATE: recognizes flag, cuts interrupts to process data
// NEXT STEP: test on long 0x7E requests, input own reply package

void setup (void){
  Serial.begin (115200);
  
  pinMode(MISO, OUTPUT);

  SPCR = SPCR | bit(SPE);           // sets SPE bit in SPCR to 1, enabling SPI
  SPCR = SPCR | bit(SPIE);          // sets SPIE bit in SPCR to 1, enabling SPI interrupts
  
  SPDR = 0;
  flag = 0;
  kk = 0;
  reqB_old = 126;

  Serial.println(reqB_old);
}  



ISR (SPI_STC_vect){
  reqB_new = SPDR;

  if ( (reqB_old == 126) && (reqB_new == 126) ){       
    // set reply mode
  }
  if ( (reqB_old == 126) && (reqB_new != 126) ){  
    reqArr[kk] = reqB_new;
    kk++;
  }
  if ( (reqB_old != 126) && (reqB_new != 126) ){  
    reqArr[kk] = reqB_new;
    kk++;
  }
  if ( (reqB_old != 126) && (reqB_new == 126) ){  
    SPI.detachInterrupt();          
    flag = 1;
  }
  
  reqB_old = reqB_new;

  SPDR = 126;
}
                                     
//SPI.detachInterrupt();
void loop (void){
  if (flag == 1){
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
    reqB_old = 126;
    
    readReg = SPSR;
    readReg = SPDR;
    SPCR = SPCR | bit(SPIE);            
  }
}

/*
ISR (SPI_STC_vect){
  reqB = SPDR;
  reqArr[kk] = reqB;
  kk++;
  
  if (reqB == 126){
    SPI.detachInterrupt();          // sets SPIE bit in SPCR to 0, disabling interrupts 
    flag = 1;
  }
  
  rplB = reqB+2;                    
  SPDR = rplB;
}
                                     

void loop (void){
  if (flag == 1){
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
    
    readReg = SPSR;
    readReg = SPDR;
    SPCR = SPCR | bit(SPIE);            
  }
}
*/
