from queue import PriorityQueue
import copy

if __name__ == "__main__":
    indexes = ["P1", "P2", "P3", "P4"]
    data = {}
    data["P1"] = [0, 0, 3, 1, 1, 1, 1, 0]
    data["P2"] = [2, 1, 1, 1, 4, 0, 0, 0]
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
    priorities = {} ## startTime, Priority
    processStart = {}
    processGiven = {}
    processQueue = {}

    for i in range(len(data)):
        p = "P{0}".format(i + 1)
        for j in range(len(data[p])):
            if j == 1:
                priorities[p] = [data[p][0],data[p][1]]
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
                    print(f"Process finished {p}, {maxHeap.get()}")
        tempQue = copy.copy(maxHeap)
        if tempQue.empty():
            continue
        currentHighest = tempQue.get()[1]

        if currentHighest not in processGiven:
            processGiven[currentHighest] = 0
        processGiven[currentHighest] += 1
        finalTimeLine[currentHighest][t] =  processQueue[currentHighest].pop(0)

        while not tempQue.empty():
            op = tempQue.get()[1]
            finalTimeLine[op][t] = "READY"
    print(finalTimeLine)

