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
