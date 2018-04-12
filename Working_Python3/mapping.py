# mapping.py

def linearMap( x, in_min, in_max, out_min, out_max ):
    mappedValue = (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min
    return round(mappedValue,2)


def exponentialMap2( x, in_min, in_max, out_min, out_max ):
    inputRange = in_max - in_min
    # print("inputRange = " + str(inputRange) )

    adjustor = (inputRange * inputRange) / float(abs(out_max-out_min)) 
    # print("adjustor = " + str(adjustor))  
    print("\tx = " + str(x))
    x = x - in_min 
    print("\tx_diff = " + str(x))
    x_squared = x * x 
    print("\tx_squared / adjustor = " + str(x_squared / adjustor))    
    mappedValue = (x_squared / adjustor)
    
    return mappedValue
    # return round(mappedValue,2)    



def exponentialMap( x, in_min, in_max, out_min, out_max ):
    mappedValue = ((x - in_min)**2) * (out_max - out_min) / ((in_max - in_min)**2) + out_min
    return round(mappedValue,2)















def run():
    while(True):
        userInput = float(input("input value: "))
        linMap = userInput
        expMap = userInput

        if(linMap > 32640):
            linMap = linearMap(linMap, 32641, 64944, 100, 1)
        elif(linMap == 0):
            pass
        else:
            linMap = linearMap(linMap, 1, 32640, -1, -100)
        # print('linMap = ' + str(linMap))
        # ------------------------------------------------------------------

        # USE THIS CODE -> Replace linear mapping with this exponential mapping.
        if(expMap > 32640):
            expMap = exponentialMap(expMap, 64944, 32641, 1, 100)
        elif(expMap == 0):
            pass
        else:
            expMap = exponentialMap(expMap, 1, 32640, -1, -100)

        print('userInput = ' + str(userInput) +
              '\tlinMap = ' + str(linMap) +
              '\texpMap = ' + str(expMap))
        # -------------------------------------------------------------------


if __name__=='__main__':
    run() 











