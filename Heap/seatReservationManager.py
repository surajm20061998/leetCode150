# My initial solution , dont think its efficient
import heapq
class SeatManager:

    def __init__(self, n: int):
        self.minHeap = [i for i in range(1,n+1)]

    def reserve(self) -> int:
        if len(self.minHeap)>0:
            return heapq.heappop(self.minHeap)
        

    def unreserve(self, seatNumber: int) -> None:
        heapq.heappush(self.minHeap, seatNumber)
        


# Your SeatManager object will be instantiated and called as such:
# obj = SeatManager(n)
# param_1 = obj.reserve()
# obj.unreserve(seatNumber)

# Better Solution 
# Dont just dump everything to a heap
# use a pointer to point to the next available seat and then just use that to reserve next seat
# When a seat is unreserved then add that to the minHeap and check minHeap before booking next seat
import heapq
class SeatManager:

    def __init__(self, n: int):
        self.nextSeat = 1
        self.minHeap = []

    def reserve(self) -> int:
        if len(self.minHeap)>0:
            return heapq.heappop(self.minHeap)
        seat = self.nextSeat
        self.nextSeat+=1
        return seat

    def unreserve(self, seatNumber: int) -> None:
        heapq.heappush(self.minHeap, seatNumber)
        


# Your SeatManager object will be instantiated and called as such:
# obj = SeatManager(n)
# param_1 = obj.reserve()
# obj.unreserve(seatNumber)