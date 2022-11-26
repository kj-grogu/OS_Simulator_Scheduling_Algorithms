class ProgramState():
    indexes = ["P1", "P2", "P3", "P4"]
    Algo = ""
    ArrivalTime = 0
    Priority = 1
    Exec_1 = 2
    Io_1 = 3
    Exec_2 = 4
    Io_2 = 5
    Exec_2 = 6
    Io_2 = 7

    Data = {}
    Data["P1"] = [0] * 8
    Data["P2"] = [0] * 8
    Data["P3"] = [0] * 8
    Data["P4"] = [0] * 8

    ## MAX vs Given
    ExecutionData = {}
    ExecutionData["P1"] = [0] * 2
    ExecutionData["P2"] = [0] * 2
    ExecutionData["P3"] = [0] * 2
    ExecutionData["P4"] = [0] * 2

    Processes = {}
    Processes["P1"] = None
    Processes["P2"] = None
    Processes["P3"] = None
    Processes["P4"] = None

    TurnAroundTime = {}
    TurnAroundTime["P1"] = 0
    TurnAroundTime["P2"] = 0
    TurnAroundTime["P3"] = 0
    TurnAroundTime["P4"] = 0

    WaitTime = {}
    WaitTime["P1"] = 0
    WaitTime["P2"] = 0
    WaitTime["P3"] = 0
    WaitTime["P4"] = 0

    ResponseTime = {}
    ResponseTime["P1"] = 0
    ResponseTime["P2"] = 0
    ResponseTime["P3"] = 0
    ResponseTime["P4"] = 0

    Throughput = {}

    Comparision = {}

    scheduler = None

    def resetSummaries(self):
        self.TurnAroundTime["P1"] = 0
        self.TurnAroundTime["P2"] = 0
        self.TurnAroundTime["P3"] = 0
        self.TurnAroundTime["P4"] = 0

        self.WaitTime["P1"] = 0
        self.WaitTime["P2"] = 0
        self.WaitTime["P3"] = 0
        self.WaitTime["P4"] = 0

        self.ResponseTime["P1"] = 0
        self.ResponseTime["P2"] = 0
        self.ResponseTime["P3"] = 0
        self.ResponseTime["P4"] = 0


