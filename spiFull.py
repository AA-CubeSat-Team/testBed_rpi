# spiFull.py


# INIT --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

import time
import spidev
import csv 
import threading
import board
import busio
import adafruit_ina219 


# SPI INITIALIZATION
bus = 0
device = 0      # slave select pin

spi = spidev.SpiDev()       # enables spi, creates "spi" object

spi.open(bus, device)       # opens connection on specified bus, device

spi.max_speed_hz = 250000   # sets master freq at 250 kHz, must be (150:300) kHz for RWA
spi.mode = 0                # sets SPI mode to 0 (look up online)


# INA219 INITIALIZATION
i2c = busio.I2C(board.SCL, board.SDA) 
ina219 = adafruit_ina219.INA219(i2c)


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
    payloadArrCRC = flatList([payloadArr1,crcSplit[1],crcSplit[0]])
    return payloadArrCRC


# CRC CHECK FUNCTION
def autoResults(reqArr1, rplArr1, rplN1):
    slvCRC = [rplArr1[-2],rplArr1[-1]]

    rplArrCorr = crcAppend(rplArr1[0:(rplN1-2)])
    corrCRC = [rplArrCorr[-2],rplArrCorr[-1]]

    checkArr1 = [0, 0]
    if slvCRC == corrCRC:
        checkArr1[0] = 1
    if slvCRC != corrCRC:
        checkArr1[0] = 0

    if rplArr1[1] == 1:
        checkArr1[1] = 1
    if (rplArr1[1] == 0) or (rplArr1[1] != 1):
        checkArr1[1] = 0

    return checkArr1


# CRC CHECK FUNCTION
def userResults(reqArr1, rplArr1, rplN1):
    slvCRC = [rplArr1[-2],rplArr1[-1]]

    rplArrCorr = crcAppend(rplArr1[0:(rplN1-2)])
    corrCRC = [rplArrCorr[-2],rplArrCorr[-1]]

    print("\nreqArr:", [hex(x) for x in reqArr1])
    print("rplArr:", [hex(x) for x in rplArr1])

    if slvCRC == corrCRC:
        print("REPLY CRC: TRUE")
    if slvCRC != corrCRC:
        print("REPLY CRC: FALSE")

    if rplArr1[1] == 1:
        print("EXECUTION: TRUE")
    if (rplArr1[1] == 0) or (rplArr1[1] != 1):
        print("EXECUTION: FALSE")


# LIST FLATTENING TOOL
from collections.abc import Iterable                            
def flatFuncAux(items):
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatFuncAux(x)
        else:
            yield x

def flatList(inpArr1):
    return list(flatFuncAux(inpArr1))


# FLAG/ESCAPE XOR FUNCTION
def xorSwitch(arr, mode):
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


# CSV INITIALIZATION
global fileName2

def csvStart(fileName1, header1):
    global qq
    qq = 0

    file = open(fileName1 + '.csv', 'w', newline ='')         # open(..'w'..) creates new CSV file
    with file:   
        write = csv.writer(file) 
        write.writerow(header1) 
         

# CSV FUNCTION                                              
global time0

def csvAdd(fileName1, outputArr1):
    global qq
    global time0

    qq = qq + 1
    timeGMT1 = time.strftime("%H:%M:%S %Z", time.gmtime())
    timeELA1 = time.time() - time0
    timeELA1 = round(timeELA1, 3)

    row1 = flatList([qq, timeGMT1, timeELA1, outputArr1])         

    file = open(fileName1 + '.csv', 'a', newline ='')      # open(..'a'..) appends existing CSV file
    with file:   
        write = csv.writer(file) 
        write.writerow(row1)  


# SPI FUNCTION
global spiAvail
spiAvail = True

