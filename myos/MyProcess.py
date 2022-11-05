import random
import threading
from time import sleep



class MyProcess(threading.Thread):
    name = ""
    id = 0
    ioProcessingLag = 0
    cursor = ""

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
