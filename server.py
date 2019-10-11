from customer import *
from waitQueue import *
from collections import deque
from subserver import *
import functools



class server :
    def __init__(self, customers, wqueue, num) :
        self.customers = customers
        self.wQueue = wqueue
        self.currentTime = 0.0
        self.serveTime = 0.0
        self.serveNum = 0
        self.eventTime = []
        self.queueSize = []
        self.events = []
        self.cusid = []
        self.subservers = []
        for i in range(num) :
            self.subservers.insert(len(self.subservers), subserver(i))

    def minSer(self) :
        self.subservers.sort()
        ser = self.subservers[0]
        return ser

    def isAllBusy(self) :
        for ser in self.subservers :
            if ser.isBusy == False :
                return False
        return True    

    def getFreeSer(self) :
        for ser in self.subservers :
            if ser.isBusy == False :
                return ser

    def record(self,event,id) :
        self.eventTime.insert(len(self.eventTime), self.currentTime)
        self.queueSize.insert(len(self.queueSize), self.wQueue.size())
        num = 0
        if event == "arrives" :
            num = 5
        elif event == "waiting" :
            num = 4
        elif event == "serving" :
            num = 3
        elif event == "leaves after serving" :
            num = 2
        else :
            num = 1
        self.events.insert(len(self.events),num)
        self.cusid.insert(len(self.cusid),id)

    def simulation(self) :
        while len(self.customers) != 0 or self.wQueue.size() != 0 :

                                                                                    # if wait queue is empty 
            if self.wQueue.size() == 0 :
                cus = self.customers.popleft()                                      # take the first cus
                cus.arrivalTime = self.wQueue.lastArrivalTime + cus.intervalTime    # cus.arrtime is lastarrtime plus intervaltime
                self.wQueue.addCus(cus)                                             # add the cus
                self.wQueue.lastArrivalTime = cus.arrivalTime                       # update the arrival time
                self.currentTime = cus.arrivalTime                                  # update currenttime because the event
                print(self.id, " : Time : ", self.currentTime," No." , cus.id, " arrives\n")
                self.record("arrives",cus.id)
               
                                                                                    # if wait queue is not empty , serve the first cus
            serCus = self.wQueue.getCus()
            endTime = serCus.serveTime + self.currentTime                           # cal the endtime
            self.wQueue.totalDelayTime += self.currentTime - serCus.arrivalTime     # wait time is endtime minus arrtime
            self.serveTime += serCus.serveTime                                      # update the serve time

            #self.wQueue.queueArea += self.wQueue.size() * serCus.intervalTime

            print(self.id, " : Time : ", self.currentTime," No. ",serCus.id," is serving\n")
            self.record("serving",serCus.id)



            while len(self.customers) != 0 and self.wQueue.size() < self.wQueue.maxLen :
                if self.customers[0].intervalTime + self.wQueue.lastArrivalTime >= endTime :
                    break
                cus = self.customers.popleft()
                cus.arrivalTime = self.wQueue.lastArrivalTime + cus.intervalTime
                self.wQueue.lastArrivalTime = cus.arrivalTime
                self.currentTime = cus.arrivalTime
                self.wQueue.addCus(cus)
                self.wQueue.delayedCusNum += 1
                print(self.id, " : Time : ", self.currentTime," No. ",cus.id," arrives and starts waiting \n")
                self.record("arrives",cus.id)
                self.record("waiting",cus.id)



            while len(self.customers) != 0 :
                if self.customers[0].intervalTime + self.wQueue.lastArrivalTime >= endTime :
                    break
                cus = self.customers.popleft()
                self.wQueue.lastArrivalTime += cus.intervalTime
                self.currentTime = self.wQueue.lastArrivalTime
                print(self.id, " : Time : ", self.currentTime," No. ",cus.id," leaves because queue if full\n")
                self.record("arrives",cus.id)
                self.record("arrives but leaves because queue is full",cus.id)

            self.currentTime = endTime
            self.serveNum += 1  
            print(self.id, " : Time : ", self.currentTime," No. ",serCus.id," is served and leaves\n")
            self.record("leaves after serving",serCus.id)



    def mmnSimulation(self) :
        while len(self.customers) != 0 or self.wQueue.size() != 0 :
            # 把在前面的事件输出
            while True :
                mSer = self.minSer()
                if mSer.isBusy and (len(self.customers) == 0 or mSer.endTime <= self.customers[0].arrivalTime) :
                    self.currentTime = mSer.endTime
                    print("id : ",mSer.id," Time : ", self.currentTime, " No. ", mSer.serCus.id," leaves after serving\n")
                    self.wQueue.totalDelayTime += self.currentTime - mSer.serCus.arrivalTime
                    self.serveTime += mSer.serCus.serveTime
                    self.serveNum += 1
                    self.record("leaves after serving", mSer.serCus.id)
                    mSer.isBusy = False
                    mSer.endTime = float("inf")
                    if self.wQueue.size() !=0 :
                        cus = self.wQueue.getCus()
                        print("Time : ", self.currentTime, " No. ", cus.id," is serving\n")
                        self.record("serving", cus.id)
                        mSer.serveCus(cus, self.currentTime)
                else :
                    break
            if len(self.customers) == 0 and self.wQueue.size() == 0 :
                break
            # 推进到当前时间
            curCus = self.customers[0]
            del self.customers[0]
            self.currentTime = curCus.arrivalTime
            print("Time : ", self.currentTime, " No. ", curCus.id," arrives\n")
            self.record("arrives", curCus.id)

            if self.wQueue.size() >= self.wQueue.maxLen and self.isAllBusy() :
                print("Time : ", self.currentTime, " No. ", curCus.id," leaves cuz full queue\n")
                self.record("leaves cuz full", curCus.id)
                continue
            if self.isAllBusy() == False :
                ser = self.getFreeSer()
                ser.serveCus(curCus, self.currentTime)
                print("Time : ", self.currentTime, " No. ", curCus.id," is serving\n")
                self.record("serving", curCus.id)
                continue
            if self.wQueue.size() < self.wQueue.maxLen :
                self.wQueue.addCus(curCus)
                print("Time : ", self.currentTime, " No. ", curCus.id," starts waiting\n")
                self.record("waiting", curCus.id)





        