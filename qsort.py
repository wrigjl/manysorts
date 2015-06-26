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

# implementation of visualized quick sort

import argparse
import harness
import copy

def do_qsort(q, a, lo=None, hi=None):
    if lo is None:
        lo = 0
    if hi is None:
        hi = len(a) - 1
        
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--len', type=int, help="length of array",
                        required=False, default=100)
    args = parser.parse_args()
    harness.SortHarness(do_qsort, args.len).go()
