# O(n*m)
# Heap Solution
# Need to understand
from collections import Counter
import heapq
class Solution:
    def leastInterval(self, tasks: List[str], n: int) -> int:
        count = Counter(tasks)
        maxHeap = [-cnt for cnt in count.values()] # Since we want to make sure the most frequent tasks are picked first to reduce idle time
        heapq.heapify(maxHeap)

        time = 0
        q = deque()

        while maxHeap or q:
            time+=1
            if maxHeap:
                cnt = 1+heapq.heappop(maxHeap) # processing this task so reduce the count (since count is negative increase it)
                if cnt!=0: # more executions left
                    q.append([cnt, time+n])
            if q and q[0][1] == time: # if q.popleft() item has the processTime equal to current time then pust into the maxHeap else idle condition
                heapq.heappush(maxHeap, q.popleft()[0])
        return time

        