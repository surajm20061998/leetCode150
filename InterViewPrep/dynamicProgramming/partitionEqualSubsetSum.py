class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        if sum(nums)%2!=0:
            return False
        
        dp=set() # Stores all subset sums that are currently possible
        dp.add(0)
        target = sum(nums)//2 # We only need to find if some subset can make this target sum
        for i in range(len(nums)-1,-1,-1):
            nextDp = set()
            for t in dp:
                # For each existing posible sum in dp we have a choice to add nums[i] or skip
                nextDp.add(t+nums[i])
                nextDp.add(t)
            dp = nextDp # update dp with all the possible sums currently possible
        return True if target in dp else False