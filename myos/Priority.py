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
        self.statusDict["READY"] = "background-color: rgb(255, 247, 99);"
        self.statusDict["CPU"] = "background-color: rgb(152, 235, 52);"
        self.statusDict["IO"] = "background-color:rgb(230, 74, 50);"
        self.throughputStart = -1;
        self.throughputEnd = -1;
        self.throughput = 0;

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
        processFinished = {}
        processFirstCPU = {}

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
                print(f"p : {p}, processStart : {processStart}")
                if priorities[p][0] <= t:
                    maxHeap.put((priorities[p][1] * -1, p))
                    if p not in processStart:
                        processStart[p] = t
                    required = calculated[p][6] - calculated[p][0]
                    if p in processGiven and processGiven[p] >= required:
                        if p not in processFinished:
                            self.ui.programState.TurnAroundTime[p] = t - processStart[p]
                            processFinished[p] = t
                        print(f"Process finished {p}, {maxHeap.get()} at time : {t}, processStart : {processStart}")
            tempQue = copy.copy(maxHeap)
            if tempQue.empty():
                continue
            currentHighest = tempQue.get()[1]

            if currentHighest not in processGiven:
                processGiven[currentHighest] = 0
                processFirstCPU[currentHighest] = t
            processGiven[currentHighest] += 1
            finalTimeLine[currentHighest][t] = processQueue[currentHighest].pop(0)

            while not tempQue.empty():
                op = tempQue.get()[1]
                finalTimeLine[op][t] = "READY"
                self.ui.programState.WaitTime[op] += 1
        print(finalTimeLine)

        ## RESPONSE TIME
        for k in list(processFirstCPU.keys()):
            self.ui.programState.ResponseTime[k] = processFirstCPU[k] - processStart[k]

        self.finalTimeline = finalTimeLine
        for t in range(31):
            for k in list(finalTimeLine.keys()):
                if self.throughputStart == -1 and self.finalTimeline[k][t] != "None":
                    self.throughputStart = t
                if self.finalTimeline[k][t] == "None":
                    continue
                self.throughputEnd = t

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
                    # print(f"Process : {p} at {self.clockTime} has  Status : {status} and Style :{style}")
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
        avgTt = 0.0
        avgRt = 0.0
        avgWt = 0.0

        for k in self.ui.programState.TurnAroundTime:
            avgTt += self.ui.programState.TurnAroundTime[k]
            avgRt += self.ui.programState.ResponseTime[k]
            avgWt += self.ui.programState.WaitTime[k]

        avgTt = avgTt / 4.0
        avgRt = avgRt / 4.0
        avgWt = avgWt / 4.0
        self.throughput = (self.throughputEnd - self.throughputStart) / 4.0

        self.ui.programState.Comparision["Priority"] = {}
        self.ui.programState.Comparision["Priority"]["AvgTurnAroundTime"] = avgTt
        self.ui.programState.Comparision["Priority"]["AvgResponseTime"] = avgRt
        self.ui.programState.Comparision["Priority"]["AvgWaitTime"] = avgWt
        self.ui.programState.Comparision["Priority"]["Throughput"] = self.throughput


    def kill(self):
        self.shutdown = True