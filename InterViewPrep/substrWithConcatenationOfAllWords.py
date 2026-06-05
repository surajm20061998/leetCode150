# Optimal Solution
# Need to study this again
# Time Complexity = O(n)
# Space COmplexity = O(m)

# In a nutshell - 
# If current word is valid:
#     add it to the window
#     shrink only if we have too many copies of that word
#     if window has all required words, record answer
# If current word is invalid:
#     reset the window.

from collections import Counter, defaultdict
class Solution:
    def findSubstring(self, s: str, words: List[str]) -> List[int]:
        if not s or not words:
            return []

        wordLen = len(words[0])
        numWords = len(words)
        windowLen = wordLen*numWords
        wordCount = Counter(words)

        ans = []

        for offset in range(wordLen):
            left = offset
            seen = defaultdict(int)
            count = 0
            for right in range (offset, len(s)-wordLen+1, wordLen):
                word = s[right:right+wordLen]

                if word in wordCount:
                    seen[word] += 1
                    count += 1

                    while seen[word] > wordCount[word]:
                        leftWord = s[left:left+wordLen]
                        seen[leftWord] -= 1
                        count -= 1
                        left+=wordLen
                    if count == numWords:
                        ans.append(left)
                else:
                    seen.clear()
                    count = 0
                    left = right+wordLen
        return ans


