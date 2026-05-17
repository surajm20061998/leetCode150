# Dynamic Programming
# Time Cmplexity = O(n)
# Space Complexity = O(n)
# Basically the pattern shows Fibonacci Sequence
class Solution:
    def climbStairs(self, n: int) -> int:
        ans = [0,1,2,3]

        if n>=3:
            for i in range(3,n):
                ans.append(ans[i]+ans[i-1])
                print(ans)
        return ans[n]
         