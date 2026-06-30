# Typical Stack Problem
# Everytime there is a # do stack.pop() else just keep adding to string
# Time Complexity: O(n + m)
# Space Complexity: O(n + m)

class Solution:
    def backspaceCompare(self, s: str, t: str) -> bool:
        def build(string):
            stack=[]
            for char in string:
                if char == "#":
                    if stack:
                        stack.pop()
                else:
                    stack.append(char)
            return stack
        return build(s) == build(t)