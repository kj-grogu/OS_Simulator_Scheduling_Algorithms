import threading
import traceback
from time import sleep
from myos.ProgramState import ProgramState


class FirstComeFirstServe(threading.Thread):

    def __init__(self, id, name, ui, callback=lambda: None):
        print(f"Constructor of FCFS")
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.ui = ui
        self.callback = callback
        self.shutdown =False
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
        self.firstCPU = {}

        self.statusDict = {}
        self.statusDict["None"] = "background-color:none;"
        self.statusDict["Ready"] = "background-color: rgb(255, 247, 99);"
        self.statusDict["CPU"] = "background-color: rgb(152, 235, 52);"
        self.statusDict["IO"] = "background-color: rgb(230, 74, 50);"
        self.throughputStart = -1;
        self.throughputEnd = -1;
        self.throughput = 0;

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
        processStart = {}
        processFirstCPU = {}

        finalTimeLine = {}
        finalTimeLine["P1"] = ["None"] * 31
        finalTimeLine["P2"] = ["None"] * 31
        finalTimeLine["P3"] = ["None"] * 31
        finalTimeLine["P4"] = ["None"] * 31

        arrived = {}

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
        for t in range(31):
            for pi in range(4):
                p = "P{0}".format(pi + 1)
                if p in arrived:
                    continue
                if t < processStart[p]:
                    continue;
                else:
                    queue.append(p)
                    arrived[p] = True
            if len(queue) < 1:
                continue

            cpuGiven = False
            beforeProcessing = queue.copy()
            toProcess = len(queue)
            if toProcess < 1:
                continue
            for qi in range(toProcess):
                print(f"Time : {t}, beforeProcessing : {beforeProcessing}")
                currentProcess = beforeProcessing[qi]
                currentMode = mode[currentProcess][0]
                print(f"Time : {t}, current Process : {currentProcess}, processStart : {processStart}")
                if currentProcess not in processStart:
                    processStart[currentProcess] = t
                    print(f"Time : {t},Adding current Process {processStart}")
                if currentMode == "IO":
                    finalTimeLine[currentProcess][t] = "IO"
                    mode[currentProcess].pop(0)
                    del queue[qi]
                    # queue.pop(0)
                    queue.append(currentProcess)
                if currentMode == "CPU":
                    if cpuGiven == False:
                        cpuGiven = True
                        finalTimeLine[currentProcess][t] = "CPU"
                        mode[currentProcess].pop(0)
                        if currentProcess not in processFirstCPU:
                            processFirstCPU[currentProcess] = t
                            self.ui.programState.ResponseTime[currentProcess] = t - processStart[currentProcess]
                    else:
                        finalTimeLine[currentProcess][t] = "Ready"
                        self.ui.programState.WaitTime[currentProcess] += 1
                if len(mode[currentProcess]) < 1:
                    queue.remove(currentProcess)
                    print("self.processStart")
                    print(processStart)
                    self.ui.programState.TurnAroundTime[currentProcess] = t - processStart[currentProcess] + 1

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
        self.queue = []
        self.clockTime = -1
        try:
            for i in range(31):
                sleep(2)
                self.clockTime += 1
                print(f"FCFS Running clockTime : {self.clockTime}")
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
            print("Some Exception in FCFS")
            traceback.print_exc()
            print(e)
        finally:
            print("Finally of FCFS...")
            self.calculateAvgMetrics()
            self.ui.repainting()
            self.kill()
            self.callback(id)
            self.ui.label_5.setText(f" FCFS Done...")

    def runOLD(self):
        self.calculateTimeline()
        self.queue = []
        self.clockTime = -1
        try:
            for i in range(31):
                sleep(2)
                self.clockTime += 1
                print(f"FCFS Running clockTime : {self.clockTime}")
                print(f"Outer loop queue: {self.queue}")
                self.currentProcess = self.queue[0] if len(self.queue) > 0 else "PX"
                if self.shutdown == True:
                    break

                # at each time unit, iterate through all the process to check if any new process has arrived
                for i in range(len(self.finalTimeline)):
                    p = ProgramState.indexes[i]

                    print(f"p : {p}, status : {self.finalTimeline[p][self.clockTime]}")
                    print(f"processStart : {self.processStart}")
                    # # process not yet in queue add to queue
                    if p not in self.processStart and self.finalTimeline[p][self.clockTime] != 'None':
                        self.processStart[p] = self.clockTime
                        self.queue.append(p)
                        print(f"Process arrived : {p}, queue : {self.queue}")
                        self.ui.programState.ResponseTime[p] = self.clockTime
                        self.ui.programState.TurnAroundTime[p] = self.clockTime

                    if len(self.queue) < 1:
                        print(f" len of Queue : {len(self.queue)} No Process arived yet at {self.clockTime}, so skipping")
                        continue

                    # # process at the head of the queue will be in executing state
                    self.currentProcess = self.queue[0]
                    if self.currentProcess not in self.firstCPU:
                        self.firstCPU[self.currentProcess] = self.clockTime
                    currentProcessIndex = self.processStart[self.currentProcess]
                    currentProcessTimeline = self.finalTimeline[self.currentProcess]
                    status = currentProcessTimeline[currentProcessIndex]
                    style = self.statusDict[status]
                    ### SET COLOR
                    bid = "{0}_timeline_{1}".format(self.currentProcess.lower(), self.clockTime)
                    button = self.ui.__dict__[bid]
                    button.setStyleSheet(style)
                    ### SET COLOR
                    sleep(0.05)
                    ### INNER LOOP ENDS

                ## READY LOOP STARTS start from 2 as first process in io and second in CPU
                for i in range(2, len(self.queue), 1):
                    p = self.queue[i]
                    bid = "{0}_timeline_{1}".format(p.lower(), self.clockTime)
                    button = self.ui.__dict__[bid]
                    style = self.statusDict["Ready"]
                    button.setStyleSheet(style)
                    if p not in self.ui.programState.WaitTime:
                        self.ui.programState.WaitTime[p] = 0
                    self.ui.programState.WaitTime[p] += 1

                ## READY LOOP ENDS

                if len(self.queue) < 1:
                    print(f"Skipping while loop as no process arrived")
                    continue

                self.processStart[self.currentProcess] += 1
                currentProcessTimeline = self.finalTimeline[self.currentProcess]
                currentProcessIndex = self.processStart[self.currentProcess]
                status = currentProcessTimeline[currentProcessIndex]
                print(f"currentProcess : {self.currentProcess}")

                if status == "None":
                    self.queue.pop(0)
                    self.processedCount += 1
                    self.ui.programState.TurnAroundTime[self.currentProcess] = self.clockTime - self.ui.programState.TurnAroundTime[self.currentProcess]

            ## WHILE LOOP ENDS
        ## TRY ENDS
        except Exception as e:
            print("Some Exception in FCFS")
            traceback.print_exc()
            print(e)
        finally:
            print("Finally of FCFS...")
            self.ui.label_5.setText(f" FCFS Done...")
            for i in self.ui.programState.indexes:
                self.ui.programState.ResponseTime[i] = self.firstCPU[i] - self.ui.programState.Data[i][0]
            print(f"TurnAroundTime : {self.ui.programState.TurnAroundTime}")
            print(f"WaitTime : {self.ui.programState.WaitTime}")
            print(f"ResponseTime : {self.ui.programState.ResponseTime}")
            self.calculateAvgMetrics()
            self.ui.repainting()
            self.kill()
            self.callback(id)

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
        self.ui.programState.Comparision["FirstComeFirstServe"] = {}
        self.ui.programState.Comparision["FirstComeFirstServe"]["AvgTurnAroundTime"] = avgTt
        self.ui.programState.Comparision["FirstComeFirstServe"]["AvgResponseTime"] = avgRt
        self.ui.programState.Comparision["FirstComeFirstServe"]["AvgWaitTime"] = avgWt
        self.ui.programState.Comparision["FirstComeFirstServe"]["Throughput"] = self.throughput

    def kill(self):
        self.shutdown = True