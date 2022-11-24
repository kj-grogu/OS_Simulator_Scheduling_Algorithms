import random
import threading
from time import sleep



class MyProcess(threading.Thread):
    name = ""
    id = 0
    ioProcessingLag = 0
    cursor = ""
<<<<<<< HEAD

    def __init__(self, id, name):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.ioProcessingLag = random.randrange(500,1000)

    def run(self):
        inputFile = open('./io/ioinput.log', 'r')
        for line in inputFile:
            self.cursor = line.strip()
            print("Process ID : {}, Cursor at {}".format(self.id, self.cursor))
            sleep(self.ioProcessingLag / 1000)
        inputFile.close()

    def display(self):
        print("Id : " + str(self.id) + " Name : " + str(self.name) + " Delay : " + str(self.ioProcessingLag) +" ms")
=======
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
>>>>>>> 294e44a8436a41a35f1984f1b0b6c28c41899e04
