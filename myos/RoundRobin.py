import random
import threading
from time import sleep


class RoundRobin(threading.Thread):
    def __init__(self, id, name, ui, callback=lambda: None):
        print(f"Constructor of FCFS")
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.ui = ui
        self.callback = callback
        self.shutdown = False
        self.toProcess = len(self.ui.programState.Data)

        self.name = ""
        self.id = 0
        self.ioProcessingLag = 0
        self.lag = 2
        self.shutdown = False
        self.clockTime = -1
        self.queue = []
        self.processedCount = 0
        self.toProcess = 4
        self.processStart = {}
        self.currentProcess = ""
        self.maxTime = 31

        self.statusDict = {}
        self.statusDict["None"] = "background-color:none;"
        self.statusDict["Ready"] = "background-color:yellow;"
        self.statusDict["CPU"] = "background-color:green;"
        self.statusDict["IO"] = "background-color:red;"

    def calculateTimeline(self):
        calculated = {}
        calculated["P1"] = []
        calculated["P2"] = []
        calculated["P3"] = []
        calculated["P4"] = []
        mode = {}
        mode["P1"] = []
        mode["P2"] = []
        mode["P3"] = []
        mode["P4"] = []
        finalTimeLine = {}
        finalTimeLine["P1"] = ["None"] * 31
        finalTimeLine["P2"] = ["None"] * 31
        finalTimeLine["P3"] = ["None"] * 31
        finalTimeLine["P4"] = ["None"] * 31
        data = self.ui.programState.Data

        for i in range(len(data)):
            p = "P{0}".format(i + 1)
            for j in range(len(data[p])):
                if j == 1:
                    continue
                l = len(calculated[p])
                prev = calculated[p][-1] if l > 0 else 0
                calculated[p].append(prev + data[p][j])
        # print(calculated)
        for i in range(len(data)):
            p = "P{0}".format(i + 1)
            arr = ["CPU", "IO"]
            ai = 0
            for j in range(len(calculated[p]) - 1):
                cur = calculated[p][j]
                next = calculated[p][j + 1]
                for k in range(cur, next, 1):
                    mode[p].append(arr[ai])
                ai += 1
                ai = ai % 2
        # print(mode)
        for i in range(len(data)):
            p = "P{0}".format(i + 1)
            start = calculated[p][0]
            end = calculated[p][-1]
            mi = 0
            for j in range(start, end, 1):
                finalTimeLine[p][j] = mode[p][mi]
                mi += 1
        # print(f"final Time Line")
        print(finalTimeLine)
        self.finalTimeline = finalTimeLine


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