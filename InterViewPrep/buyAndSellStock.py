# My 2nd Solution
# Pattern - Sliding Window / Two Pointers
# Data Structure - Array input, two pointers
# Time Complexity = O(n) 
# Space Complexity = O(1)
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        maxProf = 0
        l=0
        for r in range(1, len(prices)):
            if prices[l] > prices[r]:
                l=r
            else:
                maxProf = max(maxProf, prices[r]-prices[l])
        return maxProf
        

# Optimal Solution
# Time Complexity = O(n)
# Space Complexity = O(1)
class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        maxProf = 0
        currMin = prices[0]

        for price in prices:
            maxProf = max(maxProf, price-currMin)
            currMin = min(currMin, price)

        return maxProf
