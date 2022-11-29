import threading
import traceback
from time import sleep
from myos.ProgramState import ProgramState
from queue import PriorityQueue



def method1():
    indexes = ["P1", "P2", "P3", "P4"]
    data = {}
    data["P1"] = [0, 2, 4, 4, 4, 4, 1, 0]
    data["P2"] = [2, 1, 6, 1, 6, 0, 0, 0]
    data["P3"] = [3, 0, 2, 1, 2, 0, 0, 0]
    data["P4"] = [7, 3, 1, 1, 1, 1, 1, 0]

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
    currentProcess = "-None-"
    # data = self.ui.programState.Data

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
    timeSlice = 3
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
            if ap in processFinished :
                continue
            if mode[ap][0] == 'IO':
                if ap not in currentlyInIO:
                    currentlyInIO[ap] = True
                    ioQueue.append(ap)
                finalTimeLine[ap][t] = 'IO'
                processedAlready[ap] = True
                mode[ap].pop(0)
                processedAtTime[ap] = True
                print(f"T: {t} : {queue}, cp : {ap}, mode : I/O")
                ## if at next time the process is ready for CPU push it to CPU
                if mode[ap][0] == 'CPU':
                    queue.append(ap)


        cpuGIVEN = False
        processQueue = []
        # processQueue.extend(queue)
        [processQueue.append(x) for x in queue if x not in processQueue]
        queue = []
        queue.extend(processQueue)
        val = 0
        for cp in processQueue:
            print(f"T: {t} : {queue}, cp : {cp}, timeSliceMap : {timeSliceMap}")
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
                    print(f"T: {t} : {queue}, cp : {cp}, mode : CPU")
                    if len(mode[cp]) == 0:
                        processFinished[cp] = True
                    elif timeSliceMap[cp] == 0:
                        timeSliceMap[cp] = timeSlice
                        queue.remove(cp)
                        queue.append(cp)
                else:
                    finalTimeLine[cp][t] = 'RDY'
                    processedAlready[cp] = True
                    print(f"T: {t} : {queue}, cp : {cp}, mode : RDY")



    # self.finalTimeline = finalTimeLine
    print(f"============================")
    print(finalTimeLine)
    # print(self.ui.programState.WaitTime)
    print(f"============================")

    # for t in range(31):
    #     for k in list(finalTimeLine.keys()):
    #         if self.throughputStart == -1 and self.finalTimeline[k][t] != "None":
    #             self.throughputStart = t
    #         if self.finalTimeline[k][t] == "None":
    #             continue
    #         self.throughputEnd = t





if __name__ == "__main__":
    try:
        method1()
    except Exception as e:
        print("Some Exception in FCFS")
        traceback.print_exc()
        print(e)
    finally:
       print("Done")