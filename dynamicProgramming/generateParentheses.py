# Dynamic Programming
# backtracking
# Need to do more questions to understand backtracking
class Solution:
    def generateParenthesis(self, n: int) -> List[str]:
        res = []
        stack = []

        def backTrack(openCount, closedCount):

            # BASE CASE:
            # Used all n opening and n closing parentheses.
            # We have a complete valid answer.
            if openCount == closedCount == n:
                res.append("".join(stack))
                return

            # CHOICE 1:
            # Add "(" if we still have opening parentheses available.
            if openCount < n:
                stack.append("(")

                # EXPLORE
                backTrack(openCount + 1, closedCount)

                # UNDO
                stack.pop()

            # CHOICE 2:
            # Add ")" only if there is an unmatched "(" to close.
            if closedCount < openCount:
                stack.append(")")

                # EXPLORE
                backTrack(openCount, closedCount + 1)

                # UNDO
                stack.pop()

        backTrack(0, 0)

        return res