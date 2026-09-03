# Optimal Solution
# Using a monotonic decreasing stack
class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        nums1Idx = {n:i for i,n in enumerate(nums1)}
        res = [-1]*len(nums1)
        stack=[]

        for i in range(len(nums2)):
            curr = nums2[i]
            while stack and curr>stack[-1]:
                val = stack.pop() # curr is the next greates element of val or of stack.top()
                idx = nums1Idx[val]
                res[idx] = curr

            if curr in nums1Idx: # base condition of adding elemet to stack
                stack.append(curr)
        return res


#Not optimal, need to see solution with monotonic stack
class Solution:
    def nextGreaterElement(self, nums1: List[int], nums2: List[int]) -> List[int]:
        hmap = {n:-1 for n in nums2}
        for i in range(len(nums2)-1):
            for j in range(i+1,len(nums2)):
                if nums2[j]>nums2[i]:
                    hmap[nums2[i]] = nums2[j]
                    break

        ans = []

        for num in nums1:
            ans.append(hmap[num])
        return ans

        