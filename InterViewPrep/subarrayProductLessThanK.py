# Two Pointer / Sliding Window
# Optimal Solution
# Time Complexity = O(n)
# Space Complexity = O(1)
class Solution:
    def numSubarrayProductLessThanK(self, nums: List[int], k: int) -> int:
        if k==0 : return 0
        count = 0
        prod = 1
        l = 0
        for r in range(len(nums)):
            prod*=nums[r]
            while l<=r and prod>=k:
                prod=prod//nums[l]
                l+=1
            
            count+=r-l+1
        return count        