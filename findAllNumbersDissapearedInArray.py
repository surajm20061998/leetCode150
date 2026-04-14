#Intuition : For all the numbers (say index) present, mark nums[index] as negative, that way only the numbers that are
#            not present will have num[index] as positive values  

class Solution:
    def findDisappearedNumbers(self, nums: List[int]) -> List[int]:

        for num in nums:
            idx = abs(num) - 1
            if idx < len(nums):
                nums[idx] = -abs(nums[idx])
            
        ans = []

        for i,num in enumerate(nums):
            if num>0:
                ans.append(i+1)
        
        return ans