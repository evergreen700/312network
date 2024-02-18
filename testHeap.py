#!/usr/bin/python3

from PriorityQueue import *
import time
import random

reps = 1000000
testArray = PQueueHeap()

for i in range(reps):
    testArray.insert(random.random())

t1 = time.time()
testArray.delete_min()
t2 = time.time()
print('Total time: %s' % ((t2-t1)))

