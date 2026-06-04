# Sliding Window + Frequency Map
# Time Complexity: O(n)
# Space Complexity: O(k)

from collections import defaultdict
class Solution:
    def longestKSubstr(self, s, k):
        if len(s) == 0 or k == 0:
            return -1

        start = 0
        freq = defaultdict(int)
        res = -1

        for end in range(len(s)):
            freq[s[end]] += 1

            while len(freq) > k:
                freq[s[start]] -= 1

                if freq[s[start]] == 0:
                    del freq[s[start]]

                start += 1

            if len(freq) == k:
                res = max(res, end - start + 1)

        return res if res!=0 else -1