# Optimal Solution
# TIme Complexity : O(n)
# Space Complexity : O(1)

class Solution:
    def maxArea(self, height: List[int]) -> int:
        l=0
        r=len(height)-1
        maxArea = (min(height[l],height[r])*(r-l))

        while(l<r):
            if height[l]<=height[r]:
                l+=1
            else:
                r-=1

            maxArea = max(maxArea, (min(height[l],height[r])*(r-l)))

        return maxArea          