# Optimal Solution

class Solution:
    def decodeString(self, s: str) -> str:

        stack=[]

        for i in range(len(s)):
            if s[i] != "]":
                stack.append(s[i])
            else:
                #Loop to find the substring inside []
                substr = ""
                while stack and stack[-1]!="[":
                    substr = stack.pop()+substr
                #ppo out the [
                stack.pop()
                #Loop to find the number of times substring has to be repeated
                k=""
                while stack and stack[-1].isdigit():
                    k = stack.pop()+k
                #Append the substring k times to the stack 
                stack.append(int(k)*substr)
        return "".join(stack)


        