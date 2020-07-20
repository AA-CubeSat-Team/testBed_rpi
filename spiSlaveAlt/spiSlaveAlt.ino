#include<SPI.h>  

volatile byte reqArrX[16] = { };
byte reqArrT[16] = { };  
int qq;      
byte rplArrT[16] = { }; 
byte rplArrD[16] = { };
byte rplArrX[16] = { }; 
int rplLenT;
int ee;
int ff;
volatile byte reqB_new;
volatile byte reqB_old;
volatile byte rplB;
volatile byte flag;
volatile byte kk;
volatile byte yy;
volatile byte readReg;

unsigned int crcTable[] = {0x0000,0x1021,0x2042,0x3063,0x4084,0x50a5,0x60c6,0x70e7, 
                            0x8108,0x9129,0xa14a,0xb16b,0xc18c,0xd1ad,0xe1ce,0xf1ef,
                            0x1231,0x0210,0x3273,0x2252,0x52b5,0x4294,0x72f7,0x62d6,
                            0x9339,0x8318,0xb37b,0xa35a,0xd3bd,0xc39c,0xf3ff,0xe3de,
                            0x2462,0x3443,0x0420,0x1401,0x64e6,0x74c7,0x44a4,0x5485,
                            0xa56a,0xb54b,0x8528,0x9509,0xe5ee,0xf5cf,0xc5ac,0xd58d,
                            0x3653,0x2672,0x1611,0x0630,0x76d7,0x66f6,0x5695,0x46b4,
                            0xb75b,0xa77a,0x9719,0x8738,0xf7df,0xe7fe,0xd79d,0xc7bc,   
                            0x48c4,0x58e5,0x6886,0x78a7,0x0840,0x1861,0x2802,0x3823,
                            0xc9cc,0xd9ed,0xe98e,0xf9af,0x8948,0x9969,0xa90a,0xb92b,
                            0x5af5,0x4ad4,0x7ab7,0x6a96,0x1a71,0x0a50,0x3a33,0x2a12,
                            0xdbfd,0xcbdc,0xfbbf,0xeb9e,0x9b79,0x8b58,0xbb3b,0xab1a,
                            0x6ca6,0x7c87,0x4ce4,0x5cc5,0x2c22,0x3c03,0x0c60,0x1c41,
                            0xedae,0xfd8f,0xcdec,0xddcd,0xad2a,0xbd0b,0x8d68,0x9d49,
                            0x7e97,0x6eb6,0x5ed5,0x4ef4,0x3e13,0x2e32,0x1e51,0x0e70,
                            0xff9f,0xefbe,0xdfdd,0xcffc,0xbf1b,0xaf3a,0x9f59,0x8f78,
                            0x9188,0x81a9,0xb1ca,0xa1eb,0xd10c,0xc12d,0xf14e,0xe16f,
                            0x1080,0x00a1,0x30c2,0x20e3,0x5004,0x4025,0x7046,0x6067,
                            0x83b9,0x9398,0xa3fb,0xb3da,0xc33d,0xd31c,0xe37f,0xf35e,
                            0x02b1,0x1290,0x22f3,0x32d2,0x4235,0x5214,0x6277,0x7256,
                            0xb5ea,0xa5cb,0x95a8,0x8589,0xf56e,0xe54f,0xd52c,0xc50d,
                            0x34e2,0x24c3,0x14a0,0x0481,0x7466,0x6447,0x5424,0x4405,
                            0xa7db,0xb7fa,0x8799,0x97b8,0xe75f,0xf77e,0xc71d,0xd73c,
                            0x26d3,0x36f2,0x0691,0x16b0,0x6657,0x7676,0x4615,0x5634,
                            0xd94c,0xc96d,0xf90e,0xe92f,0x99c8,0x89e9,0xb98a,0xa9ab,
                            0x5844,0x4865,0x7806,0x6827,0x18c0,0x08e1,0x3882,0x28a3,
                            0xcb7d,0xdb5c,0xeb3f,0xfb1e,0x8bf9,0x9bd8,0xabbb,0xbb9a,
                            0x4a75,0x5a54,0x6a37,0x7a16,0x0af1,0x1ad0,0x2ab3,0x3a92,
                            0xfd2e,0xed0f,0xdd6c,0xcd4d,0xbdaa,0xad8b,0x9de8,0x8dc9,
                            0x7c26,0x6c07,0x5c64,0x4c45,0x3ca2,0x2c83,0x1ce0,0x0cc1,
                            0xef1f,0xff3e,0xcf5d,0xdf7c,0xaf9b,0xbfba,0x8fd9,0x9ff8,
                            0x6e17,0x7e36,0x4e55,0x5e74,0x2e93,0x3eb2,0x0ed1,0x1ef0};


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
    if (yy < (rplLenT + ee + ff + 1)){
      SPDR = rplArrX[yy];
      yy++;
    }
    if (yy >= (rplLenT + ee + ff + 1)){
      SPDR = 126;
    }
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
    
    genReply(reqArrT[1]);                // need to pass entire array at some point
    yy = 0;
        
    Serial.print("reqX: ");
    for (int jj = 0; jj < sizeof(reqArrX); jj++){
      Serial.print(reqArrX[jj]);
      Serial.print(" ");
      reqArrX[jj] = 0;
    }
    Serial.println();
    Serial.print("reqT: ");
    for (int jj = 0; jj < sizeof(reqArrT); jj++){
      Serial.print(reqArrT[jj]);
      Serial.print(" ");
      reqArrT[jj] = 0;
    }
    Serial.println();
    Serial.print("rplT: ");
    for (int jj = 0; jj < sizeof(rplArrT); jj++){
      Serial.print(rplArrT[jj]);
      Serial.print(" ");
    }
    Serial.println();
    Serial.print("rplX: ");
    for (int jj = 0; jj < sizeof(rplArrX); jj++){
      Serial.print(rplArrX[jj]);
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


void genReply(byte id){                       // want to build XOR functionality into genReply to deliver
  byte rplArr1T[6] = {id,126,125,3};       //    final reply array to SPI interrupt sequence
  byte rplArr2T[6] = {id,126,4,4};
  byte rplArr3T[6] = {id,126,5,5};
  byte rplArr4T[6] = {id,126,6,6};


  for (int jj = 0; jj < sizeof(rplArrT); jj++){
    rplArrT[jj] = 0;
  }
  for (int jj = 0; jj < sizeof(rplArrX); jj++){
    rplArrX[jj] = 0;
  }

      
  switch(id) {
    case 1 :
      memcpy(rplArrT, rplArr1T, sizeof(rplArr1T));
      rplLenT = sizeof(rplArr1T);
      break;
    case 2 :
      memcpy(rplArrT, rplArr2T, sizeof(rplArr2T));
      rplLenT = sizeof(rplArr2T);
      break;
    case 3 :
      memcpy(rplArrT, rplArr3T, sizeof(rplArr3T));
      rplLenT = sizeof(rplArr3T);
      break;
    case 4 :
      memcpy(rplArrT, rplArr4T, sizeof(rplArr4T));
      rplLenT = sizeof(rplArr4T);
      break;
  }                                                 

  unsigned int crcValue = 0xFFFF;
  for (int iterByte = 0; iterByte < sizeof(testArr); iterByte++){ 
    crcValue = ((crcValue << 8) ^ crcTable[((crcValue >> 8) ^ testArr[iterByte]) & 0x00FF]);
  }
  unsigned int crcSplit[] = {crcValue >> 8, crcValue & 0xFF};

  int ss = 0;
  for (int cc = 0; cc < sizeof(testArrCRC); cc++){
    if (cc < sizeof(testArr)){
      testArrCRC[cc] = testArr[cc];
    }
    if (cc >= sizeof(testArr)){
      testArrCRC[cc] = crcSplit[ss];
      ss++;
    }
  }

  
  // know length of rplArrT, don't know length of rplArrX (max = 2*rplLenT)
  // want to start by creating a rplArrT
  // want to end by handing rplArrX to SPI mechanism

  // byte rplArrT[16] = { }; 
  // byte rplArrD[16] = { };
  // byte rplArrX[16] = { };   these lengths never change, rplLenT=6 allows XOR mechanism to find contents within 16

  ee = 0;
  ff = 0;                                                  
  for (int tt = 0; tt < rplLenT; tt++){        
    if (rplArrT[tt] != 125){
      rplArrD[tt+ee] = rplArrT[tt];
    }
    if (rplArrT[tt] == 125){
      rplArrD[tt+ee] = 125;
      rplArrD[tt+ee+1] = rplArrT[tt]^0x20;
      ee++;
    }
  }                                            
  for (int dd = 0; dd < (rplLenT+ee); dd++){
    if ( (dd != 0) || (dd != rplLenT+ee-1) || (rplArrD[dd] != 126) ){
      rplArrX[dd+ff] = rplArrD[dd];
    }
    if ( (dd != 0) && (dd != rplLenT+ee-1) && (rplArrD[dd] == 126) ){   
      rplArrX[dd+ff] = 125;
      rplArrX[dd+ff+1] = rplArrD[dd]^0x20;
      ff++;
    }
  }
  
  // rplArrX is still length 16, but its contents take up rplLenT + ff + ee, rest thru end are zeros
  // since rplArrX length is known at runtime, can use variable int to cut off SPI reply transmission
  // init array lengths can all be as long as you want, because extra elements will be cut off in reply transmission
}
