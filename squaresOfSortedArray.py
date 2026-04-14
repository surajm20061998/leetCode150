#Intuition : Create an ans array res = [0,0,0,0,......]
#            L and R are 2 pointer for extreme Left and extreme Right of the nums array
#            Only the extreme elements will have bgger squares, 
#            Compare the abs of end elements and update result array backwards accordingly
class Solution:
    def sortedSquares(self, nums: List[int]) -> List[int]:
        res = [0]*len(nums)
        left = 0
        right = len(nums) -1

        for i in range(len(nums)-1,-1,-1):
            if abs(nums[left]) > abs(nums[right]):
                res[i] = nums[left]**2
                left+=1
            else:
                res[i] = nums[right]**2
                right-=1
        return res
        