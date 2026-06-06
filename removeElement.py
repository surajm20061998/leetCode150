# Two Pointer
# l points to the next position where a valid element should be placed.
# r scans every element.
# If nums[r] != val, copy it to nums[l] and move l forward.
# At the end, l is the number of elements not equal to val.
# Time Complexity = O(n)
# Space Complexity = O(1)
class Solution:
    def removeElement(self, nums: List[int], val: int) -> int:
        l=0
        for r in range(len(nums)):
            if nums[r]!=val:
                nums[l] = nums[r]
                l+=1
        return l

        