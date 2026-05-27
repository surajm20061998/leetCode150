# My Solution
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:
        distList = [] # (dist, x,y)

        for x,y in points:
            dist = (x**2 + y**2)**0.5
            distList.append((dist,x,y))
        heapq.heapify(distList)
        ans = []
        for _ in range(k):
            tmpD,tmpX, tmpY = heapq.heappop(distList)
            ans.append([tmpX, tmpY])
        return ans
        


# Correct way to do it -> using a minheap
import heapq
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:

        ans = [] #dist,x,y

        for p in points:
            x,y = p[0], p[1]
            dist = dist = (x**2 + y**2)**0.5
            ans.append([dist,x,y])
        heapq.heapify(ans)
        res=[]
        while k>0:
            dist,x,y = heapq.heappop(ans)
            res.append([x,y])
            k-=1
        return res

