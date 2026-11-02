# O(n^2) Solution
# For every element selected right to left we need to check the dp value of all the elements ahead of it
class Solution:
    def lengthOfLIS(self, nums: List[int]) -> int:
        dp = [1]*len(nums)
        for i in range(len(nums)-1, -1,-1):
            for j in range(i+1, len(nums)):
                if nums[i] < nums[j]:
                    dp[i] = max(dp[i], 1+dp[j])
        return max(dp)
                