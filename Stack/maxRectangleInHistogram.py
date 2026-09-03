# Need to understand this better
# Optimal
# Time Complexity = O(n)
# Space Complexity = O(n) 

class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:

        maxArea = 0

        stack=[]

        for i,h in enumerate(heights):
            start = i
            while stack and stack[-1][1]>h:
                index,height = stack.pop()
                maxArea = max(maxArea, height*(i-index))
                start = index
            stack.append([start, heights[i]])

        for i,h in stack:
            maxArea = max(maxArea, h*(len(heights)-i))
        return maxArea