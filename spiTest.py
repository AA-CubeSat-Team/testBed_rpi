# spiTest.py


# INIT --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# SPI INITIALIZATION
import time
import spidev

bus = 0
device = 0      # slave select pin

spi = spidev.SpiDev()       # enables spi, creates "spi" object

spi.open(bus, device)       # opens connection on specified bus, device

spi.max_speed_hz = 250000   # sets master freq at 250 kHz, must be (150:300) kHz for RWA
spi.mode = 0                # sets SPI mode to 0 (look up online)

# CSV INITIALIZATION
import csv 

global qq
qq = 0
global xx
xx = 0

header = ["entry", "time", "xfer", "mode", "byte1", "byte2", "byte3", "byte4"]        

global fileName
#fileEnd = input("enter a file name: spiLog_")
#fileName = 'spiLog_' + fileEnd + '.csv'
fileName = 'output.csv'

file = open(fileName, 'w', newline ='')         # open(..'w'..) creates new CSV file
with file:   
    write = csv.writer(file) 
    write.writerow(header) 

# CRC FUNCTION
crcTable = [0x0000,0x1021,0x2042,0x3063,0x4084,0x50a5,0x60c6,0x70e7, 
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
            0x6e17,0x7e36,0x4e55,0x5e74,0x2e93,0x3eb2,0x0ed1,0x1ef0];

def crcAppend(payloadArr1):
    crcValue = 0xFFFF
    for iterByte in payloadArr1:                          
        crcValue = (crcValue << 8) ^ crcTable[((crcValue >> 8) ^ iterByte) & 0x00FF];
        crcValue = ((1 << 16) - 1)  &  crcValue;
    crcSplit = [crcValue >> 8, crcValue & 0x00FF]
    payloadArrCRC = flatList([payloadArr1,crcSplit])
    return payloadArrCRC

# LIST FLATTENING TOOL
import collections
def flatList(x):
    if isinstance(x, collections.Iterable):
        return [a for i in x for a in flatList(i)]
    else:
        return [x]

# FLAG/ESCAPE XOR FUNCTION
def xorFunc(arr, mode):
    arrInp = arr[:]
    if mode == "reqMode":
        idxList = [i for i, val in enumerate(arrInp) if val == 0x7d]

        for idx in idxList:
            arrInp[idx] = [0x7d, arr[idx]^0x20]
            
        arrInp  = flatList(arrInp) 

        idxList = [i for i, val in enumerate(arrInp) if val == 0x7e]
        idxList.pop(-1)
        idxList.pop(0)

        for idx in idxList:
            arrInp[idx] = [0x7d, arrInp[idx]^0x20]
            
        arrXOR = flatList(arrInp) 
        return(arrXOR)

    if mode == "rplMode":
        idxList = [i for i, val in enumerate(arrInp) if val == 0x7d]

        for idx in idxList:
            arrInp[idx+1] = arrInp[idx+1]^0x20

        idxList.reverse()
        for idx in idxList:
            arrInp.pop(idx)

        arrTrue = arrInp
        return(arrTrue)

# CSV FUNCTION
def csvAdd(arr, mode):
    global qq
    global xx
    global data
    global src
    global fileName

    qq = qq + 1
    ts1 = time.gmtime()
    time1 = time.strftime("%H:%M:%S %Z", ts1)
    
    if mode == "reqMode":
        arr.pop(0)
        arr.pop(-1)
        data = arr
        src = "req"
        xx = xx + 1

    if mode == "rplMode":
        arr.pop(0)
        arr.pop(0)
        arr.pop(-1)
        data = arr
        src = "rpl"

    row1_ll = [[qq], [time1], [xx], [src], data]
    row1  = flatList(row1_ll)      

    file = open(fileName, 'a', newline ='')      # open(..'a'..) appends existing CSV file
    with file:   
        write = csv.writer(file) 
        write.writerow(row1)  

