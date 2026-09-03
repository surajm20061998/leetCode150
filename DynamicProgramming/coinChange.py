# Dynamic Programming
# Time complexity = O(amount*c)
# Space Complexity = O(amount)
# Need to study again
class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        dp = [amount+1]*(amount+1) # Initialize dp array of size amount+1 (0->amt index) and value infinity (or greater than amount)
        dp[0] = 0 # It takes 0 coins to get to a sum of 0
        for a in range(1,amount+1):
            for c in coins:
                print(dp)
                if a-c>=0:
                    dp[a] = min(dp[a], 1+dp[a-c])
        return dp[amount] if dp[amount]!=amount+1 else -1



        