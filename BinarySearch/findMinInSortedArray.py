# my solution
# intuition - Keep doing a binary search over the entire array, and keep storing min([ans, nums[l], nums[r], nums[m]])
class Solution:
    def findMin(self, nums: List[int]) -> int:
        l,r = 0, len(nums)-1
        ans = nums[-1]
        while l<=r:
            m = (l+r)//2
            print(nums[l], nums[r], nums[m])
            ans = min([ans, nums[l], nums[r], nums[m]])
            if nums[r] < nums[m]:
                l = m+1
            else :
                r = m-1
        return ans
        
        