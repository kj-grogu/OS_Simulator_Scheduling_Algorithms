import sys

from myos.MyProcess import MyProcess


def createAndTestProcess():
    p1 = MyProcess(1, "zzz")
    p2 = MyProcess(2, "yyy")

    p1.start()
    p2.start()

    p1.join()
    p2.join()

    print("Processes finished")



def generateInput():
    inputFile = open('./io/ioinput.log', 'w')
    for i in range(10000):
        inputFile.write(str(i) +"\n")
    inputFile.close()


def main(args):
    print("@>@")
    createAndTestProcess()
    # generateInput()
    print("@>@")


if __name__ == '__main__':
    main(sys.argv)

