import time








def main():
    def runn(i):
        print(time.time(),i)
    a2 = Time_interval(runn,1/360)
    while True:
        a2.run(3)






class Time_interval(object):
    """docstring for timeinterval"""
    def __init__(self, func ,timee = 1 / 2 , num = None): 
        self.timeinterv = timee #* 60 * 60
        self.num = num # 运行的次数
        self.num_now = 0
        self.time = time.time()
        self.func = func
    def run(self,*args,**kw): # 后期加入是否先运行程序
        ti = self.time + self.timeinterv *  self.num_now
        ti_now = time.time()
        if  ti < ti_now:
            # print(ti,ti_now)
            self.func(*args,**kw)
            self.num_now += 1
        else:
            time.sleep(1)
            print(time.ctime(),'finished',int(ti-ti_now),end='\r')
            

if __name__ == '__main__':
    main()