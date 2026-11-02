# O(N^2)
# Same as longest palindromic substring
# in a single for loop handle both the odd length and even length cases 

class Solution:
    def countSubstrings(self, s: str) -> int:
        res = 0

        for i in range(len(s)):
            l=r=i
            while l>=0 and r<len(s) and s[l] == s[r]:
                res+=1
                l-=1
                r+=1
            l=i
            r=i+1
            while l>=0 and r<len(s) and s[l] == s[r]:
                res+=1
                l-=1
                r+=1
        return res        