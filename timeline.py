if __name__ == "__main__":
    data = {}
    data["P1"] = [0, 0, 4, 4, 4, 2, 2, 0]
    data["P2"] = [2, 0, 8, 1, 4, 0, 0, 0]
    data["P3"] = [3, 0, 2, 1, 2, 0, 0, 0]
    data["P4"] = [7, 0, 1, 1, 1, 1, 1, 0]
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
    finalTimeLine ={}
    finalTimeLine["P1"] = ["None"] * 31
    finalTimeLine["P2"] = ["None"] * 31
    finalTimeLine["P3"] = ["None"] * 31
    finalTimeLine["P4"] = ["None"] * 31

    for i in range(len(data)):
        p =  "P{0}".format(i+1)
        for j in range(len(data[p])):
            if j == 1:
                continue
            l = len(calculated[p])
            prev = calculated[p][-1] if l> 0 else 0
            calculated[p].append(prev + data[p][j])
    print(calculated)
    for i in range(len(data)):
        p = "P{0}".format(i + 1)
        arr = ["CPU", "IO"]
        ai = 0
        for j in range(len(calculated[p]) -1):
            cur = calculated[p][j]
            next = calculated[p][j+1]
            for k in range(cur, next, 1):
                mode[p].append(arr[ai])
            ai += 1
            ai = ai  % 2
    print(mode)
    for i in range(len(data)):
        p = "P{0}".format(i + 1)
        start = calculated[p][0]
        end = calculated[p][-1]
        mi = 0
        for j in range(start, end , 1):
            finalTimeLine[p][j] = mode[p][mi]
            mi += 1
    print(f"final Time Line")
    for ft in finalTimeLine:
        print(f"{ft} : {finalTimeLine[ft]}")

