from collections import deque 
from customer import *

class waitQueue :
    def __init__ (self, maxlen) :
        self.maxLen = maxlen
        self.wQueue = deque()
        self.lastArrivalTime = 0.0
        self.totalDelayTime = 0.0
        self.delayedCusNum = 0

    
    def size(self) :
        return len(self.wQueue)
    
    def addCus(self, cus) :
        self.wQueue.append(cus)

    def getCus(self) :
        return self.wQueue.popleft()