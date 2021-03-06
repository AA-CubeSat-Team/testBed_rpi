# spiTest.py – MASTER

# INTRO: this scripts primary goals are to assemble the request array for transmission,
#        then receive and store the reply array from the slave

# BKGND: CSV – a .CSV file stands for "Comma Separated Values", it's essentially a very
#        minimal spreadsheet that stores numbers and text in row entries
#        
#        CRC - stands for "Cyclic Redundancy Check", which is a method of checking for errors
#        in data transmissions. the CRC is 2 bytes, and they are calculated with a function 
#        that inputs the request package and outputs the 2 CRC bytes. the RWA will then
#        recalculate the CRC based on the package receives and see if it matches the CRC we sent
#
#        hex – hex is a another number format like decimal or binary, where one byte is 
#        displayed "0xNN". you can read about the numbering scheme online (base-16). some
#        notable numbers are 0x00 = 0, 0x01 = 1, and 0xFF = 255
#       
#        little endian - a method of writing multi-byte numbers where the least significant 
#        byte (LSB) is placed first (to the left), while the most significant byte (MSB) is
#        placed last (to the right). significance refers to the magnitude of number represented
#
#        2's complement – a method of writing negative numbers in binary/hex that's used here 


# INIT --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---

# SPI INITIALIZATION
import time                 # imports raspberry pi/python libraries that provide more functions
import spidev

bus = 0
device = 0      # slave select pin

spi = spidev.SpiDev()       # enables spi, creates "spi" object

spi.open(bus, device)       # opens connection on specified bus, device

spi.max_speed_hz = 250000   # sets master freq at 250 kHz, must be (150:300) kHz for RWA
spi.mode = 0                # sets SPI mode to 0 (look up what this means online)

# CSV INITIALIZATION
import csv 

global qq
qq = 0

header = ['entry', 'time', 'type1', 'type2']        # modify headers to fit data inputs

file = open('output.csv', 'w', newline ='')         # open(..'w'..) creates new CSV file
with file:   
    write = csv.writer(file) 
    write.writerow([header[0], header[1], header[2], header[3]]) 

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

def crcCompute(payload):
    crcValue = 0xFFFF                                                       # generic CRC formula following the "0xFFFF" standard
    for iterbyte in payload:                          
        crcValue = (crcValue << 8) ^ crcTable[((crcValue >> 8) ^ iterbyte) & 0x00FF];
        crcValue = ((1 << 16) - 1)  &  crcValue;
    crcSplit = [crcValue & 0x00FF, crcValue >> 8]
    return crcSplit

# CSV FUNCTION
def csvAdd(rpl):
    global qq
    qq = qq + 1
    ts1 = time.gmtime()
    time1 = time.strftime("%H:%M:%S %Z", ts1)
                                                 
    row1_ll = [[qq], [time1], rpl]
    row1  = [val for sublist in row1_ll for val in sublist]          

    file = open('output.csv', 'a', newline ='')      # open(..'a'..) appends existing CSV file
    with file:   
        write = csv.writer(file) 
        write.writerow([row1[0], row1[1], row1[2], row1[3], row1[4], row1[5]]) 
    

# MAIN --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- --- ---
while True: 
    cmd = 1
    cmdArr = list(bytearray((cmd).to_bytes(1, byteorder='little', signed=True)))      # this is 3 functions stacked in one line
                                                                                      # the 1st function chops integer speed into 4 bytes
    speed = 65000                                                                     # the 2nd function converts the bytes into a byte array
    speedArr = list(bytearray((speed).to_bytes(4, byteorder='little', signed=True)))  # the 3rd function converts the byte array into a list  

    payloadArr = sum([cmdArr, speedArr],[])                 # flattens the command list and speed list into a single payload list
    crcArr = crcCompute(payloadArr)                         # calculates CRC ofthe payload

    reqArr = sum([payloadArr, crcArr],[])                   # attaches the CRC bytes to the end of the request (compare with RWA datasheet)
    
    rplArr = spi.xfer2(reqArr)                              # transfers full request over SPI to the slave, receives reply from slave

    csvAdd(rplArr)                                          # stores each byte of the reply list in a new row of the .CSV file
    
    #req.pop(-1)
    #rpl.pop(0)
    
    print("req:", req)
    print("rpl:", rpl)
    time.sleep(5)

#reqArr = [0x01, 0x02, 0x03, 0x04, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e, 0x7e]          # spare code for testing 
# req (int): [1, 232, 253, 0, 0, 119, 27]
# req (hex): ['0x1', '0xe8', '0xfd', '0x0', '0x0', '0x77', '0x1b']
#print("req:", req)
#print([hex(x) for x in output])

