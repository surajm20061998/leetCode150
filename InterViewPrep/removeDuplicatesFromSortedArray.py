# Optimal Solution
# Keep 2 pointers l,r, both start at 1 since we dont need to move out Zeroeth element
# L keeps the position where the next unique element should land
# R keeps traversing the array to find these unique elements.
# In the end return L which basically points to the last unique element

class Solution:
    def removeDuplicates(self, nums: List[int]) -> int:
        l=1
        for r in range(1,len(nums)):
            if nums[r] != nums[r-1]:
                nums[l] = nums[r]
                l+=1
        return (l)
