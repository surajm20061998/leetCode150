# Dynamic Programming
# Time Cmplexity = O(n)
# Space Complexity = O(1)

# At each house, we choose:
# 1. Rob current house + best result from two houses before
# 2. Skip current house and keep best result from previous house
# recurrence:
# dp[i] = max(nums[i] + dp[i-2], dp[i-1])
class Solution:
    def rob(self, nums: List[int]) -> int:

        # we need two variables to decide our starting point
        # We can imagine our array as
        # [rob1, rob2, n, n+1, n+2 ........]
        rob1, rob2 = 0,0
        for n in nums:
            tmp = max(n+rob1,rob2)
            rob1 = rob2
            rob2 = tmp
            print(tmp, rob1, rob2)
        return rob2
        