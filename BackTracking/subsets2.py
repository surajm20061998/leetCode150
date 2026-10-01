# My solution
# based on subsets1 and combinationSum2
class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:

        nums.sort() # easy to identify duplicates and not take those decision paths

        res = []

        def dfs(start, subset):
            res.append(subset.copy())
            prev=float("-inf") # prev is for storing previously visited element so that we avoid dupicates
            for i in range(start, len(nums)):
                if nums[i]==prev:
                    continue
                # Once we have eliminated the duplicate scenario its the same problem as subsets1
                subset.append(nums[i])
                dfs(i+1, subset)
                subset.pop()
                prev = nums[i]
        dfs(0,[])
        return res
    
# Another way to solve it
class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:

        res = []
        nums.sort()

        def dfs(i, subset):
            if i == len(nums):
                res.append(subset.copy())
                return 
            # Chosing all subsets that include nums[i]
            subset.append(nums[i])
            dfs(i+1, subset)
            subset.pop()
            # Now need to choose all subsets that dont include nums[i] and duplicates
            while i+1<len(nums) and nums[i]==nums[i+1]:
                i+=1
            dfs(i+1, subset)
        dfs(0,[])
        return res

        
        