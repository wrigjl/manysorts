#!/usr/bin/env python
#
# Copyright (c) 2015, Jason L. Wright <jason@thought.net>
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# implementation of visualized merge sort

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
    t.daemon = True
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