def spiTransfer(reqArr1,rplN1):
    global spiAvail
    spiAvail = False

    msrEmpArr = [0x7e] * (2*rplN1 + 3) 

    reqArrH = flatList([0x7e, reqArr1, 0x7e]) 
    reqArrX = xorSwitch(reqArrH, "reqMode")               
 
    slvEmpArr = spi.xfer2(reqArrX)

    time.sleep(0.100)                           # waits 100 ms for RWA to process
       
    rplArrX = spi.xfer2(msrEmpArr)

    rplArrH = xorSwitch(rplArrX, "rplMode")   
    rplArr1 = rplArrH[(0+2):(rplN1+2)] 

    spiAvail = True
    return rplArr1 


def spiWait():
    global spiAvail

    while True:
        if spiAvail == True:
            return
        if spiAvail == False:
            continue
    return


global runSensors
global samplePeriod


def pullSensors():             
    global runSensors
    global samplePeriod
    global fileName2
    global lastResetStatus2
    global nominalState

    while True:
        if runSensors == 0:
            continue

        if runSensors == 1:
            rwStatusArr = processAuto(4, 0, 0)
            lastResetStatusArr = processAuto(2, 0, 0)
            rwState2 = rwStatusArr[4]
            lastResetStatus2 = lastResetStatusArr[2]

            if rwState2 == 0:
                nominalState = False
                fixIssue(1)
            if lastResetStatus2 != 6 and lastResetStatus2 != 7:
                nominalState = False
                fixIssue(2)          

        if runSensors == 2:
            print("sensor pull")
            rwStatusArr = processAuto(4, 0, 0)
            lastResetStatusArr = processAuto(2, 0, 0)
            
            rwState2 = rwStatusArr[4]
            lastResetStatus2 = lastResetStatusArr[2]

            if rwState2 == 0:
                nominalState = False
                fixIssue(1)
            if lastResetStatus2 != 6 and lastResetStatus2 != 7:
                nominalState = False
                fixIssue(2)
            
            # tempArr = processAuto(8, 0, 0)

            voltage = ina219.bus_voltage
            voltage = round(voltage, 3)
            current = ina219.current
            current = round(current, 3)
            power = voltage * current
            power = round(power, 3)
            ina219Arr = [voltage, current, power]

            outputArr2 = flatList([rwStatusArr, ina219Arr])
            csvAdd(fileName2, outputArr2)

        time.sleep(samplePeriod)
        
    return 
pullSensorsThr = threading.Thread(target = pullSensors)


global nominalState
nominalState = True

def fixIssue(runIssue):                                     # will need to be adjusted to fit CDH error processes
    global nominalState

    if runIssue == 1:
            print("issue found")
            print("error state")

            processAuto(5, 0, 0)

            rwStatusArr = processAuto(4, 0, 0)
            if rwStatusArr[4] != 0:
                nominalState = True
                print("rw init success")
            if rwStatusArr[4] == 0:
                print("rw init failed")      
            
    if runIssue == 2:
            print("issue found")
            print("last reset status: ", lastResetStatus2)

            processAuto(3, 0, 0)
            print("cleared last reset status")

            gLRS = processAuto(2, 0, 0)
            if gLRS[2] == 6 or gLRS[2] == 7:
                nominalState = True
                print("cleared last reset status")
            if gLRS[2] != 6 and gLRS[2] != 7:
                print("failed to clear last reset status")


