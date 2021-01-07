#In His Name
import time
from numpy import var
import csv


#Exercise 4- A

def benchmark (fun): #Defining benchmark Decorator
    def inner(*args,warmups=0, iter=1, verbose=False, csv_file=None, **kwargs): #Defining inner function which is returned when decorator is called
        logs=[]
        for i in range(warmups+iter):
            t1 = time.time()
            fun(*args,**kwargs)
            t2 = time.time()
            logs.append(t2-t1)
        avg = sum(logs[warmups:])/iter                      #warmup rounds will be ignored in calculation
        print(f'Average of Executaion Time: {avg}')
        variance = var(logs[warmups:])                      #warmup rounds will be ignored in calculation, using numpy.var
        print(f'Variance of Executaion Time: {variance}')   

        if verbose:
            i=0
            for log in logs:
                i=i+1
                print(f'Execution Time #{i}: {log}')       #printing all logs including warmups
                
        if csv_file:
            with open(csv_file,'w',newline='') as f:
                i=0
                wr = csv.writer(f) 
                wr.writerow(['run time', 'is warmup', 'timing'])  #wanted format for csvfile
                for log in logs:
                    wr.writerow([i+1, i<warmups, log])
                    i=i+1
                f.close()
        return avg, variance
    return inner


@benchmark
def fun(**kwargs):          #Just for TEST
    result = 1
    for x in range(1, 10):
        result = result*x
        print(result)


fun(warmups=2, iter=5, csv_file='Result.csv', verbose=True)


#Exercise 5

import threading

class myThread(threading.Thread):               # Defining threading class as threading Documentation declared
    def __init__(self,iter ,n=100000):
        self.n = n
        self.iter=iter
        threading.Thread.__init__(self)


    def compute_fibonacci(self):                 # my f function for calculation of fibonacci number
        n= self.n
        previous = 1
        last = 1
        i = 1
        result = 1
        while i+1 < n:
            i = i+1
            result = last+previous
            previous = last
            last = result

    def run(self):                               # this function is called automatically
        for i in range(self.iter):
            self.compute_fibonacci()

@benchmark                                       # the most beautiful way of exploiting a decorator in python :)
def test(degree, iteration):
    thread_list = []
    for d in range(degree):
        thread1 = myThread(iteration)
        thread_list.append(thread1)

    for thread in thread_list:
        thread.start()


    for thread in thread_list:                   # waiting for all threads to finish
        thread.join()


def save_info(degree, iteration, avg, var):                   # a simple function for saving a little time
    with open(f'f_{degree}_{iteration}.txt', 'w') as f:
        f.write(f'Average of Execution Time(s) is: {avg}\n')
        f.write(f'Variance of Execution Time(s) is: {var}\n')
        f.close()


avg, varia = test(1,16)
save_info(1, 16, avg, varia)

avg, varia = test(2,8)
save_info(2, 8, avg, varia)

avg, varia = test(4,4)
save_info(4, 4, avg, varia)

avg, varia = test(8,2)
save_info(8, 2, avg, varia)


'''
As it is obvious, the Execution Time is not reduced by increasing the degree of parallelism, which seems a little odd...
But the point is that the threading module uses only one Process and in Python every Process is allowed to have a single 
GIL(Global Interpreter Lock) So that it is not really 'parallel' when it comes to mathematical process that all use cpu, 
multi threading is usually used for applications that probablly might wait for a response from a server(like for web crawlers).
In mathematical operation however, multiproccessing is preferred.
'''
