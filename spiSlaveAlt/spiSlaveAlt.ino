#include<SPI.h>  

volatile byte reqArr[9];        
byte rplArrT[16] = { }; 
byte rplArrD[16] = { };
byte rplArrX[16] = { }; 
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
    SPDR = rplArrX[yy];
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


void genReply(byte id){                       // want to build XOR functionality into genReply to deliver
  byte rplArr1T[6] = {126,id,126,3,3,126};       //    final reply array to SPI interrupt sequence
  byte rplArr2T[6] = {126,id,126,4,4,126};
  byte rplArr3T[6] = {126,id,126,5,5,126};
  byte rplArr4T[6] = {126,id,126,6,6,126};
    
  switch(id) {
    case 1 :
      memcpy(rplArrT, rplArr1T, sizeof(rplArr1T));
      break;
    case 2 :
      memcpy(rplArrT, rplArr2T, sizeof(rplArr2T));
      break;
    case 3 :
      memcpy(rplArrT, rplArr3T, sizeof(rplArr3T));
      break;
    case 4 :
      memcpy(rplArrT, rplArr4T, sizeof(rplArr4T));
      break;
  }

  int ff = 0;
  int ee = 0;
  for (int tt = 0; tt < sizeof(rplArrT); tt++){        
    if (rplArrT[tt] != 125){
      rplArrD[tt+ff] = rplArrT[tt];
    }
    if (rplArrT[tt] == 125){
      rplArrD[tt+ff] = 125;
      rplArrD[tt+ff+1] = rplArrT[tt]^0x20;
      ff++;
    }
  }                                            
  for (int dd = 0; dd < (sizeof(rplArrT)+ff); dd++){
    if ( (dd != 0) || (dd != sizeof(rplArrT)+ff-1) || (rplArrD[dd] != 126) ){
      rplArrX[dd+ee] = rplArrD[dd];
    }
    if ( (dd != 0) && (dd != sizeof(rplArrT)+ff-1) && (rplArrD[dd] == 126) ){
      rplArrX[dd+ee] = 125;
      rplArrX[dd+ee+1] = rplArrD[dd]^0x20;
      ee++;
    }
  }
}
