"""
test code for motor class

solenero.tech@gmail.com
solenerotech.wordpress.com


this test is done using:
    ESC: turnigy plush30
    Motor: turnigy D2830 1000kv
Different HW can have different behaviour.
Read hw manuals for details.
See blog for esc wiring.

Runing this code the motor will move.
FIX THE MOTOR TIGHT.
Do not mont the props until you are confident.


This program is free software: you can redistribute it and/or modify
it under the terms of the version 3 GNU General Public License as
published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

#solenerotech 2013.09.06

#solenerotech 2014.04.23
#finalized motor_test
#added argparser

"""

import argparse
from motor import motor

initEsc = False
gpio = 0
parser = argparse.ArgumentParser()
parser.add_argument("gpio",type = int, help = 'define gpio: 18-23-24-25  pin:12-16-18-22')
parser.add_argument('-i', dest = 'initEsc', action = 'store_true',help = 'Initialize ESC')
args = parser.parse_args()
initEsc = args.initEsc
gpio = args.gpio


print ('gpio: '+str(gpio))
print ('initEsc: '+str(initEsc))

mymotor = motor('m1', gpio, simulation=False)
#where 18 is  GPIO18 = pin 12
#GPIO23 = pin 16
#GPIO24 = pin 18
#GPIO25 = pin 22


print('***Press ENTER to start')
res = raw_input()
mymotor.start()

#TODO the next line code is necessary to INITIALIZE the ESC to a desired MAX PWM
#I suggest to run this line at least once, for each esc
#in order to obtain the same behaviour in all the ESCs
#use arg -i to  use this line
if initEsc:
    print('***Disconnect ESC power')
    print('***then press ENTER')
    res = raw_input()
    mymotor.setW(100)
    print('***Connect ESC Power')
    print('***Wait beep-beep')

    print('***then press ENTER')
    res = raw_input()


#NOTE:the angular motor speed W can vary from 0 (min) to 100 (max)
#the scaling to pwm is done inside motor class

mymotor.setW(0)
print('***Wait N beeps - one for each battery cell')
print('***Wait beeeeeep for ready')
print('***then press ENTER')
res = raw_input()
print ('increase > a | decrease > z | save Wh > n | set Wh > h|quit > 9')

cycling = True
try:
    while cycling:
        res = raw_input()
        if res == 'a':
            mymotor.setW(mymotor.getW() + 1)
        if res == 'z':
            mymotor.setW(mymotor.getW() - 1)
        if res == 'n':
            mymotor.saveWh()
        if res == 'h':
            mymotor.setWh()
        if res == '9':
            cycling = False
finally:
    # shut down cleanly
    mymotor.stop()
    print ("well done!")




