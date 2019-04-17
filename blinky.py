import RPi.GPIO as gpio
import time
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(18,gpio.OUT)
gpio.output(18,gpio.HIGH)
time.sleep(3)
gpio.output(18,gpio.LOW)
print "done"
