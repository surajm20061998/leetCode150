# Trie + DP problem, need to check this again

class TrieNode:
    def __init__(self):
        self.children = {}
        self.endOfWord = False


class Solution:
    def minExtraChar(self, s: str, dictionary: List[str]) -> int:

        # Build Trie
        root = TrieNode()

        for word in dictionary:
            curr = root

            for ch in word:
                if ch not in curr.children:
                    curr.children[ch] = TrieNode()

                curr = curr.children[ch]

            curr.endOfWord = True

        memo = {}

        def dfs(i):
            # No characters remaining
            if i == len(s):
                return 0

            if i in memo:
                return memo[i]

            # Option 1:
            # Treat s[i] as an extra character
            res = 1 + dfs(i + 1)

            # Option 2:
            # Try every dictionary word starting at i
            curr = root

            for j in range(i, len(s)):

                if s[j] not in curr.children:
                    break

                curr = curr.children[s[j]]

                if curr.endOfWord:
                    res = min(res, dfs(j + 1))

            memo[i] = res
            return res

        return dfs(0)