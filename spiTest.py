# spiTest.py

import time
import spidev

bus = 0
device = 0      # slave select pin

spi = spidev.SpiDev()       # enables spi, creates "spi" object

spi.open(bus, device)       # opens connection on specified bus, device

spi.max_speed_hz = 250000   # sets master freq at 250 kHz, must be (150:300) kHz for RWA
spi.mode = 0

while True:
    msg = [0x03, 0x05]
    rpl = spi.xfer2(msg)
    print(rpl)
    time.sleep(2)




