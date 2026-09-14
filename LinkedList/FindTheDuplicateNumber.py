# My Solution, naive approach

class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        visited = set()
        for n in nums:
            if n in visited:
                return n
            visited.add(n)
            
# Correct Solution
# using Floyd Warshall Fast and Slow Pointer approach

class Solution:
    def findDuplicate(self, nums: List[int]) -> int:
        slow, fast = 0,0
        while True:
            slow = nums[slow]
            fast = nums[nums[fast]]
            if slow == fast:
                break
        
        slow2 = 0
        while True:
            slow = nums[slow]
            slow2 = nums[slow2]
            if slow == slow2:
                return slow