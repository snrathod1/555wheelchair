import time
import socket # for sockets
from motorsAlgorithm import mixing, printDiagnostics
import motor
from mapping import exponentialMap

def run():
    # Create Global Variables
    throttle   = 0
    steering   = 0
    leftMotor  = 0
    rightMotor = 0
    color      = 0  # Used for RGB LED Strip -> Red, Green, Blue, White, Off
    IP_Addr    = '192.168.1.72'    # could also use 'localhost'
    PortNum    = 2222

    # Initialize Socket Connection
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    except socket.error:
        print('Failed to create socket.')
        print('Press PS button to Try again.')


    # 0x123456
    control     = 0x000000  # initialize control bytes
    L1          = 0x000001
    L2          = 0x000002
    L3          = 0x000004
    R1          = 0x000008
    R2          = 0x000010
    R3          = 0x000020
    UP          = 0x000040
    DOWN        = 0x000080
    LEFT        = 0x000100
    RIGHT       = 0x000200
    TRIANGLE    = 0x000400
    X           = 0x000800
    SQUARE      = 0x001000
    CIRCLE      = 0x002000
    SELECT      = 0x004000
    START       = 0x008000
    PS          = 0x010000
    LINE        = 0x020000
    TANK        = 0x040000
    LOCK        = 0x080000
    LIGHT       = 0x100000


    # Open the js0 device as if it were a file in read mode.
    pipe = open('/dev/input/js0', 'rb')

    # Create an empty list to store read characters.
    msg = []


    # Map function
    def myMap( x, in_min, in_max, out_min, out_max ):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;



    # Loop forever.
    while True:

        # For each character read from the /dev/input/js0 pipe...
        for char in pipe.read(1):
     
            # append the integer representation of the unicode character read to the msg list.
            msg += [char]
     
            # If the length of the msg list is 8...
            if len(msg) == 8:
                # print(msg)
             # Button event if 6th byte is 1
                if msg[6] == 1:
                    if msg[4]  == 1:  # msg[4] == 1 indicates button is pressed
                        if (msg[7] == 14) and not(control & LOCK):
                            # print 'button', 'X', 'pressed'
                            control |= X
                        elif (msg[7] == 13) and not(control & LOCK):
                            # print 'button', 'Circle', 'pressed'
                            control |= CIRCLE
                        elif (msg[7] == 12): # Don't LOCK the LOCK controls...
                            # print 'button', 'Triangle', 'pressed'
                            control |= TRIANGLE
                        elif (msg[7] == 15) and not(control & LOCK):
                            # print 'button', 'Square', 'pressed'
                            control |= SQUARE
                        elif (msg[7] == 4) and not(control & LOCK):
                            # print 'button', 'Up', 'pressed'
                            control |= UP
                        elif (msg[7] == 5) and not(control & LOCK):
                            # print 'button', 'Right', 'pressed'
                            control |= RIGHT
                        elif (msg[7] == 6) and not(control & LOCK):
                            # print 'button', 'Down', 'pressed'
                            control |= DOWN
                        elif (msg[7] == 7) and not(control & LOCK):
                            # print 'button', 'Left', 'pressed'
                            control |= LEFT
                        elif (msg[7] == 0) and not(control & LOCK):
                            # print 'button', 'Select', 'pressed'
                            control |= SELECT
                        elif (msg[7] == 3) and not(control & LOCK):
                            # print 'button', 'Start', 'pressed'
                            control |= START
                            # print '\tcontrol = ', hex(control)
                        elif (msg[7] == 16) and not(control & LOCK):
                            # print 'button', 'PS Button', 'pressed'
                            control |= PS
                        elif (msg[7] == 1) and not(control & LOCK):
                            # print 'button', 'L3', 'pressed'
                            control |= L3
                        elif (msg[7] == 2) and not(control & LOCK):
                            # print 'button', 'R3', 'pressed'
                            control |= R3
                        elif (msg[7] == 11) and not(control & LOCK):
                            # print 'button', 'R1', 'pressed'
                            control |= R1
                            if (not (control & LINE)):
                                print('\t', 'Pivoting CW')
                                leftMotor  = 50
                                rightMotor = -50
                                print('\t', 'Left Motor = ', leftMotor, '  Right Motor = ', rightMotor, '\n')
                                motor.setLeftGlobals(leftMotor)
                                motor.setRightGlobals(rightMotor)
                        elif (msg[7] == 10) and not(control & LOCK):
                            # print 'button', 'L1', 'pressed'
                            control |= L1
                            if (not (control & LINE)):
                                print('\t', 'Pivoting CCW')
                                leftMotor  = -50
                                rightMotor = 50
                                print('\t', 'Left Motor = ', leftMotor, '  Right Motor = ', rightMotor, '\n')
                                motor.setLeftGlobals(leftMotor)
                                motor.setRightGlobals(rightMotor)
                        elif (msg[7] == 9) and not(control & LOCK):
                            # print 'button', 'R2', 'pressed'
                            control |= R2
                            if (not (control & LINE)):
                                print('\t', 'Pivoting CW')
                                leftMotor  = 100
                                rightMotor = -100
                                print('\t', 'Left Motor = ', leftMotor, '  Right Motor = ', rightMotor, '\n')
                                motor.setLeftGlobals(leftMotor)
                                motor.setRightGlobals(rightMotor)
                        elif (msg[7] == 8) and not(control & LOCK):
                            # print 'button', 'L2', 'pressed'
                            control |= L2
                            if (not (control & LINE)):
                                print('\t', 'Pivoting CCW')
                                leftMotor  = -100
                                rightMotor = 100
                                print('\t', 'Left Motor = ', leftMotor, '  Right Motor = ', rightMotor, '\n')
                                motor.setLeftGlobals(leftMotor)
                                motor.setRightGlobals(rightMotor)
                        else:
                            pass # print 'button', msg[7], 'pressed'

                    else:          # msg[4] == 0 indicates button is released
                        if (msg[7] == 14) and not(control & LOCK):
                            # print 'button', 'X', 'released'
                            control &= ~X
                            control ^= LINE
                            if (control & LINE):
                                print('Line-Following Engaged.')
                            else:
                                print('Line-Following Disengaged.')
                        elif (msg[7] == 13) and not(control & LOCK):
                            # print 'button', 'Circle', 'released'
                            control &= ~CIRCLE
                            printDiagnostics(IP_Addr,PortNum,bool(control & LINE),bool(control & TANK),leftMotor,rightMotor,
                                         bool(control & LIGHT),color)
                        elif (msg[7] == 12): # Don't LOCK the LOCK controls
                            # print 'button', 'Triangle', 'released'
                            control &= ~TRIANGLE
                            control ^= LOCK
                            if (control & LOCK):
                                print('Controller is LOCKED.  Press <TRIANGLE> to unlock.')
                            else:
                                print('Controller is UNLOCKED.  Press <TRIANGLE> to lock.')
                        elif (msg[7] == 15) and not(control & LOCK):
                            # print 'button', 'Square', 'released'
                            control &= ~SQUARE
                            control ^= LIGHT
                            if (control & LIGHT):
                                print('Lights turned ON: ', ('OFF' if color==0 else 'RED' if color==1 else 'GREEN' if color==2
                                                 else 'BLUE' if color==3 else 'WHITE'))
                            else:
                                print('Lights turned OFF')
                        elif (msg[7] == 4) and not(control & LOCK):
                            # print 'button', 'Up', 'released'
                            control &= ~UP
                            if color < 4:
                                color+=1
                            else:
                                color = 0
                            print('COLOR set to:', ('OFF' if color==0 else 'RED' if color==1 else 'GREEN' if color==2
                                         else 'BLUE' if color==3 else 'WHITE'))
                            if (control & LIGHT):
                                print('Lights turned ON: ', ('OFF' if color==0 else 'RED' if color==1 else 'GREEN' if color==2
                                                 else 'BLUE' if color==3 else 'WHITE'))
                        elif (msg[7] == 5) and not(control & LOCK):
                            # print 'button', 'Right', 'released'
                            control &= ~RIGHT
                        elif (msg[7] == 6) and not(control & LOCK):
                            # print 'button', 'Down', 'released'
                            control &= ~DOWN
                            if color > 0:
                                color-=1
                            else:
                                color = 4
                            print('COLOR set to:', ('OFF' if color==0 else 'RED' if color==1 else 'GREEN' if color==2
                                         else 'BLUE' if color==3 else 'WHITE'))
                            if (control & LIGHT):
                                print('Lights turned ON: ', ('OFF' if color==0 else 'RED' if color==1 else 'GREEN' if color==2
                                                 else 'BLUE' if color==3 else 'WHITE'))
                        elif (msg[7] == 7) and not(control & LOCK):
                            # print 'button', 'Left', 'released'
                            control &= ~LEFT
                        elif (msg[7] == 0) and not(control & LOCK):
                            # print 'button', 'Select', 'released'
                            control &= ~SELECT
                            control ^= TANK          # toggle the steering mode: tank style vs throttle/turn
                            if (control & TANK):
                                print('Tank Style Steering Engaged.')
                            else:
                                print('Throttle & Turn Steering Engaged.')
                        elif (msg[7] == 3) and not(control & LOCK):
                            # print 'button', 'Start', 'released'
                            control &= ~START
                            # print '\tcontrol = ', hex(control)
                            # print 'IOT Reset'
                            
                            msg = input('Enter message to send: ')
                            try:
                                # Set the whole string
                                s.sendto(msg, (IP_Addr,PortNum))

                                # Receive data from client (data, addr)
                                # d = s.recvfrom(1024)
                                # reply = d[0]
                                # addr  = d[1]

                                # print 'Server reply: ' + reply

                            except socket.error as msg:
                                print('Error Code: ' + str(msg[0]) + ' Message ' + msg[1])

                        elif (msg[7] == 16) and not(control & LOCK):
                            # print 'button', 'PS Button', 'released'
                            control &= ~PS
                            IP_Addr = input('Enter IP Address: ')    # Could change as the car re-established connections to the network
                            # PortNum = raw_input('Enter Port Number: ')    # Port Number will be set using AT Commands
                            print('Establishing Connection to Port ('+str(PortNum)+') at '+IP_Addr+'\n\n')
                        elif (msg[7] == 1) and not(control & LOCK):
                            # print 'button', 'L3', 'released'
                            control &= ~L3
                        elif (msg[7] == 2) and not(control & LOCK):
                            # print 'button', 'R3', 'released'
                            control &= ~R3
                        elif (msg[7] == 11) and not(control & LOCK):
                            # print 'button', 'R1', 'released'
                            control &= ~R1
                            if (not (control & LINE)):
                                leftMotor  = 0
                                rightMotor = 0
                                print('\t', 'Left Motor = ', leftMotor, '  Right Motor = ', rightMotor, '\n')
                                motor.setLeftGlobals(leftMotor)
                                motor.setRightGlobals(rightMotor)
                        elif (msg[7] == 10) and not(control & LOCK):
                            # print 'button', 'L1', 'released'
                            control &= ~L1
                            if (not (control & LINE)):
                                leftMotor  = 0
                                rightMotor = 0
                                print('\t', 'Left Motor = ', leftMotor, '  Right Motor = ', rightMotor, '\n')
                                motor.setLeftGlobals(leftMotor)
                                motor.setRightGlobals(rightMotor)
                        elif (msg[7] == 9) and not(control & LOCK):
                            # print 'button', 'R2', 'released'
                            control &= ~R2
                            if (not (control & LINE)):
                                leftMotor  = 0
                                rightMotor = 0
                                print('\t', 'Left Motor = ', leftMotor, '  Right Motor = ', rightMotor, '\n')
                                motor.setLeftGlobals(leftMotor)
                                motor.setRightGlobals(rightMotor)
                        elif (msg[7] == 8) and not(control & LOCK):
                            # print 'button', 'L2', 'released'
                            control &= ~L2
                            if (not (control & LINE)):
                                leftMotor  = 0
                                rightMotor = 0
                                print('\t', 'Left Motor = ', leftMotor, '  Right Motor = ', rightMotor, '\n')
                                motor.setLeftGlobals(leftMotor)
                                motor.setRightGlobals(rightMotor)
                        else:
                            pass # print 'button', msg[7], 'released'
                
                # Axis event if 6th byte is 2 ------------------------------------------------------------------------------------------------
                elif msg[6] == 2:
                    if (msg[7] == 0) and not(control & LOCK) and not (control & LINE):        # Left Analog Stick, X-axis
                        pass

                    elif (msg[7] == 1) and not(control & LOCK) and not (control & LINE):    # Left Analog Stick, Y-axis
                        throttle = msg[5]*255+msg[4]
                        if throttle > 32640:
                            throttle = exponentialMap(throttle, 64944, 32641, 1, 100)
                        elif throttle == 0:
                            pass
                        else:
                            throttle = exponentialMap(throttle, 1, 32640, -1, -100)
                        print('throttle = ', throttle)
                        # Send throttle and steering data to mixing function
                        if (control & TANK):
                            leftMotor = throttle
                        else:
                            leftMotor, rightMotor = mixing(throttle, steering)
                        print('\t', 'Left Motor = ', leftMotor, '  Right Motor = ', rightMotor, '\n')
                        motor.setLeftGlobals(leftMotor)
                        motor.setRightGlobals(rightMotor)

                    elif (msg[7] == 2) and (not (control & TANK)) and not(control & LOCK) and not (control & LINE): # Right Analog Stick, X-axis
                        steering = msg[5]*255+msg[4]
                        if steering > 32640:
                            steering = exponentialMap(steering, 64944, 32641, -1, -100)
                        elif steering == 0:
                            pass
                        else:
                            steering = exponentialMap(steering, 336, 32640, 1, 100)
                        print('steering = ', steering)
                        # Send throttle and steering data to mixing function
                        leftMotor, rightMotor = mixing(throttle, steering)
                        print('\t', 'Left Motor = ', leftMotor, '  Right Motor = ', rightMotor, '\n')
                        motor.setLeftGlobals(leftMotor)
                        motor.setRightGlobals(rightMotor)

                    elif (msg[7] == 3) and (control & TANK) and not(control & LOCK) and not (control & LINE):    # Right Analog Stick, Y-axis
                        steering = msg[5]*255+msg[4]
                        if steering > 32640:
                            steering = exponentialMap(steering, 64944, 32641, 1, 100)
                        elif steering == 0:
                            pass
                        else:
                            steering = exponentialMap(steering, 1, 32640, -1, -100)
                        print('steering = ', steering)
                        # Send throttle and steering data to mixing function
                        rightMotor = steering
                        print('\t', 'Left Motor = ', leftMotor, '  Right Motor = ', rightMotor, '\n')  
                        motor.setLeftGlobals(leftMotor)
                        motor.setRightGlobals(rightMotor)                      

                    else:
                        pass # print 'axis', msg[7], msg[5]


                # Reset msg as an empty list.
                msg = []



while(True):
    try:
        run()
    except KeyboardInterrupt:
        print("Quiting...")
        quit()
    except:
        pass



