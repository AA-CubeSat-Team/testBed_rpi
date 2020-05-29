# spiTest.py

import time
import spidev

bus = 0
device = 0      # slave select pin

spi = spidev.SpiDev()