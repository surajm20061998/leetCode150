class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:

        ans = []

        def dfs(i, currList, total):
            if total == target:
                ans.append(currList.copy())
                return 
            
            if i>=len(nums) or total>target:
                return 

            currList.append(nums[i])
            dfs(i, currList, total+nums[i])
            currList.pop()
            dfs(i+1, currList, total)
        dfs(0,[],0)
        return ans
    
# Another way to do it 

class Solution:
    def combinationSum(self, nums: List[int], target: int) -> List[List[int]]:
        ans = []

        def dfs(start, curr, total):

            #baseCase
            if total == target:
                ans.append(curr.copy())
                return
            if total>target:
                return 

            for i in range(start,len(nums)):
                curr.append(nums[i])
                dfs(i, curr, total+nums[i])
                curr.pop()
        dfs(0,[],0)
        return ans
        