# My Solution
from collections import Counter
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        countMap = Counter(nums)
        countList = [] # (count, num)
        for key, val in countMap.items():
            countList.append((-1*val,key))
            ans = []
        heapq.heapify(countList)
        for _ in range(k):
            tmpC, tmpN = heapq.heappop(countList)
            ans.append(tmpN)
        return ans
       
# Optimal Solution - Not Sure
# Time Complexity - O(nlogk)
# Space Complexity - O(n)
from collections import Counter
class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counter = Counter(nums)
        return [i[0] for i in counter.most_common(k)]
        