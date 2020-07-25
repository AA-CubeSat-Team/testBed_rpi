#include<SPI.h>  

volatile byte reqArrX[20] = { };
byte reqArrT[20] = { };  
int qq;      
byte rplArr[28] = { }; 
int rplLen;
int ee;
int ff;
volatile byte reqB_new;
volatile byte reqB_old;
volatile byte flag;
volatile byte kk;
volatile byte yy;
volatile byte readReg;


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
    reqArrX[kk] = reqB_old;
    kk++;
    reqArrX[kk] = reqB_new;
    kk++;
    SPDR = 126;
  }
  if ( (reqB_old != 126) && (reqB_new != 126) ){      // during request
    reqArrX[kk] = reqB_new;
    kk++;
    SPDR = 126;
  }
  if ( (reqB_old != 126) && (reqB_new == 126) ){      // end of request
    SPI.detachInterrupt();   
    reqArrX[kk] = reqB_new;
    kk++;       
    flag = 1;
  }
  
  reqB_old = reqB_new;
}

                                     
void loop (void){
  if (flag == 1){
    
    qq = 0;
    int reqLenX = kk;
    for (int xx = 0; xx < reqLenX; xx++){
      if (reqArrX[xx+qq] != 125){
        reqArrT[xx] = reqArrX[xx+qq];
      }
      if (reqArrX[xx+qq] == 125){
        reqArrT[xx] = reqArrX[xx+qq+1]^0x20;
        qq++;
      }
    }

    for (int rr = 0; rr < sizeof(rplArr); rr++){
      rplArr[rr] = 0;
    }
    genReply(reqArrT[1]);                
    yy = 0;
        
    Serial.print("req: ");
    for (int jj = 0; jj < sizeof(reqArrT); jj++){
      Serial.print(reqArrT[jj], HEX);
      Serial.print(" ");
      reqArrT[jj] = 0;
    }
    Serial.println();
    Serial.print("rpl: ");
    for (int jj = 0; jj < sizeof(rplArr); jj++){
      Serial.print(rplArr[jj], HEX);
      Serial.print(" ");
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


void genReply(byte id){ 
  // 1 - reset MCU
      // no reply                     
      byte rplArr1[7] = {0x7E, 0x01, 0x01, 0x1F,0x3E, 0x7E};
  // 2 - get last reset status
      // uint8_t reset status 0:7
      byte rplArr2[7] = {0x7E, 0x02, 0x01, 0x05, 0x68,0xC1, 0x7E};
  // 3 - clear last reset status
      // no reply
      byte rplArr3[7] = {0x7E, 0x03, 0x01, 0x7D,0x5D,0x58, 0x7E};
  // 4 - get reaction wheel status
      // int32_t currSpeed 4 -65000:65000, int32_t refSpeed 4 -65000:65000, uint8_t state 1 0:4, uint8_t clcMode 1 0:1
      byte rplArr4[16] = {0x7E, 0x04, 0x01, 0x60,0xEA,0x00,0x00, 0xE7,0xFD,0x00,0x00, 0x04, 0x01, 0xCC,0x33, 0x7E};
  // 5 - init reaction wheel controller
      // no reply
      byte rplArr5[6] = {0x7E, 0x05, 0x01, 0xDB,0xF2, 0x7E};
  // 6 - set ref speed
      // no reply
      byte rplArr6[6] = {0x7E, 0x06, 0x01, 0x88,0xA7, 0x7E};
  // 7 - set current limit control mode
      // no reply
      byte rplArr7[6] = {0x7E, 0x07, 0x01, 0xB9,0x94, 0x7E};
  // 8 - get temperature
      // int32_t
      byte rplArr8[10] = {0x7E, 0x08, 0x01, 0x9C,0xFF,0xFF,0xFF, 0xC2,0xF2, 0x7E};
  // 9 - get telemetry
      // lots of stuff
      // byte rplArr9[6] = {0x7E,0x09,0x01,crc,crc,0x7E};
  // 10 - ping
      // no reply
      byte rplArr10[6] = {0x7E, 0x0A, 0x01, 0xE5,0xE2, 0x7E};
  // 11 - get system information
      // lots of stuff
      // byte rplArr9[6] = {0x7E,0x0B,0x01,crc,crc,0x7E};

      
  switch(id) {
    case 1 :         
      rplLen = sizeof(rplArr1);
      memcpy(rplArr, rplArr1, rplLen);
      break;

    case 2 :      
      rplLen = sizeof(rplArr2);
      memcpy(rplArr, rplArr2, rplLen);
      break;

    case 3 :      
      rplLen = sizeof(rplArr3);
      memcpy(rplArr, rplArr3, rplLen);
      break;

   case 4 :         
      rplLen = sizeof(rplArr4);
      memcpy(rplArr, rplArr4, rplLen);
      break;

   case 5 :       
      rplLen = sizeof(rplArr5);
      memcpy(rplArr, rplArr5, rplLen);
      break;

   case 6 :         
      rplLen = sizeof(rplArr6);
      memcpy(rplArr, rplArr6, rplLen);
      break;

   case 7 :         
      rplLen = sizeof(rplArr7);
      memcpy(rplArr, rplArr7, rplLen);
      break;

   case 8 :         
      rplLen = sizeof(rplArr8);
      memcpy(rplArr, rplArr8, rplLen);
      break;

  /* case 9 :        
      rplLen = sizeof(rplArr9);
      memcpy(rplArr, rplArr9, rplLen);
      break;*/

   case 10 :   
      rplLen = sizeof(rplArr10);
      memcpy(rplArr, rplArr10, rplLen);
      break;

  /* case 11 :
      rplLen = sizeof(rplArr11);
      memcpy(rplArr, rplArr11, rplLen);
      break;*/

  }
}
