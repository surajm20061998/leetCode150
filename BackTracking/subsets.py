# Backtracking recursive solution
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        ans = [] # final ans
        subset = [] # array to build each subset
        def dfs(i):
            if i>=len(nums):
                ans.append(subset.copy())
                return
            subset.append(nums[i]) # Decision Tree -> Take the element and build subset
            dfs(i+1)
            subset.pop() # Decision Tree -> Dont take the element and build subset
            dfs(i+1)
        dfs(0)
        return ans
            
# Another way to solve it
class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        ans = []
        
        def dfs(start, subset):
            ans.append(subset.copy())
            for i in range(start, len(nums)):
                subset.append(nums[i])
                dfs(i+1, subset)
                subset.pop()
        dfs(0,[])
        return ans            
            
            
        