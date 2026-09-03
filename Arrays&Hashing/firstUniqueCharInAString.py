# Optimal Soultion
# Time Complexity - O(n)
# Space Complexity - O(n)
from collections import Counter
class Solution:
    def firstUniqChar(self, s: str) -> int:
        c = Counter(s)

        for i,ch in enumerate(s):
            if c[ch] == 1:
                return i

        return -1
        