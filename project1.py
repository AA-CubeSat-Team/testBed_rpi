import RPi.GPIO as GPIO     	# Importing RPi library to use the GPIO pins
from time import sleep  	# Importing sleep from time library
led_pin = 18            	# Initializing the GPIO pin 18 for LED
GPIO.setmode(GPIO.BCM)         	 # We are using the BCM pin numbering
GPIO.setup(led_pin, GPIO.OUT)  	 # Declaring pin 21 as output pin
pwm = GPIO.PWM(led_pin, 100)   	 # Created a PWM object
pwm.start(50)                   	 # Started PWM at 0% duty cycle, "off"
sleep(3) 
while 1:
	dc = input("Change brightness [LOW MEDIUM HIGH]: ")
	if dc == LOW
		pwm.ChangeDutyCycle(20)
		sleep(5)
		pwm.ChangeDutyCycle(0)
	elif dc == MEDIUM
		pwm.ChangeDutyCycle(50)
		sleep(5)
		pwm.ChangeDutyCycle(0)
	elif dc == HIGH
		pwm.ChangeDutyCycle(100)
		sleep(5)
		pwm.ChangeDutyCycle(0)
	elif dc == PARTY
		pwm.ChangeDutyCycle(100)
		sleep(1)
		pwm.ChangeDutyCycle(50)
		sleep(1)
		pwm.ChangeDutyCycle(20)
		sleep(1)
	else 
		pwm.ChangeDutyCycle(0)

