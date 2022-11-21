import random
import threading
from time import sleep


class RoundRobin(threading.Thread):
    name = ""
    id = 0
    ioProcessingLag = 0
    lag = 2
    shutdown = False

    def __init__(self, id, name, ui, callback=lambda: None):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.ui = ui
        self.callback = callback
        self.shutdown =False

    def run(self):
        try:
            for i in range(30):
                if self.shutdown == True:
                    break
                for j in range(4):
                    bid = "p{0}_timeline_{1}".format(j+1, i)
                    print(f"FCFS Scheduler got:{self.name} got button : {bid}")

                    # button = getattr(self.ui, bid)
                    button = self.ui.__dict__[bid]
                    button.setStyleSheet("background-color:green;");
                    sleep(0.005)
                    # button.setStyleSheet("background-color : green;")
                sleep(self.lag)
        except Exception as e:
            print(e)
        finally:
            self.kill()
            self.callback(id)


    def kill(self):
        self.shutdown = True