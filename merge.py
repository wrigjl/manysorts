
import numpy
import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import pprint
import threading
import Queue
import copy
import random

resQueue = Queue.Queue(10)
#theArray = numpy.random.permutation(1000)
theArray = range(1000)
random.shuffle(theArray)

#theArray = [54, 26, 93, 17, 77, 31, 44, 55, 20]

fig = plt.figure()
ax = plt.axes(xlim=(0, len(theArray)), ylim=(0, len(theArray)))
line, = ax.plot([], [], 'ro')

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
        q.task_done()
        return

    line.set_data(range(0, len(a)), a)
    q.task_done()
    return line,

aargs = {
    'queue': resQueue,
    'done': False
}
        
def sort_thread():
    do_merge(resQueue, theArray, copy.deepcopy(theArray), 0)
    pprint.pprint(theArray)
    resQueue.put(None)

threads = []
for target in (sort_thread,):
    t = threading.Thread(target=target)
    threads.append(t)

def do_merge(q, a, Z, base):
    if len(a) == 1:
        return a
    m = len(a) / 2
    l = do_merge(q, a[:m], Z, 0)
    r = do_merge(q, a[m:], Z, m)
    
    if not len(l) or not len(r):
        return l or r

    result = []
    i = j = 0
    while len(result) < len(r)+len(l):
        if l[i] < r[j]:
            result.append(l[i])
            i = i + 1
        else:
            result.append(r[j])
            j = j + 1
        if i == len(l) or j == len(r):
            result.extend(l[i:] or r[j:])
            break

    for i in xrange(len(result)):
        Z[base + i] = result[i]
        q.put(copy.deepcopy(Z))

    return result

[t.start() for t in threads]

ani = animation.FuncAnimation(fig, update, fargs=(aargs,), interval=10,
                              init_func=init, blit=True)
plt.show()

[t.join() for t in threads]
