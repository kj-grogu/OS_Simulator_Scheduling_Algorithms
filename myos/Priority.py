import threading
import traceback
from time import sleep
from myos.ProgramState import ProgramState
from queue import PriorityQueue
import copy

class Priority(threading.Thread):

    def __init__(self, id, name, ui, callback=lambda: None):
        print(f"Constructor of Priority")
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.ui = ui
        self.callback = callback
        self.shutdown =False
        self.toProcess = len(self.ui.programState.Data)
        self.maxHeap = PriorityQueue()

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
        self.statusDict["READY"] = "background-color:yellow;"
        self.statusDict["CPU"] = "background-color:green;"
        self.statusDict["IO"] = "background-color:red;"

    def calculateTimeline(self):
        # data = {}
        # data["P1"] = [0, 0, 3, 1, 1, 1, 1, 0]
        # data["P2"] = [2, 1, 1, 1, 4, 0, 0, 0]
        # data["P3"] = [3, 2, 2, 1, 2, 0, 0, 0]
        # data["P4"] = [1, 3, 1, 1, 1, 1, 1, 0]
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
        priorities = {}  ## startTime, Priority
        processStart = {}
        processGiven = {}
        processQueue = {}
        data = self.ui.programState.Data

        for i in range(len(data)):
            p = "P{0}".format(i + 1)
            for j in range(len(data[p])):
                if j == 1:
                    priorities[p] = [data[p][0], data[p][1]]
                    continue
                l = len(calculated[p])
                prev = calculated[p][-1] if l > 0 else 0
                calculated[p].append(prev + data[p][j])
                if j > 1:
                    if p not in processQueue:
                        processQueue[p] = []
                    for k in range(data[p][j]):
                        if j % 2 == 0:
                            processQueue[p].append("CPU")
                        else:
                            processQueue[p].append("IO")

        maxHeap = PriorityQueue()
        for t in range(31):
            for j in range(4):
                p = "P{0}".format(j + 1)
                if priorities[p][0] <= t:
                    maxHeap.put((priorities[p][1] * -1, p))
                    if p not in processStart:
                        processStart[p] = t
                    required = calculated[p][6] - calculated[p][0]
                    if p in processGiven and processGiven[p] >= required:
                        self.ui.programState.TurnAroundTime[self.currentProcess] = self.clockTime - processStart[p]
                        print(f"Process finished {p}, {maxHeap.get()}")
            tempQue = copy.copy(maxHeap)
            if tempQue.empty():
                continue
            currentHighest = tempQue.get()[1]

            if currentHighest not in processGiven:
                processGiven[currentHighest] = 0
            processGiven[currentHighest] += 1
            finalTimeLine[currentHighest][t] = processQueue[currentHighest].pop(0)

            while not tempQue.empty():
                op = tempQue.get()[1]
                finalTimeLine[op][t] = "READY"
                self.ui.programState.WaitTime[op] += 1
        print(finalTimeLine)
        self.finalTimeline = finalTimeLine

    def run(self):
        self.calculateTimeline()
        self.queue = []
        self.clockTime = -1
        try:
            for i in range(31):
                sleep(2)
                self.clockTime += 1
                print(f"Priority Running clockTime : {self.clockTime}")
                if self.processedCount >= 4 or self.shutdown == True:
                    break
                for j in range(len(ProgramState.indexes)):
                    p = ProgramState.indexes[j]
                    ### SET COLOR
                    bid = "{0}_timeline_{1}".format(p.lower(), self.clockTime)
                    button = self.ui.__dict__[bid]
                    status = self.finalTimeline[p][i]
                    style = self.statusDict[status]
                    print(f"Process : {p} at {self.clockTime} has  Status : {status} and Style :{style}")
                    button.setStyleSheet(style)
                    sleep(0.05)
                    ### SET COLOR
                ## FOR ENDS
            ## FOR ENDS
        ## TRY ENDS
        except Exception as e:
            print("Some Exception in Priority")
            traceback.print_exc()
            print(e)
        finally:
            print("Finally of Priority...")
            self.calculateAvgMetrics()
            self.ui.repainting()
            self.kill()
            self.callback(id)
            self.ui.label_5.setText(f" Priority Done...")

    def calculateAvgMetrics(self):
        # self.ui.programState.TurnAroundTime["P1"] = 1
        # self.ui.programState.TurnAroundTime["P1"] = 2
        # self.ui.programState.TurnAroundTime["P1"] = 4
        # self.ui.programState.TurnAroundTime["P1"] = 2
        #
        # self.ui.programState.WaitTime["P1"] = 4
        # self.ui.programState.WaitTime["P2"] = 6
        # self.ui.programState.WaitTime["P3"] = 8
        # self.ui.programState.WaitTime["P4"] = 2
        #
        # self.ui.programState.ResponseTime["P1"] = 7
        # self.ui.programState.ResponseTime["P2"] = 8
        # self.ui.programState.ResponseTime["P3"] = 3
        # self.ui.programState.ResponseTime["P4"] = 1

        self.ui.programState.Comparision["Priority"] = {}
        self.ui.programState.Comparision["Priority"]["AvgTurnAroundTime"] = 2
        self.ui.programState.Comparision["Priority"]["AvgResponseTime"] = 3
        self.ui.programState.Comparision["Priority"]["AvgWaitTime"] = 4


    def kill(self):
        self.shutdown = True