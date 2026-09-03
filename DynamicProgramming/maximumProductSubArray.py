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