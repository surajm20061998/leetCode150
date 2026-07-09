# O(n) time solution but space is in the order of O(n) too
# Need to find a space optimal solution

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n=len(nums)
        prefArr = [1]*n
        sufArr = [1]*n

        for i in range(1,len(nums)):
            prefArr[i] = prefArr[i-1]*nums[i-1]

        for i in range(len(nums)-2,-1,-1):
            sufArr[i] = sufArr[i+1]*nums[i+1]

        ans = []

        for i in range(len(nums)):
            ans.append(prefArr[i]*sufArr[i])
        
        print(prefArr, sufArr, ans)
        return ans
        
        
# Rightway to do it
# Instead of 2 different arrays do 2 different passes
# Forward pass to compute prefix product and backward pass to compute postfix product

class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n=len(nums)
        prefix = 1
        ans = []
        for i in range(len(nums)):
            ans.append(prefix)
            prefix = prefix*nums[i]
        postfix = 1
        for i in range(len(nums)-1,-1,-1):
            ans[i] = ans[i]*postfix
            postfix = postfix*nums[i]
        return(ans)
