# Optimal Soultion
# Time Complexity - O(n)
# Space Complexity - O(n)
from collections import Counter
class Solution:
    def canConstruct(self, ransomNote: str, magazine: str) -> bool:

        c = Counter(magazine)
        for ch in ransomNote:
            if ch not in c or c[ch]==0:
                return False
            
            c[ch]-=1
        
        return True

        