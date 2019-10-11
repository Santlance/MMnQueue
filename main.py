from customer import *
from collections import deque
from waitQueue import *
from server import *
import numpy as npy
import matplotlib.pyplot as mplot
# 函数入口
if __name__ == '__main__' :
    instr = input("请输入平均到达时间、平均服务时间、顾客数、队列最大长度、服务器数\n")
    strs = instr.split(" ")
    averArrTime = float(strs[0])
    averSerTime = float(strs[1])
    customerNum = int(strs[2])
    maxQueueLen = int(strs[3])
    serNUm = int(strs[4])
    wQueue = waitQueue(maxQueueLen)

    # produce the interval time sequence refer to poisson_distribution
    arrTimes = npy.random.poisson(float(averArrTime),customerNum)      
    # produce the serval time sequence refer to exponential_distribution
    serTimes = npy.random.exponential(averSerTime,customerNum)  
    customers = []
    countTime = 0.0
    # produce the customer sequence
    for i in range(0,customerNum) :                             
        countTime += arrTimes[i]
        cus = customer(arrTimes[i], serTimes[i], i, countTime)
        customers.insert(len(customers), cus)
    lastArrivalTime = customers[len(customers) - 1].arrivalTime
    ser = server(customers, wQueue, serNUm)
    
    ser.mmnSimulation()
    
    print("the number of arriving people per s : ", customerNum / lastArrivalTime," p/s\n")
    print("the number of serving people per s : ", (ser.serveNum / ser.serveTime), " p/s\n")
    print("average number of people in queue : ",(wQueue.totalDelayTime / ser.currentTime)," p\n")
    print("average number of waiting time : ", (wQueue.totalDelayTime / ser.serveNum)," s\n")
    print("rate of using the server : " ,(ser.serveTime / ser.currentTime),"\n")
    #mplot.yticks([y for y in range(maxQueueLen + 1)])
    #mplot.step(ser.eventTime,ser.queueSize)
    #mplot.show()
    #mplot.plot(ser.eventTime,ser.queueSize)
    #mplot.scatter(ser.eventTime,ser.queueSize)
    #mplot.bar(ser.eventTime, ser.queueSize)
    #mplot.xticks([x for x in range(int(ser.currentTime) + 1) if x % 100 == 0])
    #mplot.scatter(ser.eventTime, ser.events)
    #mplot.show()

    colors = ['r','g','y','orange','b']
    figure = mplot.figure()
    fig1 = figure.add_subplot()
    fig1.set_xlabel("current time")
    fig1.set_ylabel("event")
    fig1.set_yticks([1,2,3,4,5])
    fig1.set_yticklabels(["leaves due to full","leaves after serving","serving","waiting","arrives"])
    for i in range(0,len(ser.eventTime)) :
        fig1.scatter(ser.eventTime[i],ser.events[i],c=colors[ser.events[i] - 1])
    for i in range(0,len(ser.eventTime)) : 
        fig1.annotate(str(ser.cusid[i]),(ser.eventTime[i],ser.events[i]))
    
    fig2 = fig1.twinx() # 双Y轴
    #fig = mplot.figure()
    #fig2 = fig.add_subplot()
    fig2.step(ser.eventTime,ser.queueSize)
    fig2.set_ylabel("queue size")
    fig2.set_xlabel("current time")
    mplot.show()
