# Optimal Solution
# Time Complexity: O(n) 
# Space Complexity: O(1)
# Need to study again once more
class Solution:
    def maxAlternatingSum(self, nums: List[int]) -> int:
        sumEven, sumOdd = 0,0
        for i in range(len(nums)-1,-1,-1):
            tmpEven = max(sumOdd + nums[i], sumEven) # means max(pick nums[i] and add it to sumOdd, skip it)
            tmpOdd = max(sumEven - nums[i], sumOdd) # means max(pick nums[i] and subtract it from SumEven, skip it)
            sumEven, sumOdd = tmpEven, tmpOdd
        return sumEven # since at the start of the sequence chosen element is always added 