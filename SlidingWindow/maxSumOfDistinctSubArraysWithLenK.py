# Sliding Window Problem
# Initial Solution - Not the best
class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:

        res = 0
        count = defaultdict(int)
        currSum = 0
        l = 0

        for r in range(len(nums)):
            currSum += nums[r]
            count[nums[r]] += 1
            if r-l+1 > k:
                count[nums[l]] -= 1
                if count[nums[l]]==0:
                    count.pop(nums[l])
                currSum -= nums[l]
                l+=1
            if r-l+1 == len(count) == k:
                res = max(res, currSum)
        return res
    

# Better Solution
# Using the last known position of current element
class Solution:
    def maximumSubarraySum(self, nums: List[int], k: int) -> int:

        res = 0
        prevIdx = {}
        curSum = 0
        l = 0
        for r in range(len(nums)):
            curSum += nums[r]
            i = prevIdx.get(nums[r], -1)
            while l<=i or r-l+1 > k:
                curSum -= nums[l]
                l+=1
            if r-l+1 == k:
                res = max(res,curSum)
            prevIdx[nums[r]] = r
        return res