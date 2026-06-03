# Time Complexity: O(n)
# Space Complexity: O(1)
# Sliding Window
class Solution:
    def minSubArrayLen(self, target: int, nums: List[int]) -> int:
        l = 0
        summ = 0
        ans = float("inf")

        for r in range(len(nums)):
            summ += nums[r]

            if summ>=target:
                while(summ>=target):
                    ans = min(ans, r-l+1)
                    summ -= nums[l]
                    l+=1
                    
        return ans if ans!=float("inf") else 0