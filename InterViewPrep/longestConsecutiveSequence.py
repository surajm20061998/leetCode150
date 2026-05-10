#Optimal Solution
#TIme Complexity - O(n)
#Space COmplexity - O(n)
# basic idea is to create a set out of the nums list and then pick a number from set and 
# keep checking if n-1 not in set and n+length in set, and longest length is the final answer
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        numSet = set(nums)
        longest = 0
        for n in numSet:
            if n-1 not in numSet:
                length = 0
                while(n+length) in numSet:
                    length+=1
                longest = max(longest, length)
        return longest