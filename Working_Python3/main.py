import gamepad15
import threading
##import sensor code

##GPIO setup


class myThread (threading.Thread):
    def __init__(self, threadID, name):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
    def run(self):
        print("Starting" + self.name)

switch_thread = myThread(1, "switch_thread")


def run_wheelchair(threadName):
    while(True):
        # controller mode
        if (switch == 1):
            gamepad15.run()
            # sensor mode
        elif (switch == 0):
            #run sensor code

        #if emergency stop
        #switch_thread.exit()

switch_thread.start()
        

