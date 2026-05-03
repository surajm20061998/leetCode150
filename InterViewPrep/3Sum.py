# Optimal Solution
# Time - O(n^2)
# Space - O(k) 
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        ans = set()
        print(nums)
        for i,a in enumerate(nums):
            l,r = i+1, len(nums)-1
            while(l<r):
                s = a+nums[l]+nums[r]
                if s>0:
                    r-=1
                elif s<0:
                    l+=1
                else:
                    ans.add((a,nums[l],nums[r]))
                    l+=1

        return list(ans)
        
# Better Solution, skipping duplicates
# Time - O(n^2)
# Space - O(k)       
class Solution:
    def threeSum(self, nums: list[int]) -> list[list[int]]:
        nums.sort()
        ans = []
        print(nums)
        for i,a in enumerate(nums):
            if i>0 and a==nums[i-1]:
                continue
            l,r = i+1, len(nums)-1
            while(l<r):
                s = a+nums[l]+nums[r]
                if s>0:
                    r-=1
                elif s<0:
                    l+=1
                else:
                    ans.append([a,nums[l],nums[r]])
                    l+=1
                    while nums[l] == nums[l-1] and l<r:
                        l+=1
        return ans