# Brute Force Solution
class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:
        if not nums:
            return 0
        nums.sort()
        maxLength = 0
        length = 0
        print(nums)
        for i in range(len(nums)-1):
            if nums[i]+1 == nums[i+1]:
                length+=1
                maxLength = max(maxLength, length)
                print(length, maxLength)
            elif nums[i] == nums[i+1]:
                continue
            else:
                length = 0

        return maxLength+1
                
        

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
            if n-1 not in numSet: #This means that we have hit a number that can potentially be a start of a given sequence
                length = 0
                while(n+length) in numSet: # We have the start of sequence now we just need to keep incrementing by 1 
                                           # and keep checking if we have the next element of the sequence in the set
                    length+=1
                longest = max(longest, length)
        return longest