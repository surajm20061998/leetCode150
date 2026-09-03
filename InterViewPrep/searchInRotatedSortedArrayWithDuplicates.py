class Solution:
    def search(self, nums: List[int], target: int) -> int:
        ans = -1
        l,r = 0, len(nums)-1

        while l<=r:
            m = (l+r)//2

            if nums[m] == target:
                return True
            
            # In a rotated sorted array, either the left half or the right half will always be unsorted

            # Duplicates make it impossible to tell
            # Shrink the window in this case
            if nums[l] == nums[m] == nums[r]:
                l += 1
                r -= 1
                continue

            if nums[l] <= nums[m]:
                #left half is sorted
                if nums[l]<=target<nums[m]:
                    r = m-1
                else :
                    l = m+1
            
            else :
                #Righ half is sorted
                if nums[m]<target<=nums[r]:
                    l = m+1
                else :
                    r = m-1
        return False
        