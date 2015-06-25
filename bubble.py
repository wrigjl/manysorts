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

# implementation of visualized bubble sort

import matplotlib
matplotlib.use('TKAgg')
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
import Queue
import copy
import random

resQueue = Queue.Queue(10)
theArray = range(100)
random.shuffle(theArray)

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
        return
    line.set_data(range(0, len(a)), a)
    q.task_done()
    return line,

aargs = {
    'queue': resQueue,
    'done': False
}
        
def sort_thread():
    do_bubble(resQueue, theArray)
    resQueue.put(None)

threads = []
for target in (sort_thread,):
    t = threading.Thread(target=target)
    t.daemon = True
    threads.append(t)

def do_bubble(q, a):
    for j in range(len(a) - 1, -1, -1):
        swapped = False
        for i in range(0, j):
            if a[i] <= a[i + 1]:
                continue
            a[i], a[i + 1] = a[i + 1], a[i]
            q.put(copy.deepcopy(a))
            swapped = True
        if not swapped:
            return

[t.start() for t in threads]

ani = animation.FuncAnimation(fig, update, fargs=(aargs,), init_func=init,
                              blit=True, interval=10)
plt.show()
