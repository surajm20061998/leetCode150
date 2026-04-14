#Intuition : Very basic Stack pop and add question
class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:

        def finalOpString(s):
            stack=[]
            for char in s:
                if char == '#' and stack:
                    stack.pop()
                elif char !='#':
                    stack.append(char)
            return stack

        return finalOpString(s)==finalOpString(t)