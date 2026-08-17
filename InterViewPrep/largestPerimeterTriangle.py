# My inital solution
# Not optimal need to figure out the optimal solution

class Solution:
    def largestPerimeter(self, nums: List[int]) -> int:
        nums.sort()
        maxPerimeter = 0
        for i in range(len(nums)-2):
            a = nums[i]
            b = nums[i+1]
            c = nums[i+2]
            if a+b>c and b+c>a and a+c>b:
                maxPerimeter = max(maxPerimeter, a+b+c)
        return maxPerimeter
    

# Best Solution 
# Sort and look from back of the array, if there are 3 numbers that satisfy a+b>c then thats the ans since array is sorted
class Solution:
    def largestPerimeter(self, nums: List[int]) -> int:
        nums.sort()
        for i in range(len(nums)-3,-1,-1):
            if nums[i]+nums[i+1]>nums[i+2]:
                return nums[i]+nums[i+1]+nums[i+2]
        return 0
                

        