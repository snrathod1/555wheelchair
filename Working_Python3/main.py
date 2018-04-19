import gamepad15
import threading
import serial
##import sensor code

##GPIO setup


class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print("Starting " + self.name)

switch_thread = myThread(1, "switch_thread")


def run_wheelchair(): #threadName):
    try:
        while(True):
            # controller mode
            if (True):
                gamepad15.run()
                # sensor mode
            else:
                pass
                #run sensor code

            #if emergency stop
            #switch_thread.exit()
    except Exception as ex:
        print(ex)
        print("Quitting...")
        quit()


# Begin Main
switch_thread.start()
run_wheelchair()        

