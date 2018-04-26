# initialize_RPi.GPIO()
import RPi.GPIO as GPIO
import time
import gamepad15
import threading
import serial
import motor
##import sensor code
flag = True


GPIO.setwarnings(False)

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


def my_callback(self):
    global flag
    time.sleep(.1)
    if(GPIO.input(switch_Pin)):
        flag = True
        # print("flag = True")
        sensorThread.start()
        gamepadThread._stop()        
        print("Enabling Self-Driving Mode")
    else:
        flag = False
        # print("flag = False")
        sensorThread._stop()
        gamepadThread.start()
        print("Enabling Joystick Mode")



# Initialize Globals
leftMotorDir  = True             # Let Dir = True  be FORWARD MOTION
leftMotorPWM  = 0                # Let Dir = False be REVERSE MOTION
rightMotorDir = True             # Start with speed set to zero
rightMotorPWM = 0 
#-----------------------------------------------------------------------------------------------------------------
# GND Pins = 6, 9, 14, 20, 25, 30, 34, 39
leftMotorDir_Pin  = 11
leftMotorPWM_Pin  = 12
leftMotorBrk_Pin  = 13
rightMotorDir_Pin = 15
rightMotorPWM_Pin = 16
rightMotorBrk_Pin = 18
switch_Pin        = 19
frequency         = 100 # Hz 

# Declare the Pin Mapping we will use
GPIO.setmode(GPIO.BOARD)

# Set the input/output mode for the Motor Driver Pins 
GPIO.setup(leftMotorDir_Pin,  GPIO.OUT)
GPIO.setup(leftMotorPWM_Pin,  GPIO.OUT)
GPIO.setup(leftMotorBrk_Pin,  GPIO.OUT)

GPIO.setup(rightMotorDir_Pin, GPIO.OUT) 
GPIO.setup(rightMotorPWM_Pin, GPIO.OUT)
GPIO.setup(rightMotorBrk_Pin, GPIO.OUT)

GPIO.setup(switch_Pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(switch_Pin, GPIO.BOTH, callback=my_callback, bouncetime=250)
#callback function should switch between sensor code and control code

# Set Dir pins 
GPIO.output(leftMotorDir_Pin,  GPIO.HIGH)
GPIO.output(rightMotorDir_Pin, GPIO.HIGH) 

# Set PWM pins 
leftMotor  = GPIO.PWM(leftMotorPWM_Pin, frequency)
leftMotor.start(0)  # Initial Duty Cycle
rightMotor = GPIO.PWM(rightMotorPWM_Pin, frequency)
rightMotor.start(0) # Initial Duty Cycle

# Set Brake Pins
GPIO.output(leftMotorBrk_Pin,  GPIO.HIGH)
GPIO.output(rightMotorBrk_Pin, GPIO.HIGH)

#-----------------------------------------------------------------------------------------------------------------
# Done with Initializations.  Create new threads to monitor inputs.  



# Define two functions to set motor speeds
# These functions set the Left and Right Motors based on the GLOBAL Variables 
def setLeftMotor():  
    global leftMotorDir, leftMotorPWM

    if( leftMotorDir ):     # FORWARD MOTION 
        GPIO.output(leftMotorDir_Pin, GPIO.HIGH)  # Set direction 
    else:                   # REVERSE MOTION 
        GPIO.output(leftMotorDir_Pin, GPIO.LOW)   # Set direction 
    
    leftMotor.ChangeDutyCycle(leftMotorPWM*.49)   # Set speed 
    return



def setRightMotor(): 
    global rightMotorDir, rightMotorPWM

    if( rightMotorDir ):    # FORWARD MOTION 
        GPIO.output(rightMotorDir_Pin, GPIO.HIGH) # Set direction 
    else:                   # REVERSE MOTION 
        GPIO.output(rightMotorDir_Pin, GPIO.LOW)  # Set direction 
    
    rightMotor.ChangeDutyCycle(rightMotorPWM*.50) # Set speed 
    return










def setLeftGlobals(leftSpeed):
    global leftMotorDir, leftMotorPWM

    if(leftSpeed < 0):
        leftMotorDir = False  # REVERSE
    else:
        leftMotorDir = True      # FORWARD
    leftMotorPWM = abs(leftSpeed)
    setLeftMotor()
    return


def setRightGlobals(rightSpeed):
    global rightMotorDir, rightMotorPWM

    if(rightSpeed < 0):
        rightMotorDir = False  # REVERSE
    else:
        rightMotorDir = True   # FORWARD
    rightMotorPWM = abs(rightSpeed)
    setRightMotor()
    return




# Main Functionality that switches between threads
def run_wheelchair():
        global flag
        #print('before')
        #sensorThread  = threading.Thread(target=readSensors)
        #print('middle')
        #gamepadThread = threading.Thread(target=gamepad15.run)
        
       # print(flag)
        while(True):
            pass



# Begin Main
sensorThread  = threading.Thread(target=readSensors)
gamepadThread = threading.Thread(target=gamepad15.run)
run_wheelchair() 
