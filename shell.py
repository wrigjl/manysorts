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

# implementation of visualized Shell sort

import argparse
import harness
import copy

def do_shell(q, a):
    gaps = gen_gaps(len(a))
    
    for gap in gaps:
        for i in xrange(0, gap):
            # insertion sort the gapped array
            r = range(i, len(a), gap)
            for j in xrange(1, len(r)):
                for k in xrange(j - 1, -1, -1):
                    if a[r[k + 1]] >= a[r[k]]:
                        break
                    a[r[k]], a[r[k + 1]] = a[r[k + 1]], a[r[k]]
                    q.put(copy.deepcopy(a))

def gen_gaps(alen):
    '''Generate gaps based on Sedgewick 1986 (O(N**4/3))
       1, 8, 23, 77, 281, ...
    '''
    k = 1
    gaps = [1]
    while gaps[-1] < alen:
        gaps.append(4 ** k + 3 * (2 ** (k - 1)) + 1)
        k = k + 1
    gaps.reverse()
    return gaps

def gen_gaps(alen):
    '''Generate gaps based on Hibbard, 1963 (O(N**3/2)).
       1, 3, 7, 15, 31, 63, ...
    '''
    k = 1
    gaps = []
    while True:
        n = (1 << k) - 1
        if n >= alen:
            break
        gaps.append(n)
        k = k + 1
    gaps.reverse()
    return gaps

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--len', type=int, help="length of array",
                        required=False, default=100)
    args = parser.parse_args()
    harness.SortHarness(do_shell, args.len).go()
