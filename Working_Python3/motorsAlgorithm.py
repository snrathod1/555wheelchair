import math

def mixing(throttle, turn):
    # throttle and turn are values from -100 to +100

    k = 1.00  
    highestVal = 1.0

    # Set baseline speed using throttle (left-stick, Y-axis)
    lTemp = abs(float(throttle))
    rTemp = abs(float(throttle))
    # print '(1)', 'lTemp = ', lTemp, '  rTemp = ', rTemp
    
    # Add steering (right-stick, X-axis)
    if   turn < 0:   # Going left
        rTemp += abs(turn)
    elif turn > 0:   # Going right
        lTemp += abs(turn)
    else:
        pass         # Going straight, so no turning added to either motor
    # print '(2)', 'lTemp = ', lTemp, '  rTemp = ', rTemp
    
    # If any result exceeds 100%, adjust k so the result = 100%,
    #    and use the same k value for the other motor too.
    if (rTemp > 100) or (lTemp > 100):
        highestVal = max(lTemp, rTemp)
        # print 'highestVal = ', highestVal
        k = 100.0/highestVal
        # print 'k = ', k
        lTemp *= k
        rTemp *= k
        # print '(3)', 'lTemp = ', lTemp, '  rTemp = ', rTemp
    
    if throttle < 0:
        lTemp = -abs(lTemp)
        rTemp = -abs(rTemp)

    return lTemp, rTemp

def printDiagnostics(IP_Addr, PortNum, Line, Tank, leftMotor, rightMotor, LightEnabled,color):
    print(('\n' * 100))
    print(('*'  * 60))
    IP_temp = '*****       IP Address:  ' + IP_Addr + '  '
    while len(IP_temp) < 55:
        IP_temp = IP_temp + ' '
    IP_temp = IP_temp + '*****'
    PN_temp = '*****      Port Number:  ' + str(PortNum) + '  '
    while len(PN_temp) < 55:
        PN_temp = PN_temp + ' '
    PN_temp = PN_temp + '*****'
    print(IP_temp)
    print(PN_temp)
    print(('*'  * 60) + '\n')

    print('   Line-Following: ')
    print(('\tYES' if (Line) else '\tNO'))
    print('   Steering: ')
    print(('\t\tTANK STYLE' if (Tank) else '\t\tTHROTTLE & TURN'))
    print('   Light Enabled: ')
    print(('\tYES' if (LightEnabled) else '\tNO'))
    print('   Light Color: ')
    print(('\tOFF' if color==0 else '\tRED' if color==1 else '\tGREEN' if color==2 else '\tBLUE' if color==3 else '\tWHITE'))
    print('')
    print('   Left Motor: ', round(leftMotor,2), '\tRight Motor: ', round(rightMotor,2))
    print(('*'  * 60) + '\n')
    return
    


# 
# Main loop
# while True:
# 
#     throttle = input('throttle = ')
#     turn = input('turn = ')
#     left, right = mixing(throttle, turn)
#     print '\t', 'Left = ', left, 'Right = ', right, '\n\n'
# 





# https://electronics.stackexchange.com/questions/19669/algorithm-for-mixing-2-axis-analog-input-to-control-a-differential-motor-drive/19702
