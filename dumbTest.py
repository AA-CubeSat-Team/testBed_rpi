
import time
import threading

global runSensors
global samplePeriod
global speedInp


def pullSensors():              # runs in the background, but needs main inputs for .csv
    global runSensors
    global samplePeriod
    global speedInp

    speedInp = 0
    while True:
        if runSensors == 1:
            # pull speed via SPI, processAuto function
            # pull power via I2C
            # add to .csv
            print(speedInp, 'sensors pulled')
            time.sleep(samplePeriod)
        if runSensors == 0:
            print("not pulling sensors")
            time.sleep(samplePeriod)
pullSensorsThr = threading.Thread(target = pullSensors)





runSensors = 1
samplePeriod = 0.5
pullSensorsThr.start()

while True:
    global speedInp

    speedInp = input('enter a speed\n')

    if speedInp == "b":
        runSensors = 0
        break

    speedInp = int(speedInp)

    print('speed: ', speedInp)


print("end of script")

time.sleep(5)
runSensors = 1

# threads runSensorsseparately, uses global flags to interact between loops