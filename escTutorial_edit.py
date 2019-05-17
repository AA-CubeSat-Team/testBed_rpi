#escTutorial_edit.py

import os
import time
os.system ("sudo pigpiod")
time.sleep(1)
import pigpio

ESC=18

pi = pigpio.pi()
pi.set_servo_pulsewidth(ESC, 0)

max_value = 2000 #ESC's max value
min_value = 700 #ESC's min value

print("For first time launch, select calibrate")
print("Type the exact word for the function you want")
print("calibrate OR manual OR control OR arm OR stop")

def manual_drive(): #You will use this function to program your ESC if required
    print("You have selected manual option so give a value between 0 and you max value")    
    while True:
    	inp = input()
    	if inp == "stop":
    		stop()
    		break
    	elif inp == "control":
    		control()
    		break
    	elif inp == "arm":
    		arm()
    		break
    	else:
    		pi.set_servo_pulsewidth(ESC, inp)

 def calibrate():
 	pi.set_servo_pulsewidth(ESC, 0)
 	print("Disconnect the battery and press Enter")
 	inp = input()
 	if inp == "":
 		pi.set_servo_pulsewidth(ESC, max_value)
 		print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
 		inp = input()
 		if inp == "":
 			pi.set_servo_pulsewidth(ESC, min_value)
 			print("Playing special tone")
 			time.sleep(5)
 			pi.set_servo_pulsewidth(ESC, 0)
 			print("Arming ESC now")
 			pi.set_servo_pulsewidth(ESC, min_value)
 			control()

 def control():
 	print("starting motor if its calibrated and armed, if not press x")
 	time.sleep(1)
 	speed = 1500
 	print("q - slow a lot")
 	print("a - slow a little")
 	print("d - speed up a little")
 	print("e - speed up a lot")
 	while True:
 		pi.set_servo_pulsewidth(ESC, speed)
 		inp = input()

 		if inp == "q"
 			speed -= 100
 			print("speed = %d")
 		elif inp == "e"
 			speed += 100
 			print("speed = %d")
 		elif inp == "d"
 			speed += 10
 			print("speed = %d")
 		elif inp == "a"
 			speed += 10
 			print("speed = %d")
 		elif inp == "stop"
 			stop()
 			break
 		elif inp == "manual"
 			manual_drive()
 			break
 		elif inp =="arm"
 			arm()
 			break

 def arm():
 	print"Connect the battery and press Enter"
 	inp = input()
 	if inp == "":
 		pi.set_servo_pulsewidth(ESC, 0)
 		time.sleep(1)
 		pi.set_servo_pulsewidth(ESC, max_value)
 		time.sleep(1)
 		pi.set_servo_pulsewidth(ESC, min_value)
 		time.sleep(1)
 		control()

 def stop():
 	pi.set_servo_pulsewidth(ESC, 0)
 	pi.stop()

 inp == input()
 if inp == "manual":
 	manual_drive()
 elif inp == "calibrate":
 	calibrate()
 elif inp == "arm":
 	arm()
 elif inp == "control":
 	control()
 elif inp == "stop":
 	stop()
 else:
 	print("Restart the program")


