import gamepad15
import threading
import serial
import time
#import motor
##import sensor code
#flag = True
import flag

def setFlag(boolean):
    global flag
    if(boolean):
        flag = True
        print("Flag = " + str(flag))
    else:
        flag = False
        print("Flag = " + str(flag))



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
        #global flag
        #print('before')
        #sensorThread  = threading.Thread(target=readSensors)
        #print('middle')
        #gamepadThread = threading.Thread(target=gamepad15.run)
        


       # print(flag)
        while(True):
            print(flag.flag)
            time.sleep(.2)
            if (flag.flag):  # controller mode
                try:
                    sensorThread._stop()
                    gamepadThread.start()
                    #print("Enabling Joystick Mode")
                except RuntimeError or AssertionError:
                    #print("In 'if except'")                    
                    continue
            else:       # sensor code
                try:
                    gamepadThread._stop()
                    sensorThread.start()
                    #print("Enabling Self-Driving Mode")
                except RuntimeError or AssertionError:
                    #print("In 'else except'")
                    continue

# Begin Main
if __name__ == "__main__":
    import motor

    sensorThread  = threading.Thread(target=readSensors)
    gamepadThread = threading.Thread(target=gamepad15.run)
    run_wheelchair()        



    
