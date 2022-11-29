import threading
import traceback
from time import sleep
from myos.ProgramState import ProgramState
from queue import PriorityQueue

class ShortestRemainingTimeFirst(threading.Thread):

    def __init__(self, id, name, ui, callback=lambda: None):
        print(f"Constructor of ShortestRemainingTimeFirst")
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
        self.statusDict["Ready"] = "background-color: rgb(255, 247, 99);"
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
        arrived = {}
        processStart = {}
        processFirstCPU = {}

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

        minHeap = PriorityQueue()

        for t in range(31):
            for pi in range(4): ## check if a process has arrived
                p = "P{0}".format(pi + 1)
                if p in arrived:
                    continue
                if t < processStart[p]:
                    continue;
                else:
                    minHeap.put((requiredCPUTime[p][0], p))
                    arrived[p] = True

            cpuGiven = False

            toProcess = minHeap.qsize()
            if toProcess < 1:
                continue

            iterateQueue = []
            while not minHeap.empty():
                iterateQueue.append(minHeap.get())
            minHeap = PriorityQueue()

            print(f"T : {t}, currentInQueue : {iterateQueue}")

            # for each process at this time unit that has arrived try to update status
            for qi in range(toProcess):
                print(f"Time : {t}, beforeProcessing : {iterateQueue}")
                currentProcess = iterateQueue[qi][1]
                currentMode = mode[currentProcess][0]
                if currentProcess not in processStart:
                    processStart[currentProcess] = t
                if currentMode == "IO":
                    finalTimeLine[currentProcess][t] = "IO"
                    mode[currentProcess].pop(0)
                if currentMode == "CPU":
                    if cpuGiven == False:
                        cpuGiven = True
                        finalTimeLine[currentProcess][t] = "CPU"
                        mode[currentProcess].pop(0)
                        ccp = requiredCPUTime[currentProcess][0]
                        if ccp > 1:
                            requiredCPUTime[currentProcess][0] = ccp - 1
                        else:
                            requiredCPUTime[currentProcess].pop(0)
                        if currentProcess not in processFirstCPU:
                            processFirstCPU[currentProcess] = t
                            self.ui.programState.ResponseTime[currentProcess] = t - processStart[currentProcess]
                    else:
                        finalTimeLine[currentProcess][t] = "Ready"
                        self.ui.programState.WaitTime[currentProcess] += 1
                if len(requiredCPUTime[currentProcess]) > 0:
                    minHeap.put((requiredCPUTime[currentProcess][0], currentProcess))
                else:
                    self.ui.programState.TurnAroundTime[currentProcess] = t - processStart[currentProcess] + 1

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

    def calculateTimelineOLD(self):
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
        requiredCPUTime["P1"] = 0
        requiredCPUTime["P2"] = 0
        requiredCPUTime["P3"] = 0
        requiredCPUTime["P4"] = 0
        processFinished = {}
        processFinished["P1"] = False
        processFinished["P2"] = False
        processFinished["P3"] = False
        processFinished["P4"] = False

        currentProcess = "-None-"
        data = self.ui.programState.Data

        for i in range(len(data)):
            p = "P{0}".format(i + 1)
            for j in range(len(data[p])):
                if j < 2:
                    continue
                requiredCPUTime[p] += data[p][j]

        print(requiredCPUTime)

        for i in range(len(data)):
            p = "P{0}".format(i + 1)
            arrivalTime[p] = data[p][0]

        for i in range(len(data)):
            p = "P{0}".format(i + 1)
            for j in range(len(data[p])):
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

        minHeap = PriorityQueue()
        for t in range(31):
            for j in range(4):
                p = "P{0}".format(j + 1)
                if t >= arrivalTime[p]:
                    if p not in processStart:
                        processStart[p] = t
                        minHeap.put((requiredCPUTime[p], p))
                    if p in processGiven and processGiven[p] >= requiredCPUTime[p] and not processFinished[p]:
                        print(f"Process finished {p}")
                        processFinished[p] = True
                        self.ui.programState.TurnAroundTime[p] = t - processStart[p] # calculate the TurnAroundTime when finishing
                        currentProcess = "-None-"  ## if minHeap.empty() else minHeap.get()[1] # take up the next process
            if currentProcess == "-None-":
                while not minHeap.empty():
                    nextProcess = minHeap.get()[1]
                    if processFinished[nextProcess] == True:
                        continue
                    else:
                        currentProcess = nextProcess
                        self.ui.programState.ResponseTime[currentProcess] = t - processStart[currentProcess] # when changing process update the responseTime
                        break
            if currentProcess == "-None-":
                continue
            if currentProcess not in processGiven:
                processGiven[currentProcess] = 0
            processGiven[currentProcess] += 1
            operation = processQueue[currentProcess].pop(0)
            finalTimeLine[currentProcess][t] = operation

            # mark other processes as ready if they have arrived
            for op in indexes:
                if processFinished[op] == True:
                    continue
                if op not in processStart or currentProcess == op:
                    continue
                finalTimeLine[op][t] = "READY"
                self.ui.programState.WaitTime[op] += 1 # increase the wait time for each ready state

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
                print(f"ShortestRemainingTimeFirst Running clockTime : {self.clockTime}")
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
            print("Some Exception in ShortestRemainingTimeFirst")
            traceback.print_exc()
            print(e)
        finally:
            print("Finally of ShortestRemainingTimeFirst...")
            self.calculateAvgMetrics()
            self.ui.repainting()
            self.kill()
            self.callback(id)
            self.ui.label_5.setText(f" ShortestRemainingTimeFirst Done...")

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
        self.ui.programState.Comparision["ShortestRemainingTimeFirst"] = {}
        self.ui.programState.Comparision["ShortestRemainingTimeFirst"]["AvgTurnAroundTime"] = avgTt
        self.ui.programState.Comparision["ShortestRemainingTimeFirst"]["AvgResponseTime"] = avgRt
        self.ui.programState.Comparision["ShortestRemainingTimeFirst"]["AvgWaitTime"] = avgWt
        self.ui.programState.Comparision["ShortestRemainingTimeFirst"]["Throughput"] = self.throughput


    def kill(self):
        self.shutdown = True