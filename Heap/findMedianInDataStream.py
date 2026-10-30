# My Solution -> Naive
class MedianFinder:

    def __init__(self):
        self.count = 0
        self.arr = []
        
    def addNum(self, num: int) -> None:
        self.arr.append(num)
        self.count+=1
        self.arr.sort()

    def findMedian(self) -> float:
        if self.count%2!=0:
            return self.arr[(self.count-1)//2]
        else :
            return (self.arr[(self.count-1)//2] + self.arr[((self.count-1)//2)+1])/2
        
        
# Better solution using 2 heaps, a maxHeap and a minHeap
class MedianFinder:

    def __init__(self):
        self.small = [] # Small Elements
        self.large = [] # Large Elements
        

    def addNum(self, num: int) -> None:
        heapq.heappush(self.small, -1*num)

        if (self.small and self.large and (-1* self.small[0]) > self.large[0]):
            val = -1*heapq.heappop(self.small)
            heapq.heappush(self.large, val)

        # check for uneven size
        if len(self.small) > len(self.large)+1:
            val = -1*heapq.heappop(self.small)
            heapq.heappush(self.large, val)
        if len(self.large) > len(self.small)+1:
            val = heapq.heappop(self.large)
            heapq.heappush(self.small, -1*val)


    def findMedian(self) -> float:
        if len(self.small) > len(self.large):
            return -1*self.small[0]
        elif len(self.large) > len(self.small):
            return self.large[0]
        else:
            return ((-1*self.small[0])+(self.large[0]))/2

