# Sliding Window Problem
# Not the most efficient Solution
# Time Complexity = O(26*n)
# Space Complexity = O(k)
class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        count = {}
        start = 0
        res = -1

        for end in range(len(s)):
            count[s[end]] = 1 + count.get(s[end], 0)

            while (end-start+1) - max(count.values()) > k: # window condition
                count[s[start]] -= 1
                start+=1
            res = max(res, end-start+1)
        return res
