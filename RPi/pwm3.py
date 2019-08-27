import RPi.GPIO as GPIO     	# Importing RPi library to use the GPIO pins
from time import sleep  	# Importing sleep from time library
pwm_pin = 18            	# Initializing the GPIO pin 18 for LED
GPIO.setmode(GPIO.BCM)         	 # We are using the BCM pin numbering
GPIO.setup(led_pin, GPIO.OUT)  	 # Declaring pin 21 as output pin
pwm = GPIO.PWM(pwm_pin, 100)   	 # Created a PWM object
pwm.start(0)                   	 # Started PWM at 0% duty cycle, "off"
while 1:
	dc = int(input("Change duty cycle: "))
	pwm.ChangeDutyCycle(dc)