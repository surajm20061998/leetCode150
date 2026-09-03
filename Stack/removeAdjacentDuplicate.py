# Very similiar to asteroid collision question
class Solution:
    def removeDuplicates(self, s: str) -> str:
        stack = []

        for ch in s:
            if not stack:
                stack.append(ch)
            else:
                if stack[-1]==ch:
                    while stack and stack[-1]==ch:
                        stack.pop()
                else:
                    stack.append(ch)

        return ''.join(stack)
        