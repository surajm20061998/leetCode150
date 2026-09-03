class Solution:
    def evalRPN(self, tokens: List[str]) -> int:
        stack = []
        op = {
            '+' : lambda a,b : a+b,
            '-' : lambda a,b : a-b,
            '*' : lambda a,b : a*b,
            '/' : lambda a,b : int(a/b)
        }

        for t in tokens:
            if t in op:
                b = stack.pop()
                a = stack.pop()
                stack.append(op[t](a,b))
            else:
                stack.append(int(t))
        return stack.pop()
        