# Need to check this again
class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        res = []
        digitToChar = {
            "2": "abc",
            "3": "def",
            "4": "ghi",
            "5": "jkl",
            "6": "mno",
            "7": "qprs",
            "8": "tuv",
            "9": "wxyz",
        }

        def dfs(i, currStr):
            if len(currStr) == len(digits):
                res.append(currStr)
                return
            for c in digitToChar[digits[i]]:
                dfs(i+1, currStr+c)
        if digits:
            dfs(0, "")
        return res
