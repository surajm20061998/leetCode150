# Naive Solution - TLEd
# Time Complexity - O(n^2)ish
# Space Complexity - O(n)
class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:

        n = len(temperatures)
        ans = [0]*n

        for i in range(n-1):
            for j in range(i+1,n):
                if temperatures[j] > temperatures[i]:
                    ans[i] = j-i
                    break

        return ans


#Optimal Solution
#Time Complexity - O(n)
#Space Complexity - O(n)

class Solution:
    def dailyTemperatures(self, temperatures: List[int]) -> List[int]:

        res=[0]*len(temperatures)
        stack = [] # pair [temp,index]

        for i,t in enumerate(temperatures):
            while stack and t>stack[-1][0]:
                stackT,stackInd = stack.pop()
                res[stackInd] = (i-stackInd)
            stack.append([t,i])
        return res
        