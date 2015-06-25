
import numpy
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pprint
import threading
import Queue
import copy

resQueue = Queue.Queue(10)
theArray = numpy.random.permutation(1000)

fig = plt.figure()
ax = plt.axes(xlim=(0, len(theArray)), ylim=(0, len(theArray)))
line, = ax.plot([], [], 'ro')

def init():
    line.set_data([], [])
    return line,

def update(num, aargs):
    if aargs['done']:
        return line,
    q = aargs['queue']
    a = q.get()
    if a is None:
        aargs['done'] = True
        return line,
    line.set_data(range(0, len(a)), a)
    q.task_done()
    return line,

aargs = {
    'queue': resQueue,
    'done': False
}
        
def sort_thread():
    do_qsort(resQueue, theArray, 0, len(theArray)-1)
    resQueue.put(None)

threads = []
for target in (sort_thread,):
    t = threading.Thread(target=target)
    threads.append(t)

def do_qsort(q, a, lo, hi):
    if lo < hi:
        p = partition(q, a, lo, hi)
        do_qsort(q, a, lo, p - 1)
        do_qsort(q, a, p + 1, hi)

def choose_pivot(q, a, lo, hi):
    return (lo + hi) / 2

def partition(q, a, lo, hi):
    pivotIndex = choose_pivot(q, a, lo, hi)
    pivotValue = a[pivotIndex]
    a[pivotIndex], a[hi] = a[hi], a[pivotIndex]
    q.put(copy.deepcopy(a))
    storeIndex = lo
    for i in xrange(lo, hi):
        if a[i] < pivotValue:
            a[storeIndex], a[i] = a[i], a[storeIndex]
            q.put(copy.deepcopy(a))
            storeIndex = storeIndex + 1
    a[storeIndex], a[hi] = a[hi], a[storeIndex]
    q.put(copy.deepcopy(a))
    return storeIndex

[t.start() for t in threads]

ani = animation.FuncAnimation(fig, update, blit=True, init_func=init,
                              fargs=(aargs,), interval=10)
plt.show()

[t.join() for t in threads]
