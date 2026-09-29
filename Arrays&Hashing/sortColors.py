# Mistake I kept making was to keep incrementing i while decrementing r, in the case of nums[i] == 2, swap but dont increment i, the l pointer still needs to check swapped elements

class Solution:
    def sortColors(self, nums: list[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        l = 0
        r = len(nums)-1
        i = 0
        while i<=r:
            if nums[i] == 0:
                nums[i],nums[l] = nums[l], nums[i]
                l+=1
            elif nums[i] == 2:
                nums[i], nums[r] = nums[r], nums[i]
                r-=1
                i-=1
            i+=1

        #Put 0s in the front and 2s in the back

        