# SPI FUNCTION
def spiFunc(reqArr1,rplN1):
    msrEmpArr = [0x7e] * (2*rplN1 + 3) 

    reqArrH = flatList([0x7e, reqArr1, 0x7e]) 
    reqArrX = xorFunc(reqArrH, "reqMode")

    slvEmpArr = spi.xfer2(reqArrX)

    time.sleep(0.100)                           # waits 100 ms for RWA to process
       
    rplArrX = spi.xfer2(msrEmpArr)

    rplArrH = xorFunc(rplArrX, "rplMode")    
    rplArr1 = rplArrH[(0+2):(rplN1+2)] 
       

    slvCRC = [rplArr[-2],rplArr[-1]]

    rplArrCorr = crcAppend(rplArr[0:(rplN1-2)])
    corrCRC = [rplArrCorr[-2],rplArrCorr[-1]]

    if slvCRC == corrCRC:
        print("REPLY CRC CONFIRM")
    if slvCRC != corrCRC:
        print("REPLY CRC ERROR")

    return rplArr1   
    

# MAIN --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
while True: 

##- Input to Request Payload --- --- ---
    comID = input("enter a command ID:\n")
    comID = int(comID)
    comIDArr = list(bytearray((comID).to_bytes(1, byteorder='little', signed=False)))

    if comID == 1:
        payloadArr = flatList([comIDArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiFunc(reqArr,rplN)

    if comID == 2:
        payloadArr = flatList([comIDArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 1 + 4
        rplArr = spiFunc(reqArr,rplN)

    if comID == 3:
        payloadArr = flatList([comIDArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiFunc(reqArr,rplN)

    if comID == 4:
        payloadArr = flatList([comIDArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 10 + 4
        rplArr = spiFunc(reqArr,rplN)

    if comID == 5:
        payloadArr = flatList([comIDArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiFunc(reqArr,rplN)

    if comID == 6:
        speed = input("enter a speed [-65000:65000, 0.1 RPM]:\n")
        speed = int(speed)
        speedArr = list(bytearray((speed).to_bytes(4, byteorder='little', signed=True)))

        rampTime = input("enter a rampTime [10:10000, ms]:\n")
        rampTime = int(rampTime)
        rampTimeArr = list(bytearray((rampTime).to_bytes(2, byteorder='little', signed=False)))

        payloadArr = flatList([comIDArr, speedArr, rampTimeArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiFunc(reqArr,rplN)

    if comID == 7:
        clcMode = input("enter a current limit control mode [0 - low, 1 - high]:\n")
        clcMode = int(clcMode)
        clcModeArr = list(bytearray((clcMode).to_bytes(1, byteorder='little', signed=False)))

        payloadArr = flatList([comIDArr, clcModeArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiFunc(reqArr,rplN)

    if comID == 8:
        payloadArr = flatList([comIDArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 4 + 4
        rplArr = spiFunc(reqArr,rplN)

    if comID == 9:
        payloadArr = flatList([comIDArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 79 + 4
        rplArr = spiFunc(reqArr,rplN)

    if comID == 10:
        payloadArr = flatList([comIDArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiFunc(reqArr,rplN)

    if comID == 11:
        payloadArr = flatList([comIDArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 20 + 4
        rplArr = spiFunc(reqArr,rplN)






##- Input to Request Payload --- --- ---



    #print("reqArr:", [hex(x) for x in reqArr])
    #print("reqArrH:", [hex(x) for x in reqArrH])
    #print("reqArrX:", [hex(x) for x in reqArrX])
    #print("rplArrX:", [hex(x) for x in rplArrX])
    #print("rplArrH:", [hex(x) for x in rplArrH])
    print("rplArr:", [hex(x) for x in rplArr])


    #csvAdd(reqArrT, "reqMode")
    #csvAdd(reqArrX, "reqMode")
    #csvAdd(rplArrX, "rplMode")
    #csvAdd(rplArrT, "rplMode")


    #output = reqArr
    #print("req:", output)
    #print([hex(x) for x in output])



