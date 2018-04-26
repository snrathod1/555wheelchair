import gamepad15
import threading
import serial
import motor
##import sensor code
flag = True



def readSensors():

    s=serial.Serial('/dev/ttyUSB0',9600)

    while True:
        line = s.readline()
        leftSpeed,rightSpeed = line.split(',')
        leftSpeed = int(leftSpeed)
        rightSpeed = int(rightSpeed)
        motor.setLeftGlobals(leftSpeed)
        motor.setRightGlobals(rightSpeed)

    s.close()



# Main Functionality that switches between threads
def run_wheelchair():
        global flag
        #print('before')
        sensorThread  = threading.Thread(target=readSensors)
        #print('middle')
        gamepadThread = threading.Thread(target=gamepad15.run)
        


       # print(flag)
        while(True):
            if (flag):  # controller mode
                #print("inside if(flag)")
                try:
                    sensorThread._stop()
                    gamepadThread.start()
                except RuntimeError:
                    continue
            else:       # sensor code
                try:
                    gamepadThread._stop()
                    sensorThread.start()
                except RuntimeError:
                    continue

# Begin Main

run_wheelchair()        



    
