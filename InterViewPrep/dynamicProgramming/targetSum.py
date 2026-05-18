class Solution:
    def findTargetSumWays(self, nums: List[int], target: int) -> int:
        dp={} # to store (index,total) -> number of ways
        def backtracking(i,total):
            if i == len(nums): #base case -> we have reached the end of the array
                return 1 if total==target else 0
            if (i,total) in dp: #base case -> pair already exists in cache and we just need to return its value
                return dp[(i,total)]
            #Recursive case
            #At every step we have a choice that is to add or subtract nums[i] fromt total
            #We just need to get the sum of both of these decisions at every element
            dp[i,total] = backtracking(i+1, total+nums[i]) + backtracking(i+1, total-nums[i])
            return dp[(i,total)]
        return backtracking(0,0)