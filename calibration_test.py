#calibration_test.py
import RPi.GPIO as gp
import time

#initialize GPIO settings
gp.setmode(gp.BCM)
gp.setwarnings(False)
gp.setup(18,gp.OUT)

#all units will be in micro seconds
#the presumed frequency of the esc for this test is 500Hz. The duration of one period is 2000
pwm = gp.PWM(18, 500)#sets pin 18 to a 500HZ pwm, referenced as pwm
#MINIMUM PULSE WIDTH = 1000 This results in a duty cycle of 50%
min = 20
#MAXIMUM PULSE WIDTH = 1950 this results in a duty cycle of 97.5%
max = 97.5

#start the pwm with a duty cycle of 0. the power should not be on at this point or should be turned off when prompted

#prompt the user to cut off power from the esc
print("Cut off power from the ESC if it is not already off. Press enter when the power is cut")
inp = raw_input()
pwm.start(max)
print("Turn on power to the ESC and press enter")
inp = raw_input()
if inp == "":
    pwm.ChangeDutyCycle(min)
    print("You should have just heard a beep from the motor.\n this means that that esc has saved and stored its current calibration settings.")

#enter into the eternal while loop to allow for playing around with duty cycles
print("Any duty cycle above 97.5 will be rounded down to 97.5. and below 20 will be rounded to 20")
print("The exit code for the program is: 8051")
while(True):
    inp = input("Enter the next duty cyle you would like to try: ")
    if(inp > max):
        inp = max
    elif(inp < min):
        inp = min
    elif(inp = 0)
        pwm.stop()
    pwm.ChangeDutyCycle(inp)
