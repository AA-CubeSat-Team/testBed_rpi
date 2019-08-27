#hall_test.py

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library
import time
def EventHandler(pin):
    num += 1


GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set GPIO6 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(6, GPIO.RISING)
GPIO.add_event_callback(6,EventHandler,10)
num = 0
while True:
    print("I'm alive!")#This
    print("num is ", num)
    time.sleep(2)
GPIO.cleanup() # Clean up
