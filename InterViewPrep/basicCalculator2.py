# optimal solution

class Solution:
    def calculate(self, s: str) -> int:

        stack = []
        num = 0
        prevOp = "+"

        for i,c in enumerate(s):
            if c.isdigit():
                num=num*10+int(c)

            if c in "+-*/" or i==len(s)-1:
                if prevOp == "+":
                    stack.append(num)
                elif prevOp == "-":
                    stack.append(-num)
                elif prevOp == "*":
                    stack.append(stack.pop()*num)
                elif prevOp == "/":
                    stack.append(int(stack.pop()/num))
                prevOp = c
                num=0
        return sum(stack)
        