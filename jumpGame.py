# Intuition - > Run the array backwards, target being your last element
# if at any index i, nums[i]+i>=target -> set i as new target
#in the end return if target==0
class Solution:
    def canJump(self, nums: List[int]) -> bool:

        n = len(nums)
        g = n-1

        for i in range(n-2,-1,-1):
            if g<=nums[i]+i:
                g=i
            
        
        return g==0
            

        