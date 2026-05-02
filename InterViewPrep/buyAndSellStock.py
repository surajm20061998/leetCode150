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
