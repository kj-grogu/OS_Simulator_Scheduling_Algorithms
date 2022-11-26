import threading
import traceback
from time import sleep
from myos.ProgramState import ProgramState
from queue import PriorityQueue

class RoundRobin(threading.Thread):

    def __init__(self, id, name, ui, callback=lambda: None):
        print(f"Constructor of RoundRobin")
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

        queue = []
        for t in range(31):
            for j in range(4):
                p = "P{0}".format(j + 1)
                if t >= arrivalTime[p]:
                    if p not in processStart:
                        processStart[p] = t
                        # queue.append(p)
                        queue.insert(0, p)

            if len(queue) < 1:
                continue  # nothing to update at this time continue to next time unit

            print(f"at time : {t} : {queue}")
            currentProcess = queue.pop(0)

            if currentProcess not in processGiven:
                processGiven[currentProcess] = 0
                self.ui.programState.ResponseTime[currentProcess] = t - processStart[currentProcess]
            processGiven[currentProcess] += 1
            requiredCPUTime[currentProcess] -= 1
            finalTimeLine[currentProcess][t] = processQueue[currentProcess].pop(0)
            if len(processQueue[currentProcess]) > 0:
                queue.append(currentProcess)  # push the back the same process later processing if its not finished
            else:
                processFinished[currentProcess] = True
                self.ui.programState.TurnAroundTime[currentProcess] = t - processStart[currentProcess] + 1# calculate the TurnAroundTime when finishing

            # mark other processes as ready if they have arrived
            for op in indexes:
                if processFinished[op] == True:
                    continue
                if op not in processStart or currentProcess == op:
                    continue
                finalTimeLine[op][t] = "READY"
                self.ui.programState.WaitTime[op] += 1  # increase the wait time for each ready state

        self.finalTimeline = finalTimeLine
        print(f"============================")
        print(self.finalTimeline)
        print(self.ui.programState.WaitTime)
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
                print(f"RoundRobin Running clockTime : {self.clockTime}")
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
            print("Some Exception in RoundRobin")
            traceback.print_exc()
            print(e)
        finally:
            print("Finally of RoundRobin...")
            self.calculateAvgMetrics()
            self.ui.repainting()
            self.kill()
            self.callback(id)
            self.ui.label_5.setText(f" RoundRobin Done...")

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
        self.ui.programState.Comparision["RoundRobin"] = {}
        self.ui.programState.Comparision["RoundRobin"]["AvgTurnAroundTime"] = avgTt
        self.ui.programState.Comparision["RoundRobin"]["AvgResponseTime"] = avgRt
        self.ui.programState.Comparision["RoundRobin"]["AvgWaitTime"] = avgWt
        self.ui.programState.Comparision["RoundRobin"]["Throughput"] = self.throughput


    def kill(self):
        self.shutdown = True