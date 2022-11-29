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
        self.statusDict["Ready"] = "background-color: rgb(255, 247, 99);"
        self.statusDict["CPU"] = "background-color: rgb(152, 235, 52);"
        self.statusDict["IO"] = "background-color:rgb(230, 74, 50);"

        self.throughputStart = -1;
        self.throughputEnd = -1;
        self.throughput = 0;

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

        queue = []
        for t in range(31):
            for j in range(4):
                p = "P{0}".format(j + 1)
                if t >= arrivalTime[p]:
                    if p not in processStart:
                        processStart[p] = t
                        queue.append(p)

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
        arrivedProcess = {}
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

        for i in range(len(data)):
            p = "P{0}".format(i + 1)
            for j in range(len(data[p])):
                if j == 1:
                    priorities[p] = data[p][1]
                    continue
                if j < 2 or j % 2 == 1:
                    continue
                if data[p][j] > 0:
                    requiredCPUTime[p].append(data[p][j])

        print(requiredCPUTime)
        print(f"priorities{priorities}")

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

        queue = []
        timeSlice = self.ui.programState.roundRobinCPUBurst
        timeSliceMap = {}
        ioQueue = []
        currentlyInIO = {}

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
                    queue.append(p)
                    timeSliceMap[p] = timeSlice

            if len(queue) < 1:
                continue  # nothing to update at this time continue to next time unit

            processedAtTime = {}
            currentlyInIO = {}
            processedAlready = {}
            # MARK ALL THE IO PROCESS SEPERATELY
            for ap in arrivedProcess:
                if ap in processFinished:
                    continue
                if mode[ap][0] == 'IO':
                    if ap not in currentlyInIO:
                        currentlyInIO[ap] = True
                        ioQueue.append(ap)
                    finalTimeLine[ap][t] = 'IO'
                    processedAlready[ap] = True
                    mode[ap].pop(0)
                    processedAtTime[ap] = True
                    ## if at next time the process is ready for CPU push it to CPU
                    if mode[ap][0] == 'CPU':
                        queue.append(ap)

            cpuGIVEN = False
            processQueue = []
            # processQueue.extend(queue)
            [processQueue.append(x) for x in queue if x not in processQueue]
            queue = []
            queue.extend(processQueue)
            for cp in processQueue:
                print(f"at time : {t} : {queue}, cp : {cp}, mode : {mode[cp]}")
                if cp in currentlyInIO:
                    queue.remove(cp)
                    queue.append(cp)
                    continue
                if cp in processFinished:
                    queue.remove(cp)
                    continue
                if cp in processedAlready:
                    continue
                if timeSliceMap[cp] > 0:
                    if cpuGIVEN == False:
                        processedAlready[cp] = True
                        cpuGIVEN = True
                        finalTimeLine[cp][t] = 'CPU'
                        timeSliceMap[cp] -= 1
                        mode[cp].pop(0)
                        if len(mode[cp]) == 0:
                            processFinished[cp] = True
                            self.ui.programState.TurnAroundTime[cp] = t - arrivedProcess[cp] + 1
                        elif timeSliceMap[cp] == 0:
                            timeSliceMap[cp] = timeSlice
                            queue.remove(cp)
                            queue.append(cp)
                        if cp not in processFirstCPU.keys():
                            processFirstCPU[cp] = t
                            self.ui.programState.ResponseTime[cp] = t - arrivedProcess[cp]
                    else:
                        finalTimeLine[cp][t] = 'Ready'
                        processedAlready[cp] = True
                        self.ui.programState.WaitTime[cp] += 1

        print(finalTimeLine)
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