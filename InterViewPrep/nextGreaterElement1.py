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

        