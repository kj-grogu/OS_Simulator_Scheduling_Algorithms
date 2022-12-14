import threading
import traceback
from time import sleep
from myos.ProgramState import ProgramState
from queue import PriorityQueue

class ShortestJobFirst(threading.Thread):

    def __init__(self, id, name, ui, callback=lambda: None):
        print(f"Constructor of ShortestJobFirst")
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
        indexes = ["P1", "P2", "P3", "P4"]
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
        arrivalTime = {}
        arrivalTime["P1"] = 0
        arrivalTime["P2"] = 0
        arrivalTime["P3"] = 0
        arrivalTime["P4"] = 0

        priorities = {}  ## startTime, Priority
        processStart = {}
        processGiven = {}
        processQueue = {}

        requiredCPUTime = {}
        requiredCPUTime["P1"] = []
        requiredCPUTime["P2"] = []
        requiredCPUTime["P3"] = []
        requiredCPUTime["P4"] = []

        processFinished = {}
        processFinished["P1"] = False
        processFinished["P2"] = False
        processFinished["P3"] = False
        processFinished["P4"] = False
        arrivedProcess = {}
        processStart = {}
        processFirstCPU = {}
        processFinished = {}

        currentProcess = "-None-"
        data = self.ui.programState.Data

        for t in range(len(data)):
            p = "P{0}".format(t + 1)
            processStart[p] = data[p][0]
            for pi in range(len(data[p])):
                if pi == 1:
                    continue
                l = len(calculated[p])
                prev = calculated[p][-1] if l > 0 else 0
                calculated[p].append(prev + data[p][pi])
        # print(calculated)

        for i in range(len(data)):
            p = "P{0}".format(i + 1)
            for j in range(len(data[p])):
                if j < 2 or j % 2 == 1:
                    continue
                if data[p][j] > 0:
                    requiredCPUTime[p].append(data[p][j])

        print(requiredCPUTime)

        for t in range(len(data)):
            p = "P{0}".format(t + 1)
            arr = ["CPU", "IO"]
            ai = 0
            for pi in range(len(calculated[p]) - 1):
                cur = calculated[p][pi]
                next = calculated[p][pi + 1]
                for k in range(cur, next, 1):
                    mode[p].append(arr[ai])
                ai += 1
                ai = ai % 2
        print("Mode=====")
        print(mode)
        print("Mode=====")

        minProcess = "X"
        minCPU = 10000

        for t in range(31):
            for pi in range(4):  ## check if a process has arrived
                p = "P{0}".format(pi + 1)
                if p in arrivedProcess:
                    continue
                if t < processStart[p]:
                    continue;
                else:
                    print(f"T: {t} New Process Arrived : {p}")
                    arrivedProcess[p] = t

            currentlyInIO = {}
            print(f"T:{t}, arrived Process : {arrivedProcess}")

            if minProcess == 'X' or minProcess in processFinished.keys() or mode[minProcess][0] == 'IO':
                for ap in arrivedProcess.keys():
                    if len(mode[ap]) == 0:
                        continue
                    if mode[ap][0] == 'CPU':
                        val = requiredCPUTime[ap][0]
                        if val < minCPU:
                            minCPU = requiredCPUTime[ap][0]
                            minProcess = ap
                            print(f"minProcess found : {minProcess}")

            print(f"T:{t}, min Process : {minProcess}, requiredCPUTime of minProcess : {requiredCPUTime[minProcess]}")
            for ap in arrivedProcess:
                if ap in processFinished.keys():
                    continue
                if mode[ap][0] == 'IO':
                    finalTimeLine[ap][t] = "IO"
                    mode[ap].pop(0)
                    currentlyInIO[ap] = True
                    continue
                if ap == minProcess:
                    finalTimeLine[ap][t] = "CPU"
                    mode[ap].pop(0)
                    if requiredCPUTime[ap][0] > 1:
                        requiredCPUTime[ap][0] -= 1
                    else:
                        requiredCPUTime[ap].pop(0)
                        if len(requiredCPUTime[ap]) == 0:
                            processFinished[ap] = True
                            self.ui.programState.TurnAroundTime[ap] = t - processStart[ap] + 1
                        minCPU = 10000
                    if ap not in processFirstCPU.keys():
                        processFirstCPU[ap] = t
                        self.ui.programState.ResponseTime[ap] = t - processStart[ap]
                else:
                    finalTimeLine[ap][t] = "READY"
                    self.ui.programState.WaitTime[ap] += 1

        print(finalTimeLine)
        self.finalTimeline = finalTimeLine
        print(f"============================")
        print(self.finalTimeline)
        print(f"============================")

        for t in range(31):
            for k in list(finalTimeLine.keys()):
                if self.throughputStart == -1 and self.finalTimeline[k][t] != "None":
                    self.throughputStart = t
                if self.finalTimeline[k][t] == "None":
                    continue
                self.throughputEnd = t

    def run(self):
        self.calculateTimeline()
        self.clockTime = -1
        try:
            for i in range(31):
                sleep(2)
                self.clockTime += 1
                print(f"ShortestJobFirst Running clockTime : {self.clockTime}")
                if self.processedCount >= 4 or self.shutdown == True:
                    break
                for j in range(len(ProgramState.indexes)):
                    p = ProgramState.indexes[j]
                    ### SET COLOR
                    bid = "{0}_timeline_{1}".format(p.lower(), self.clockTime)
                    button = self.ui.__dict__[bid]
                    status = self.finalTimeline[p][i]
                    style = self.statusDict[status]
                    print(f"Coloring button : {bid}, with style : {style}")
                    # print(f"Process : {p} at {self.clockTime} has  Status : {status} and Style :{style}")
                    button.setStyleSheet(style)
                    sleep(0.05)
                    ### SET COLOR
                ## FOR ENDS
            ## FOR ENDS
        ## TRY ENDS
        except Exception as e:
            print("Some Exception in ShortestJobFirst")
            traceback.print_exc()
            print(e)
        finally:
            print("Finally of ShortestJobFirst...")
            self.calculateAvgMetrics()
            self.ui.repainting()
            self.kill()
            self.callback(id)
            self.ui.label_5.setText(f" ShortestJobFirst Done...")

    def calculateAvgMetrics(self):
        avgTt = 0.0
        avgRt = 0.0
        avgWt = 0.0

        for k in self.ui.programState.TurnAroundTime:
            avgTt +=  self.ui.programState.TurnAroundTime[k]
            avgRt += self.ui.programState.ResponseTime[k]
            avgWt += self.ui.programState.WaitTime[k]

        avgTt = avgTt / 4.0
        avgRt = avgRt / 4.0
        avgWt = avgWt / 4.0
        self.throughput = (self.throughputEnd - self.throughputStart) / 4.0
        self.ui.programState.Comparision["ShortestJobFirst"] = {}
        self.ui.programState.Comparision["ShortestJobFirst"]["AvgTurnAroundTime"] = avgTt
        self.ui.programState.Comparision["ShortestJobFirst"]["AvgResponseTime"] = avgRt
        self.ui.programState.Comparision["ShortestJobFirst"]["AvgWaitTime"] = avgWt
        self.ui.programState.Comparision["ShortestJobFirst"]["Throughput"] = self.throughput


    def kill(self):
        self.shutdown = True