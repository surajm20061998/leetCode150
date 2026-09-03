# Linear Time Solution
# Need to understad this better
class Solution:
    def subarraySum(self, nums: List[int], k: int) -> int:
        count = 0
        hmap = {0:1} #-> {prefix, count}
        #Initally add 0,1
        prefixSum = 0
        for n in nums:
            prefixSum+=n
            diff = prefixSum-k
            count+=hmap.get(diff,0)
            hmap[prefixSum] = 1+hmap.get(prefixSum,0)
        return count
