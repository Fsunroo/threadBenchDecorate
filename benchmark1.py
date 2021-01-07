# IN HIS NAME
import time
import csv
from numpy import var


#PART 2
#Exercise 4-A:
def benchmark(fun):
    def inner(*args,warmups=0 ,iter=1, verbose=False, csv_file = None,**kwargs):
        logs = []  #k:v for iteration:time
        for i in range(warmups+iter):
            t1 = time.time()
            fun(*args,**kwargs)
            t2 = time.time()
            logs.append(t2-t1) 

        avg = sum(logs[warmups:])/iter
        print(f'Average of Execution Time is: {avg}')

        variance = var(logs[warmups:])
        print(f'Variance of Execution Time is: {variance}')

        if verbose:
            for log in logs:
                print(f'Execution time  #{logs.index(log)+1} :{log}')

        if csv_file:
            with open(csv_file, 'w',newline='') as f:
                wr = csv.writer(f, dialect='excel')
                row = ['runtime', 'is warmup', 'timing']
                wr.writerow(row)

                for log in logs:
                    iteration = logs.index(log)
                    row = [iteration+1 ,iteration < warmups , log]
                    wr.writerow(row)
                f.close()
        return avg, variance
                
    return inner

@benchmark
def fun(**kwargs):
    result = 1
    for x in range(1,10):
        result = result*x
        print(result)


fun(warmups=2, iter=5,csv_file='Result.csv', verbose=True)


#Exercise 5:
import threading


def compute_fibonacci(n=50000,**kwargs):
    previous=1
    last=1
    i=1
    result=1
    while i+1< n:
        i=i+1
        result = last+previous
        previous = last
        last = result
    #print('computed as: ',result)


def test(f,iter=1,degree=1):
    
    thread_list=[]
    for d in range(degree):
        thread_list.append(threading.Thread(
            target=f, kwargs={'iter': iter}))

    for thread in thread_list:
        thread.start()
'''
    for thread in thread_list:
        thread.join()'''

def save_info(degree,iteration,avg,var):
    with open(f'f_{degree}_{iteration}.txt','w') as f:
        f.write(f'Average of Execution Time(s) is: {avg}\n')
        f.write(f'Variance of Execution Time(s) is: {var}\n')
        f.close()


avg, varia = test(compute_fibonacci, iter=16, degree=1)
save_info(1, 16, avg, varia)

avg, varia = test(compute_fibonacci, iter=8, degree=2)
save_info(2, 8, avg, varia)

avg, varia = test(compute_fibonacci, iter=4, degree=4)
save_info(4, 4, avg, varia)

avg, varia = test(compute_fibonacci, iter=2, degree=8)
save_info(8, 2, avg, varia)
