class Solution:
    def subsets(self, nums: List[int]) -> List[List[int]]:
        res=[] # final result
        subset = []
        def dfs(i):
            if i>=len(nums): #boundary condition if we reach the end of our array then we just push copy of current subset to result
                res.append(subset.copy())
                return      
            #Decision 1 -> we decide to add nums[i] to the current subset
            subset.append(nums[i])
            dfs(i+1)
            #Decision 2 -> we decide to not add nums[i] to the current subset
            subset.pop()
            dfs(i+1)
        dfs(0)
        return res   