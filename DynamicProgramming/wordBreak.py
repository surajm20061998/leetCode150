# Set dp array to size of s+1 and mark all as false
# Set dp of last element to be true since we know that can be reached.
# From the end of the string check for Recurrence realtion -> dp[i] = dp[i+len(w)]

# Time Complexity - O(N × M × L)

class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> bool:
        dp = [False]*(len(s)+1)
        dp[len(s)] = True

        for i in range(len(s)-1, -1, -1):
            for w in wordDict:
                if (i+len(w)) <= len(s) and s[i:i+len(w)] == w:
                    dp[i] = dp[i+len(w)]
                if dp[i]:
                    break
        return dp[0]
        