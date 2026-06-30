# Two Pointer + Sorting
# Time Complexity = O(n^2)
# Space Complexity = O(1) aux space
class Solution:
    def threeSumClosest(self, nums: List[int], target: int) -> int:
        nums.sort()
        closest  = nums[0] + nums[1] + nums[2]

        for k in range(len(nums)-2):
            l = k+1
            r = len(nums)-1

            while(l<r):
                currentSum = nums[k]+nums[l]+nums[r]
                if abs(currentSum - target) < abs(target - closest):
                    closest = currentSum

                if currentSum < target:
                    l+=1
                elif currentSum > target:
                    r-=1
                else:
                    return target
        return closest