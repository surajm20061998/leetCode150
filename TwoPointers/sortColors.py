# Correct Solution
# Use 3 pointers
# l=0,i=0,r=n-1
# move i and everytime ele at i==0, swap with ele at l
# everytime ele at i==2, swap with ele at r

class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """

        l=0
        i=0
        r=len(nums)-1

        while i<=r:
            if nums[i]==0:
                nums[l],nums[i] = nums[i], nums[l]
                l+=1
                i+=1
            elif nums[i]==2:
                nums[i],nums[r] = nums[r], nums[i]
                r-=1
                 # Do not increment i because the swapped-in
                 # element has not been examined yet.
            else :
                i+=1


# My solution

class Solution:
    def sortColors(self, nums: List[int]) -> None:
        """
        Do not return anything, modify nums in-place instead.
        """
        #first put all twos in the end
        l=0
        for r in range(len(nums)):
            if nums[r]!=2:
                nums[l],nums[r]=nums[r],nums[l]
                l+=1
        #Then all the ones
        n=l
        l=0
        for r in range(n):
            if nums[r]!=1:
                nums[l],nums[r]=nums[r],nums[l]
                l+=1
        print(nums)
        #Then all the zeors
        #not required since 2s and 1s are in place 0s automatically fall in place 