class Solution:
    def nextGreaterElements(self, nums: List[int]) -> List[int]:
        n = len(nums)
        res = [-1] * n
        stack = []  # stores indices

        for i in range(2 * n):
            curr = nums[i % n]

            while stack and curr > nums[stack[-1]]:
                idx = stack.pop()
                res[idx] = curr

            if i < n:
                stack.append(i)

        return res