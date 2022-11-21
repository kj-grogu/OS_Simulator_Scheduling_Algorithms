import threading
from time import sleep
from myos.ProgramState import ProgramState


class FirstComeFirstServe(threading.Thread):
    name = ""
    id = 0
    ioProcessingLag = 0
    lag = 2
    shutdown = False
    clockTime = -1
    queue = []
    processedCount = 0
    toProcess = 4
    processStart = {}
    currentProcess = ""
    maxTime = 31

    statusDict = {}
    statusDict["None"] = "background-color:none;"
    statusDict["Ready"] = "background-color:yellow;"
    statusDict["CPU"] = "background-color:green;"
    statusDict["IO"] = "background-color:red;"

    def __init__(self, id, name, ui, callback=lambda: None):
        threading.Thread.__init__(self)
        self.id = id
        self.name = name
        self.ui = ui
        self.callback = callback
        self.shutdown =False
        self.toProcess = len(self.ui.programState.Data)

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
        self.calculateTimeline()
        self.queue = []
        self.clockTime = -1
        try:
            while(self.clockTime < self.maxTime and self.processedCount < 4):
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

                    # process not yet arrived
                    # if(self.finalTimeline[p][self.clockTime] == 'None'):
                    #     print(f"Skipping this process {p} as not yet arrived")
                    #     continue
                    #     ## inner IF ENDS
                    # ## NONE IF ENDS

                    # # process not yet in queue add to queue
                    if p not in self.processStart and self.finalTimeline[p][self.clockTime] != 'None':
                        self.processStart[p] = self.clockTime
                        self.queue.append(p)
                        print(f"Process arrived : {p}, queue : {self.queue}")


                    # # process at the head of the queue will be in executing state
                    self.currentProcess = self.queue[0]
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

                ## READY LOOP STARTS
                for i in range(1, len(self.queue), 1):
                    p = self.queue[i]
                    bid = "{0}_timeline_{1}".format(p.lower(), self.clockTime)
                    button = self.ui.__dict__[bid]
                    style = self.statusDict["Ready"]
                    button.setStyleSheet(style)
                ## READY LOOP ENDS

                self.processStart[self.currentProcess] += 1
                currentProcessTimeline = self.finalTimeline[self.currentProcess]
                currentProcessIndex = self.processStart[self.currentProcess]
                status = currentProcessTimeline[currentProcessIndex]
                print(f"currentProcess : {self.currentProcess}")
                if status == "None":
                    self.queue.pop(0)
                    self.processedCount += 1
            ## WHILE LOOP ENDS
        ## TRY ENDS
        except Exception as e:
            print(e)
        finally:
            print("Finally of FCFS...")
            self.kill()
            self.callback(id)
            self.ui.label_5.setText(f" FCFS Done...")


    def kill(self):
        self.shutdown = True