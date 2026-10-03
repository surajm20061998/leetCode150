class Solution:
    def wordBreak(self, s: str, wordDict: List[str]) -> List[str]:
        wordDict = set(wordDict)
        def dfs(i):
            if i==len(s):
                return [""]
            
            res = []
            for j in range(i, len(s)):
                w = s[i:j+1]
                if w not in wordDict:
                    continue
                strings = dfs(j+1)
                if not strings:
                    continue
                for substring in strings:
                    sentence = w
                    if substring:
                        sentence += " " + substring
                    res.append(sentence)
            return res
        return dfs(0)