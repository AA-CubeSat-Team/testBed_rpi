import RPi.GPIO as GPIO     	# Importing RPi library to use the GPIO pins
from time import sleep  	# Importing sleep from time library
led_pin = 18            
GPIO.setwarnings(False)			# Initializing the GPIO pin 18 for LED
GPIO.setmode(GPIO.BCM)         	 # We are using the BCM pin numbering
GPIO.setup(led_pin, GPIO.OUT)  	 # Declaring pin 21 as output pin
pwm = GPIO.PWM(led_pin, 100)  
low = "low"
medium = "medium"
high = "high"
party = "party"								 # Created a PWM object
pwm.start(0)                   	 # Started PWM at 0% duty cycle, "off" 
while 1:
	dc = input("Change brightness [low medium high]: ")
	if low in dc:
		pwm.ChangeDutyCycle(20)
		sleep(5)
		pwm.ChangeDutyCycle(0)
	elif medium in dc:
		pwm.ChangeDutyCycle(50)
		sleep(5)
		pwm.ChangeDutyCycle(0)
	elif high in dc:
		pwm.ChangeDutyCycle(100)
		sleep(5)
		pwm.ChangeDutyCycle(0)
	elif party in dc:
		pwm.ChangeDutyCycle(100)
		sleep(1)
		pwm.ChangeDutyCycle(50)
		sleep(1)
		pwm.ChangeDutyCycle(20)
		sleep(1)
		pwm.ChangeDutyCycle(0)
	else: 
		pwm.ChangeDutyCycle(0)

