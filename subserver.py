

class subserver :
    def __init__(self, id) :
        self.id = id
        self.endTime = 0.0
        self.isBusy = False
        self.serCus = None

    def serveCus(self, cus, curTime) :
        self.isBusy = True
        self.serCus = cus
        self.endTime = cus.serveTime + curTime

    def __lt__ (self,other) :
        return self.endTime < other.endTime
    
    def __repr__(self) :
        return ("<id: "+str(self.id)+" , endTime : "+str(self.endTime)+ " >")