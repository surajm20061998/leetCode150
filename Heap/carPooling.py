class Solution:
    def carPooling(self, trips: List[List[int]], capacity: int) -> bool:
        minHeap = [] # pair of [end, numPassengers]
        currPass = 0
        trips.sort(key = lambda t:t[1])
        for t in trips:
            numPass, start, end = t
            while minHeap and minHeap[0][0] <= start:
                currPass -= minHeap[0][1]
                heapq.heappop(minHeap)
            currPass += t[0]
            if currPass > capacity:
                return False
            heapq.heappush(minHeap, [end, numPass])
        return True
        