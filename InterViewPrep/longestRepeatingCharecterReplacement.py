# Sliding Window Problem
# Not the most efficient Solution
# Time Complexity = O(26*n)
# Space Complexity = O(k)
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        # Validity condition -> windowLen - countOfMostFrequent <= k
        # Expand window till validity condition 
        # Then slide the window

        freq = {}
        l=0
        res = -1
        for r in range(len(s)):
            freq[s[r]] = 1 + freq.get(s[r],0)
            while ((r-l+1) - max(freq.values())) > k:
                freq[s[l]]-=1
                l+=1
            res = max(res, r-l+1)
        return res if res!=-1 else 1
        
