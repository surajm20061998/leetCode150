# Naive Solution
# Time Complexity -> O(n^2)
# Space Complexity -> O(1)
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        for i in range(len(nums)-1):
            for j in range(i+1, len(nums)):
                if nums[i]+nums[j]==target:
                    return [i,j]
        
# Optimised Solution
# TIme Complexity -> O(n)
# Space Complexity -> O(n)
class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        numToIndex={}

        for i,num in enumerate(nums):
            if target-num in numToIndex:
                return [numToIndex[target-num], i]
            numToIndex[num] = i
        

        