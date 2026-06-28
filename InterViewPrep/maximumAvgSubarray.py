#Sliding Window
class Solution:
    def findMaxAverage(self, nums: List[int], k: int) -> float:
        l=0
        msum = sum(nums[:k])
        ans = msum

        for r in range(k, len(nums)):
            msum+=nums[r]
            msum-=nums[l]
            l+=1
            ans = max(ans,msum)
        return ans/k