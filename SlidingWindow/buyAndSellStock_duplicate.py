# N^2 solution -> need to find a better way
class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        n = len(prices)

        m = 0

        for i in range(n-1):
            for j in range(i+1,n):
                m = max(m, (prices[j]-prices[i]))

        return m
    

# Better Solution 
# Intuition - > Consider every day as sell day, we need to keep a running minimum of all elements till sell day
class Solution:
    def maxProfit(self, prices: List[int]) -> int:

        m = 0
        currMin = prices[0]

        for price in prices:
            m = max(m,(price-currMin))
            currMin = min(currMin, price)
        return m
