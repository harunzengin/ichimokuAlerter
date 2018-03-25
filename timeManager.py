import time
class timeManager():

    def __init__(self,timeStamp):
        self.detect1h = int(timeStamp // 3600000)
        self.detect4h = int(timeStamp // 14400000)
        self.detect1d = int(timeStamp // 86400000)
        self.getActionType(timeStamp)

    def getActionType(self,time:int) -> chr:
        if(int(time // 86400000) != self.detect1d):

            self.detect1d = int(time // 86400000)
            return 'd'

        if(int(time//14400000) != self.detect4h):
            self.detect4h = int(time // 14400000)
            return 'q'

        if (int(time// 3600000) != self.detect1h):
            print(str(int(time// 3600000)) + "    "+ str(self.detect1h))
            self.detect1h = int(time // 3600000)
            return 'h'
        return 'n'