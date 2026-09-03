# Optimal Solution
# Time - O(n)
# Space - O(k) where k is the length of the max sequence without repetiotion 
class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:

        seenSet = set()
        l=0
        res = 0
        for r in range(len(s)):
            
            while s[r] in seenSet:
                seenSet.remove(s[l])
                l+=1
            seenSet.add(s[r])
            res = max(res, r-l+1)
        return res


        