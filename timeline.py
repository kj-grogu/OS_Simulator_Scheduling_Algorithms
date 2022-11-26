from queue import PriorityQueue
import copy

if __name__ == "__main__":
    indexes = ["P1", "P2", "P3", "P4"]
    data = {}
    data["P1"] = [0, 0, 3, 1, 1, 1, 1, 0]
    data["P2"] = [2, 1, 1, 1, 0, 0, 0, 0]
    data["P3"] = [3, 2, 2, 1, 2, 0, 0, 0]
    data["P4"] = [1, 3, 1, 1, 1, 1, 1, 0]
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
                if p in processGiven and requiredCPUTime[p] == 0 and not processFinished[p]:
                    print(f"Process finished {p}")
                    processFinished[p] = True
                    # self.ui.programState.TurnAroundTime[p] = t - processStart[p]  # calculate the TurnAroundTime when finishing
                    currentProcess = "-None-"  ## if minHeap.empty() else minHeap.get()[1] # take up the next process

        if len(queue) < 1:
            continue # nothing to update at this time continue to next time unit

        print(f"at time : {t} : {queue}")
        currentProcess = queue.pop(0)

        if currentProcess not in processGiven:
            processGiven[currentProcess] = 0
        processGiven[currentProcess] += 1
        requiredCPUTime[currentProcess] -= 1
        finalTimeLine[currentProcess][t] = processQueue[currentProcess].pop(0)
        if len(processQueue[currentProcess]) > 0:
            queue.append(currentProcess) # push the back the same process later processing if its not finished
        else:
            processFinished[currentProcess] = True


        # mark other processes as ready if they have arrived
        for op in indexes:
            if processFinished[op] == True:
                continue
            if op not in processStart or currentProcess == op:
                continue
            finalTimeLine[op][t] = "READY"
            # self.ui.programState.WaitTime[op] += 1  # increase the wait time for each ready state

    print(f"============================")
    print(finalTimeLine)
    print(f"============================")
