# Worst Solution possible
# Need to find a better solution
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:

        p=''.join(sorted(p))
        n=len(p)
        output = []
        for i in range(len(s)-n+1):
            if (''.join(sorted(s[i:i+n])) == p):
                output.append(i)
        return output

# Better or Optimal Solution 
# CharSetSize = 26
# Time Complexity = O(n*CharSetSize) 
# Space Complexity = O(charSetSize)
from collections import Counter
class Solution:
    def findAnagrams(self, s: str, p: str) -> List[int]:
        if len(p) > len(s) :
            return []
        
        ans = []
        need = Counter(p)
        window = Counter()
        winLen = len(p)
        start = 0

        for end in range(len(s)):
            window[s[end]] += 1

            if (end - start + 1) > winLen:
                window[s[start]] -= 1
                if window[s[start]] == 0:
                    del window[s[start]]
                start+=1
            if window == need:
                ans.append(start)
        return ans

        