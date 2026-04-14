#intuiton : two pointers L,R
#           if nums[R] is not zero -> swap nums[L] and nums[R] and increment L 
#           else only more R and keep L as is

class Solution:
    def moveZeroes(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        l=0
        for r in range(len(nums)):
            if nums[r]!=0:
                nums[r],nums[l] = nums[l],nums[r]
                l+=1