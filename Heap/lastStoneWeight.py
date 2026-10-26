# Naive Solution by just sorting the array everytime
class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        stones.sort()
        while len(stones)>1:
            print(stones)
            x,y = stones.pop(), stones.pop()
            if x!=y:
                stones.append(abs(x-y))
                stones.sort()
        return stones[0] if len(stones)>0 else 0
    
# Better solution using minheap
import heapq
class Solution:
    def lastStoneWeight(self, stones: List[int]) -> int:
        minHeap = [-x for x in stones]
        heapq.heapify(minHeap)
        while len(minHeap)>1:
            print(minHeap)
            x, y = heapq.heappop(minHeap), heapq.heappop(minHeap)
            if x!=y:
                heapq.heappush(minHeap, x-y)
        return -1*minHeap[0] if len(minHeap)>0 else 0
