#include<SPI.h>  

volatile byte reqArr[9];        
byte rplArr[6]; 
volatile byte reqB_new;
volatile byte reqB_old;
volatile byte rplB;
volatile byte flag;
volatile byte kk;
volatile byte yy;
volatile byte readReg;

// CURRENT STATE: sends follow-up reply package based on request contents
// NEXT STEP: 

void setup (void){
  Serial.begin (115200);
  
  pinMode(MISO, OUTPUT);

  SPCR = SPCR | bit(SPE);           // sets SPE bit in SPCR to 1, enabling SPI
  SPCR = SPCR | bit(SPIE);          // sets SPIE bit in SPCR to 1, enabling SPI interrupts
  
  SPDR = 0;
  flag = 0;
  kk = 0;
  yy = 0;
  reqB_old = 126;

  Serial.println("Setup complete");
}  


ISR (SPI_STC_vect){
  reqB_new = SPDR;

  if ( (reqB_old == 126) && (reqB_new == 126) ){      // master querying reply   
    SPDR = rplArr[yy];
    yy++;
  }
  if ( (reqB_old == 126) && (reqB_new != 126) ){      // beginning of request
    reqArr[kk] = reqB_new;
    kk++;
    yy = 0;
    SPDR = 126;
  }
  if ( (reqB_old != 126) && (reqB_new != 126) ){      // during request
    reqArr[kk] = reqB_new;
    kk++;
    SPDR = 126;
  }
  if ( (reqB_old != 126) && (reqB_new == 126) ){      // end of request
    SPI.detachInterrupt();          
    flag = 1;
  }
  
  reqB_old = reqB_new;
}

                                     
void loop (void){
  if (flag == 1){
    genReply(reqArr[0]);
    
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


void genReply(int id){
  byte rpl1[6] = {126,3,3,3,3,126};
  byte rpl2[6] = {126,4,4,4,4,126};
    
  switch(id) {
    case 1 :
      memcpy(rplArr, rpl1, sizeof(rpl1));
      break;
    case 2 :
      memcpy(rplArr, rpl2, sizeof(rpl1));
      break;
  }
}