# SPI AUTO MECHANISM
def processAuto(comID1,data1,data2):
    spiWait()

    if comID1 == 1:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiTransfer(reqArr,rplN)
        checkArr = autoResults(reqArr, rplArr, rplN)

        outputArr1 = [checkArr[0], checkArr[1]]

    if comID1 == 2:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 1 + 4
        rplArr = spiTransfer(reqArr,rplN)
        checkArr = autoResults(reqArr, rplArr, rplN)

        lastResetStatus = rplArr[2]  

        outputArr1 = [checkArr[0], checkArr[1], rplArr[2]] 

    if comID1 == 3:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiTransfer(reqArr,rplN)
        checkArr = autoResults(reqArr, rplArr, rplN)

        outputArr1 = [checkArr[0], checkArr[1]]

    if comID1 == 4:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 10 + 4
        rplArr = spiTransfer(reqArr,rplN)
        checkArr = autoResults(reqArr, rplArr, rplN)

        currSpeed = int.from_bytes(bytes(bytearray(rplArr[2:6])), byteorder='little', signed=True)
        refSpeed = int.from_bytes(bytes(bytearray(rplArr[6:10])), byteorder='little', signed=True)
        rwState = rplArr[10]
        clcModeS = rplArr[11]

        outputArr1 = [checkArr[0], checkArr[1], currSpeed, refSpeed, rwState, clcModeS]

    if comID1 == 5:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiTransfer(reqArr,rplN)
        checkArr = autoResults(reqArr, rplArr, rplN)

        outputArr1 = [checkArr[0], checkArr[1]]

    if comID1 == 6:
        speed = data1
        speedArr = list(bytearray((speed).to_bytes(4, byteorder='little', signed=True)))

        rampTime = data2
        rampTimeArr = list(bytearray((rampTime).to_bytes(2, byteorder='little', signed=False)))

        payloadArr = flatList([comID1, speedArr, rampTimeArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiTransfer(reqArr,rplN)
        checkArr = autoResults(reqArr, rplArr, rplN)

        outputArr1 = [checkArr[0], checkArr[1]]

    if comID1 == 7:
        clcModeM = data1
        clcModeArr = list(bytearray((clcModeM).to_bytes(1, byteorder='little', signed=False)))

        payloadArr = flatList([comID1, clcModeArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiTransfer(reqArr,rplN)
        checkArr = autoResults(reqArr, rplArr, rplN)

        outputArr1 = [checkArr[0], checkArr[1]]

    if comID1 == 8:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 4 + 4
        rplArr = spiTransfer(reqArr,rplN)
        checkArr = autoResults(reqArr, rplArr, rplN)

        mcuTemp = int.from_bytes(bytes(bytearray(rplArr[2:6])), byteorder='little', signed=True)

        outputArr1 = [checkArr[0], checkArr[1], mcuTemp]

    if comID1 == 9:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 79 + 4
        rplArr = spiTransfer(reqArr,rplN)
        checkArr = autoResults(reqArr, rplArr, rplN)

        lastResetStatus = rplArr[2]
        mcuTemp = int.from_bytes(bytes(bytearray(rplArr[3:7])), byteorder='little', signed=True)
        rwState = rplArr[7]
        rwClcMode = rplArr[8]
        rwCurrSpeed = int.from_bytes(bytes(bytearray(rplArr[9:13])), byteorder='little', signed=True)
        rwRefSpeed = int.from_bytes(bytes(bytearray(rplArr[13:17])), byteorder='little', signed=True)
        numOfInvalidCrcPackets = int.from_bytes(bytes(bytearray(rplArr[17:21])), byteorder='little', signed=False)
        numOfInvalidLenPackets = int.from_bytes(bytes(bytearray(rplArr[21:25])), byteorder='little', signed=False)
        numOfInvalidCmdPackets = int.from_bytes(bytes(bytearray(rplArr[25:29])), byteorder='little', signed=False)
        numOfCmdExecutedRequests = int.from_bytes(bytes(bytearray(rplArr[29:33])), byteorder='little', signed=False)
        numOfCmdReplies = int.from_bytes(bytes(bytearray(rplArr[33:37])), byteorder='little', signed=False)
        uartNumOfBytesWritten = int.from_bytes(bytes(bytearray(rplArr[37:41])), byteorder='little', signed=False)
        uartNumOfBytesRead = int.from_bytes(bytes(bytearray(rplArr[41:45])), byteorder='little', signed=False)
        uartNumOfParityErrors = int.from_bytes(bytes(bytearray(rplArr[45:49])), byteorder='little', signed=False)
        uartNumOfNoiseErrors = int.from_bytes(bytes(bytearray(rplArr[49:53])), byteorder='little', signed=False)
        uartNumOfFrameErrors = int.from_bytes(bytes(bytearray(rplArr[53:57])), byteorder='little', signed=False)
        uartNumOfRegisterOverrunErrors = int.from_bytes(bytes(bytearray(rplArr[57:61])), byteorder='little', signed=False)
        uartTotalNumOfErrors = int.from_bytes(bytes(bytearray(rplArr[61:65])), byteorder='little', signed=False)
        spiNumOfBytesWritten = int.from_bytes(bytes(bytearray(rplArr[65:69])), byteorder='little', signed=False)
        spiNumOfBytesRead = int.from_bytes(bytes(bytearray(rplArr[69:73])), byteorder='little', signed=False)
        spiNumOfRegisterOverrunErrors = int.from_bytes(bytes(bytearray(rplArr[73:77])), byteorder='little', signed=False)
        spiTotalNumOfErrors = int.from_bytes(bytes(bytearray(rplArr[77:81])), byteorder='little', signed=False)

        outputArrA = [checkArr[0], checkArr[1], lastResetStatus, mcuTemp, rwState, rwClcMode, rwCurrSpeed, rwRefSpeed]
        outputArrB = [numOfInvalidCrcPackets, numOfInvalidLenPackets, numOfInvalidCmdPackets, numOfCmdExecutedRequests, numOfCmdReplies]
        outputArrC = [uartNumOfBytesWritten, uartNumOfBytesRead, uartNumOfParityErrors, uartNumOfNoiseErrors, uartNumOfFrameErrors, uartNumOfRegisterOverrunErrors, uartTotalNumOfErrors]
        outputArrD = [spiNumOfBytesWritten, spiNumOfBytesRead, spiNumOfRegisterOverrunErrors, spiTotalNumOfErrors]

        outputArr1 = flatList([outputArrA, outputArrB, outputArrC, outputArrD])

    if comID1 == 10:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiTransfer(reqArr,rplN)
        checkArr = autoResults(reqArr, rplArr, rplN)

        outputArr1 = [checkArr[0], checkArr[1]]

    if comID1 == 11:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 20 + 4
        rplArr = spiTransfer(reqArr,rplN)
        checkArr = autoResults(reqArr, rplArr, rplN)

        versionMajor = int.from_bytes(bytes(bytearray(rplArr[2:6])), byteorder='little', signed=False)
        versionBuildNumber = int.from_bytes(bytes(bytearray(rplArr[6:10])), byteorder='little', signed=False)      
        uid1 = int.from_bytes(bytes(bytearray(rplArr[10:14])), byteorder='little', signed=False)
        uid2 = int.from_bytes(bytes(bytearray(rplArr[14:18])), byteorder='little', signed=False)
        uid3 = int.from_bytes(bytes(bytearray(rplArr[18:22])), byteorder='little', signed=False)

        outputArr1 = [checkArr[0], checkArr[1], versionMajor, versionBuildNumber, uid1, uid2, uid3]

    return outputArr1


# SPI USER MECHANISM
def processUser(comID1):
    if comID1 == 1:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiTransfer(reqArr,rplN)
        userResults(reqArr, rplArr, rplN)

    if comID1 == 2:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 1 + 4
        rplArr = spiTransfer(reqArr,rplN)
        userResults(reqArr, rplArr, rplN)

        lastResetStatus = rplArr[2]
        print("\nlast reset status: ", lastResetStatus)     

    if comID1 == 3:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiTransfer(reqArr,rplN)
        userResults(reqArr, rplArr, rplN)

    if comID1 == 4:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 10 + 4
        rplArr = spiTransfer(reqArr,rplN)
        userResults(reqArr, rplArr, rplN)

        currSpeed = int.from_bytes(bytes(bytearray(rplArr[2:6])), byteorder='little', signed=True)
        print("\ncurr speed: ", currSpeed)
        refSpeed = int.from_bytes(bytes(bytearray(rplArr[6:10])), byteorder='little', signed=True)
        print("ref speed: ", refSpeed)
        state = rplArr[10]
        print("state: ", state)
        clcModeS = rplArr[11]
        print("clc mode: ", clcModeS)

    if comID1 == 5:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiTransfer(reqArr,rplN)
        userResults(reqArr, rplArr, rplN)

    if comID1 == 6:
        speed = input("enter a speed [-65000:65000, 0.1 RPM]:\n")
        speed = int(speed)
        speedArr = list(bytearray((speed).to_bytes(4, byteorder='little', signed=True)))

        rampTime = input("enter a rampTime [10:10000, ms]:\n")
        rampTime = int(rampTime)
        rampTimeArr = list(bytearray((rampTime).to_bytes(2, byteorder='little', signed=False)))

        payloadArr = flatList([comID1, speedArr, rampTimeArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiTransfer(reqArr,rplN)
        userResults(reqArr, rplArr, rplN)

    if comID1 == 7:
        clcModeM = input("enter a current limit control mode [0 - low, 1 - high]:\n")
        clcModeM = int(clcModeM)
        clcModeArr = list(bytearray((clcModeM).to_bytes(1, byteorder='little', signed=False)))

        payloadArr = flatList([comID1, clcModeArr])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiTransfer(reqArr,rplN)
        userResults(reqArr, rplArr, rplN)

    if comID1 == 8:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 4 + 4
        rplArr = spiTransfer(reqArr,rplN)
        userResults(reqArr, rplArr, rplN)

        mcuTemp = int.from_bytes(bytes(bytearray(rplArr[2:6])), byteorder='little', signed=True)
        print("\nmcu temp: ", mcuTemp)

    if comID1 == 9:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 79 + 4
        rplArr = spiTransfer(reqArr,rplN)
        userResults(reqArr, rplArr, rplN)

        lastResetStatus = rplArr[2]
        print("\nlast reset status: ", lastResetStatus)
        mcuTemp = int.from_bytes(bytes(bytearray(rplArr[3:7])), byteorder='little', signed=True)
        print("mcu temp: ", mcuTemp)
        rwState = rplArr[7]
        print("rw state: ", rwState)
        rwClcMode = rplArr[8]
        print("rw clc mode: ", rwClcMode)
        rwCurrSpeed = int.from_bytes(bytes(bytearray(rplArr[9:13])), byteorder='little', signed=True)
        print("rw curr speed: ", rwCurrSpeed)        
        rwRefSpeed = int.from_bytes(bytes(bytearray(rplArr[13:17])), byteorder='little', signed=True)
        numOfInvalidCrcPackets = int.from_bytes(bytes(bytearray(rplArr[17:21])), byteorder='little', signed=False)
        print("rw ref speed: ", rwRefSpeed) 
        numOfInvalidLenPackets = int.from_bytes(bytes(bytearray(rplArr[21:25])), byteorder='little', signed=False)
        numOfInvalidCmdPackets = int.from_bytes(bytes(bytearray(rplArr[25:29])), byteorder='little', signed=False)
        numOfCmdExecutedRequests = int.from_bytes(bytes(bytearray(rplArr[29:33])), byteorder='little', signed=False)
        numOfCmdReplies = int.from_bytes(bytes(bytearray(rplArr[33:37])), byteorder='little', signed=False)
        uartNumOfBytesWritten = int.from_bytes(bytes(bytearray(rplArr[37:41])), byteorder='little', signed=False)
        uartNumOfBytesRead = int.from_bytes(bytes(bytearray(rplArr[41:45])), byteorder='little', signed=False)
        uartNumOfParityErrors = int.from_bytes(bytes(bytearray(rplArr[45:49])), byteorder='little', signed=False)
        uartNumOfNoiseErrors = int.from_bytes(bytes(bytearray(rplArr[49:53])), byteorder='little', signed=False)
        uartNumOfFrameErrors = int.from_bytes(bytes(bytearray(rplArr[53:57])), byteorder='little', signed=False)
        uartNumOfRegisterOverrunErrors = int.from_bytes(bytes(bytearray(rplArr[57:61])), byteorder='little', signed=False)
        uartTotalNumOfErrors = int.from_bytes(bytes(bytearray(rplArr[61:65])), byteorder='little', signed=False)
        spiNumOfBytesWritten = int.from_bytes(bytes(bytearray(rplArr[65:69])), byteorder='little', signed=False)
        print("num of bytes written: ", spiNumOfBytesWritten) 
        spiNumOfBytesRead = int.from_bytes(bytes(bytearray(rplArr[69:73])), byteorder='little', signed=False)
        print("num of bytes read: ", spiNumOfBytesRead) 
        spiNumOfRegisterOverrunErrors = int.from_bytes(bytes(bytearray(rplArr[73:77])), byteorder='little', signed=False)
        print("num of register overrun errors: ", spiNumOfRegisterOverrunErrors) 
        spiTotalNumOfErrors = int.from_bytes(bytes(bytearray(rplArr[77:81])), byteorder='little', signed=False)
        print("num of total errors: ", spiTotalNumOfErrors) 

    if comID1 == 10:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 0 + 4
        rplArr = spiTransfer(reqArr,rplN)
        userResults(reqArr, rplArr, rplN)

    if comID1 == 11:
        payloadArr = flatList([comID1])
        reqArr = crcAppend(payloadArr)
        
        rplN = 20 + 4
        rplArr = spiTransfer(reqArr,rplN)
        userResults(reqArr, rplArr, rplN)

        versionMajor = int.from_bytes(bytes(bytearray(rplArr[2:6])), byteorder='little', signed=False)
        print("version major: ", versionMajor)
        versionBuildNumber = int.from_bytes(bytes(bytearray(rplArr[6:10])), byteorder='little', signed=False)
        print("version build number: ", versionBuildNumber)
        uid1 = int.from_bytes(bytes(bytearray(rplArr[10:14])), byteorder='little', signed=False)
        print("UID 1: ", uid1)
        uid2 = int.from_bytes(bytes(bytearray(rplArr[14:18])), byteorder='little', signed=False)
        print("UID 2: ", uid2)
        uid3 = int.from_bytes(bytes(bytearray(rplArr[18:22])), byteorder='little', signed=False)
        print("UID 3: ", uid3)

      
    

# MAIN --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
gLRS = processAuto(2, 0, 0)
print("last reset status: ",gLRS[2])
processAuto(3, 0, 0)
print("cleared last reset status")

while True: 
    opMode = input("\nenter an operating mode:\n1 - auto test\n2 - user input\n3 - full manual\n\n")
    opMode = int(opMode)

    if opMode == 1:
        print("\nAUTO TEST OP MODE")
        print("enter '99' to return to op mode select")

        samplePeriod = 1
        runSensors = 0
        pullSensorsThr.start()

        while True: 
            testMode = input("\nenter a test mode:\n1 - manual speed\n2 - step speed\n3 - minimum ramp time\n4 - zero crossing\n")
            testMode = int(testMode)

            if testMode == 99:
                break

            if testMode == 1:
                print("\nMANUAL SPEED TEST MODE\n") 
                nominalState = True

                header = ["entry","timeGMT","timeELA (s)","CRC","exec","currSpeed (0.1 RPM)","refSpeed (0.1 RPM)","state","clcMode"]
                fileName = "manSpeedTest"
                csvStart(fileName, header)
                
                fileName2 = fileName

                time0 = time.time()

                samplePeriod = 0.1
                runSensors = 2

                while True:
                    if nominalState == False:
                        print("nominalState: ", nominalState)
                        break

                    if nominalState == True:
                        speedInp = input("enter a speed [-65000:65000, 0.1 RPM]:\n")
                        speedInp = int(speedInp)
                        processAuto(6,speedInp,0)

                runSensors = 0
                print("test complete")

            if testMode == 2:
                print("\nSTEP SPEED TEST MODE\n")
                nominalState = True

                fileName = "stepSpeedTest"
                header = ["entry","timeGMT","timeELA (s)","CRC","exec","currSpeed (0.1 RPM)","refSpeed (0.1 RPM)","state","clcMode","voltage (V)","current (mA)","power (mW)"]
                csvStart(fileName, header)

                fileName2 = fileName

                time0 = time.time()

                samplePeriod = 0.1
                runSensors = 2

                for speedInp in range(10000, 70000, 5000):
                    if nominalState == False:
                        print("nominalState: ", nominalState)
                        break

                    if nominalState == True:
                        print("speedInp: ", speedInp)
                        processAuto(6, speedInp, 0)
                        time.sleep(1)

                for speedInp in range(65000, 5000, -5000):
                    if nominalState == False:
                        print("nominalState: ", nominalState)
                        break

                    if nominalState == True:
                        print("speedInp: ", speedInp)
                        processAuto(6, speedInp, 0)
                        time.sleep(1)

                runSensors = 0
                print("test complete")
                
            if testMode == 3:
                print("\nMINIMUM RAMP TIME TEST MODE\n")
                nominalState = True

                fileName = "minRampTimeTest"
                header = ["entry","timeGMT","timeELA (s)","CRC","exec","currSpeed (0.1 RPM)","refSpeed (0.1 RPM)","state","clcMode","voltage (V)","current (mA)","power (mW)"]
                csvStart(fileName, header)

                fileName2 = fileName

                time0 = time.time()

                samplePeriod = 0.1
                runSensors = 2

                baseSpeed = 10000

                for inpSpeed in [10500, 12500, 15000, 20000, 30000, 40000, 50000, 60000, 65000]:
                    if nominalState == False:
                        print("nominalState: ", nominalState)
                        break

                    if nominalState == True:
                        processAuto(6, baseSpeed, 0)
                        print("baseSpeed: ", baseSpeed)
                        time.sleep(5)
                        processAuto(6, inpSpeed, 0)
                        print("inpSpeed: ", inpSpeed)
                        time.sleep(5)

                runSensors = 0
                print("test complete")

            if testMode == 4:
                print("\nZERO CROSSING TEST MODE\n")
                nominalState = True

                fileName = "zeroCrossTest"
                header = ["entry","timeGMT","timeELA (s)","CRC","exec","currSpeed (0.1 RPM)","refSpeed (0.1 RPM)","state","clcMode","voltage (V)","current (mA)","power (mW)"]
                csvStart(fileName, header)

                fileName2 = fileName

                time0 = time.time()

                samplePeriod = 0.1
                runSensors = 2

                baseSpeed = 10000

                for rampTime1 in [0, 10, 10**2, 10**3, 10**4]:
                    if nominalState == False:
                        print("nominalState: ", nominalState)
                        break

                    if nominalState == True:
                        processAuto(6, baseSpeed, rampTime1)
                        print("pos baseSpeed: ", baseSpeed)
                        print("ramp time: ", rampTime1)
                        time.sleep((rampTime1*10**-3) + 3)

                        processAuto(6, -1*baseSpeed, rampTime1)
                        print("neg baseSpeed: ", -1*baseSpeed)
                        print("ramp time: ", rampTime1)
                        time.sleep((rampTime1*10**-3) + 3)

                runSensors = 0
                print("test complete")


    if opMode == 2:
        print("\nUSER INPUT OP MODE")
        print("enter '99' to return to mode select")

        while True: 
            comID = input("\nenter a command ID:\n")
            comID = int(comID)

            if comID == 99:
                break

            processUser(comID)
            
            
    if opMode == 3:
        print("\nFULL MANUAL OP MODE")





