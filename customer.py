import numpy

class customer:
    def __init__(self, interTime, serTime, id,arrTime):
        self.id = id
        self.intervalTime = interTime
        self.serveTime = serTime
        self.arrivalTime = arrTime
        print(self.arrivalTime,self.serveTime,self.id,"\n")
