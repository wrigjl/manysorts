
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
theArray = numpy.random.permutation(100)

fig = plt.figure()
ax = plt.axes(xlim=(0, len(theArray)), ylim=(0, len(theArray)))
line, = ax.plot(range(0, len(theArray)), theArray, 'ro')

def init():
    line.set_data([], [])
    return line,

def update(num, aargs):
    if aargs['done']:
        return
    q = aargs['queue']
    a = q.get()
    if a is None:
        aargs['done'] = True
        return
    line.set_data(range(0, len(a)), a)
    q.task_done()
    return line,

aargs = {
    'queue': resQueue,
    'done': False
}
        
def sort_thread():
    do_insertion(resQueue, theArray)
    resQueue.put(None)

threads = []
for target in (sort_thread,):
    t = threading.Thread(target=target)
    threads.append(t)

def do_insertion(q, a):
    for n in range(1, len(a)):
        for i in range(n - 1, -1, -1):
            if a[i + 1] >= a[i]:
                break
            a[i], a[i + 1] = a[i + 1], a[i]
            q.put(copy.deepcopy(a))
    q.put(None)

[t.start() for t in threads]

ani = animation.FuncAnimation(fig, update, fargs=(aargs,), interval=10,
                              init_func=init, blit=True)
plt.show()

[t.join() for t in threads]
