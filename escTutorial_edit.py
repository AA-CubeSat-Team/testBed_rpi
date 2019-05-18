#escTutorial_edit.py


import os
import time
os.system ("killall pigpiod")
os.system ("sudo pigpiod")
time.sleep(1)
import pigpio

ESC=18

gpio = pigpio.pi()
gpio.set_servo_pulsewidth(ESC, 0)

max_value = 1950 #ESC's max value
min_value = 1000 #ESC's min value

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
            gpio.set_servo_pulsewidth(ESC, inp)
            time.sleep(10)
            print("done")

def calibrate():
    gpio.set_servo_pulsewidth(ESC, 0)
    print("Disconnect the battery and press Enter")
    inp = input()
    if inp == "":
        gpio.set_servo_pulsewidth(ESC, max_value)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = input()
        if inp == "":
            gpio.set_servo_pulsewidth(ESC, min_value)
            print("Playing special tone")
            time.sleep(5)
            gpio.set_servo_pulsewidth(ESC, 0)
            print("Arming ESC now")
            gpio.set_servo_pulsewidth(ESC, min_value)
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
        gpio.set_servo_pulsewidth(ESC, speed)
        time.sleep(10)
        print("done")
        inp = input()

        if inp == "q":
            speed -= 100
            print("speed = " + string(speed))
        elif inp == "e":
            speed += 100
            print("speed = " + string(speed))
        elif inp == "d":
            speed += 10
            print("speed = " + string(speed))
        elif inp == "a":
            speed += 10
            print("speed = " + string(speed))
        elif inp == "stop":
            stop()
            break
        elif inp == "manual":
            manual_drive()
            break
        elif inp =="arm":
            arm()
            break

def arm():
    print("Connect the battery and press Enter")
    inp = input()
    if inp == "":
        gpio.set_servo_pulsewidth(ESC, 0)
        time.sleep(1)
        gpio.set_servo_pulsewidth(ESC, max_value)
        time.sleep(1)
        gpio.set_servo_pulsewidth(ESC, min_value)
        time.sleep(1)
        control()

def stop():
    gpio.set_servo_pulsewidth(ESC, 0)
    gpio.stop()

inp = input()
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


