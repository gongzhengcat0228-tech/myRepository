import numpy as np
T=20000
arate=3
drate=4
t=0
arrival=[]  # 记录顾客到达的时间
while t<T:
    t=t+np.random.exponential(1.0/arate)  # 生成到达序列，顾客到达的时间间隔服从指数分布
    arrival.append(t)

t=0  # 主循环，t表示当前时刻
N=0  # 顾客的数量
departure=[]  # 记录顾客离开的时间
recording=[]  # recording = [start_time, end_time, number_of_packets]
while t<T and len(arrival)>0:
    if len(departure)==0:
        told=t  # told=t=0
        t=arrival[0]  # 记录顾客的到达时间
        del arrival[0]
        de=t+np.random.exponential(1.0/drate)  # 生成顾客的服务时间
        departure.append(de)
        recording.append([told, t, N])  # 记录从told到t这一时间段中队列中有多少顾客
        N=N+1  # 队列人数加一
    else:
        if departure[0]<arrival[0]:  # departure[0]=t+np.random.exponential(1.0/drate)<下一个顾客到达时间，下一事件顾客离开队列
            told=t  # told=t=0
            t=departure[0]
            del departure[0]
            recording.append([told, t, N])
            N=N-1  # 队列人数减一
            if N>=1:  # 若仍有人在系统里，则立即开始为下一个人服务
                de=t+np.random.exponential(1.0/drate)
                departure.append(de)
                departure.sort()  # 保证队列最前端的是最早的离开时间
        else:  # departure[0]=t+np.random.exponential(1.0/drate)>下一个顾客到达时间，下一事件新顾客到达队列
            told=t
            t=arrival[0]
            del arrival[0]
            recording.append([told, t, N])
            N=N+1  # 队列人数加一

x1=0.0
x2=0.0
for i in range(0, len(recording)):
    x1=x1+(recording[i][1]-recording[i][0])*recording[i][2]  # x1+ = (end_time - start_time)*number_of_packets
    x2=x2+(recording[i][1]-recording[i][0])

Mnumber=[x[2] for x in recording]  # number_of_packets
M=max(Mnumber)  # 记录队列中人数最多的时候的人数
distribution=[0 for i in range(M+1)]  # 初始化分布，使用列表推导式，把列表0，1，2...M索引的位置的值上都设置为0

for i in range(0, len(recording)):
    state=recording[i][2]  # 排队人数，有限自动状态机中的状态
    distribution[state]=distribution[state]+recording[i][1]-recording[i][0]  # 算出每个状态持续的总时间
    # If there are "state" packets, we add the duration the systems stays in this state.

meanqueue=x1/x2  # 平均排队人数
print (meanqueue)
sumtime=sum(distribution)  # 系统总时间
pdf=[x/sumtime for x in distribution] # 算出每个状态持续时间占总时间的比例，也就是概率
print(pdf)
# The distribution is (sum time duration when there are "state" packets)/(total time duration)


        
    
    
