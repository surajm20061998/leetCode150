# Sliding Window
# Same as Longest Repeating Charecter Replacement Question, but we only need to keep track of Zeroes
# At any point if number of Zeroes is more than K (shrink the window)
# Time Complexity = O(n)
# Space Complexity = O(1)
class Solution:
    def longestOnes(self, nums: List[int], k: int) -> int:
        countZeros = 0
        start = 0
        res = -1

        for end in range(len(nums)):
            if nums[end] == 0:
                countZeros+=1
            while countZeros > k:
                if nums[start] == 0:
                    countZeros-=1
                start+=1
            res = max(res, end-start+1)
        return res

        