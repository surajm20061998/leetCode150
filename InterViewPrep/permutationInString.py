# Not the most optimal solution
# Time Complexity = O(n*mlogm)
# Space COmplexity = O(m)
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        winLen = len(s1)
        sortedS1 = ''.join(sorted(s1))
        for end in range(len(s2)-winLen+1):
            if ''.join(sorted(s2[end:end+winLen])) == sortedS1:
                return True
        return False
    

# Correct Solution or Optimal Solution
# CharSetSize - 26
# Time Complexity = O(n*CharSetSize)
# Space Complexity = O(charSetSize)
from collections import Counter
class Solution:
    def checkInclusion(self, s1: str, s2: str) -> bool:
        if len(s1) > len(s2):
            return False
        
        need = Counter(s1)
        window = Counter()
        winLen = len(s1)
        start = 0

        for end in range(len(s2)):
            window[s2[end]] += 1

            if (end - start + 1) > winLen:
                window[s2[start]] -= 1
                if window[s2[start]] == 0:
                    del window[s2[start]]
                start+=1
            
            if window == need:
                return True
        return False
        
        