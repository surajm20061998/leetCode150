# Brute Force Solution
# For every height given, maintain maxLeftHeight(L) and MaxRightHeight(L)
# Then for every given height we do (min(L,R) - h[i]) if (min(L,R) - h[i]) > 0 else 0
class Solution:
    def trap(self, height: List[int]) -> int:

        n = len(height)
        maxLeftHeight = [0]*n
        maxRightHeight = [0]*n
        minLRHeight = [0]*n
        trap = [0]*n

        for i in range(1, n):
            maxLeftHeight[i] = max(maxLeftHeight[i-1], height[i-1])

        for i in range(n-2,-1,-1):
            maxRightHeight[i] = max(maxRightHeight[i+1], height[i+1])

        for i in range(n):
            minLRHeight[i] = min(maxLeftHeight[i], maxRightHeight[i])

        for i in range(n):
            trap[i] = (minLRHeight[i] - height[i]) if (minLRHeight[i] - height[i] > 0) else 0

        return sum(trap)
        