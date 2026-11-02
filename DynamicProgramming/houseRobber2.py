# much similar tohouse roober 1 just need to understand the helper and split condition
class Solution:
    def rob(self, nums: List[int]) -> int:
        if len(nums) == 1:
            return nums[0]
        def helper(nums):
            rob1, rob2 = 0, 0

            for n in nums:
                newRob = max(rob1+n, rob2)
                rob1 = rob2
                rob2 = newRob
            return rob2

        return max(helper(nums[:-1]), helper(nums[1:]))