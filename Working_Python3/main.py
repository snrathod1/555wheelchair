import gamepad15
import threading
import serial
import time
import flag


def readSensors():

    s=serial.Serial('/dev/ttyUSB0',9600)

    while True:
        while not flag.flag:
            print("in readSensors()")
            line = str(s.readline())
            line = line[2:]
            transmission = line.split('\\')
            #print(transmission)
            leftSpeed,rightSpeed = transmission[0].split(',')
            leftSpeed = float(leftSpeed)
            rightSpeed = float(rightSpeed)
            print(str(leftSpeed) + ", " + str(rightSpeed))
            motor.setLeftGlobals(leftSpeed)
            motor.setRightGlobals(rightSpeed)


            if(flag.flag):
                motor.setLeftGlobals(0)
                motor.setRightGlobals(0)
                print("Turning Motors OFF")


    s.close()




# Begin Main
if __name__ == "__main__":
    import motor

    sensorThread  = threading.Thread(target=readSensors).start()
    gamepadThread = threading.Thread(target=gamepad15.run).start()
