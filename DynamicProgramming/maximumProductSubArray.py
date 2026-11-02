# Need to review this again

class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        res = nums[0]
        currMax = nums[0]
        currMin = nums[0]

        for n in nums[1:]:
            candidates = (n, currMax*n, currMin*n)
            currMax = max(candidates)
            currMin = min(candidates)
            res = max(res,currMax)
        return res
    
# Saw it again -> 
class Solution:
    def maxProduct(self, nums: List[int]) -> int:
        # Maintain the maximum and minimum possible subarray product for each element
        res = max(nums)
        currMin, currMax = 1,1

        for n in nums:
            tmp = currMax*n
            currMax = max(n*currMax, n*currMin, n)
            currMin = min(tmp, n*currMin, n)
            res = max(currMax, res)
        return res
        