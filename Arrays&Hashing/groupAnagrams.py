# Optimal TIme 
# Time Comlexity - O(n * k log k)
# Space Complexity - O(n * k)
from collections import defaultdict
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:

        D = defaultdict(list)
        for s in strs:
            key = ''.join(sorted(s))
            D[key].append(s)
        return list(D.values())