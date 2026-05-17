# My Initial Solution
class Solution:
    def kClosest(self, points: List[List[int]], k: int) -> List[List[int]]:

        ansdict = {}

        for i,p in enumerate(points):
            x=p[0]
            y=p[1]
            dist = (x**2 + y**2)**0.5
            ansdict[i] = dist
        sorted_keys = sorted(ansdict, key=ansdict.get)
        print(sorted_keys)
        ans = []
        for i in range(k):
            ans.append(points[sorted_keys[i]])
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

