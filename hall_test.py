#hall_test.py

import RPi.GPIO as GPIO # Import Raspberry Pi GPIO library

GPIO.setwarnings(False) # Ignore warning for now
GPIO.setmode(GPIO.BCM)
GPIO.setup(6, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set GPIO6 to be an input pin and set initial value to be pulled low (off)
GPIO.add_event_detect(6, GPIO.RISING)

num = 0
while True:
    if GPIO.event_detected(6):
        num += 1
        print(num)

GPIO.cleanup() # Clean up