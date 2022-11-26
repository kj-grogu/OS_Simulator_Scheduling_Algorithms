import random
import threading
from time import sleep



class MyProcess(threading.Thread):
    name = ""
    id = 0
    ioProcessingLag = 0
    cursor = ""
    lag = 0.05
    shutdown = False

    def __init__(self, id, name, ui, callback=lambda: None):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.ui = ui
        self.callback = callback
        self.shutdown =False
        # self.ioProcessingLag = random.randrange(500,1000)

    def run(self):
        inputFile = open('./io/ioinput.log', 'r')
        for i in range(30):
            bid = "p{0}_timeline_{1}".format(self.id, i)
            print(f"Process:{self.id} got button : {bid}")
            button = getattr(self.ui, bid)
            button.setStyleSheet("background-color : green")

            if self.shutdown == True:
                break
            sleep(self.lag)
        inputFile.close()
        self.callback(id)
    def kill(self):
        self.shutdown = True
