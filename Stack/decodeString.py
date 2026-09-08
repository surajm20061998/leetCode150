# Optimal Solution
# If charecter is not "]" keep putting in stack
# else - traverse stack till "[" to find the substring
#        pop the "["
#        traverse the stack and stack.pop() till stack[-1] is digit to find k
#        Once we have k and substring , push k*substring to the stack
# Repeat till end of string
#return

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
                #pop out the [
                stack.pop()
                #Loop to find the number of times substring has to be repeated
                k=""
                while stack and stack[-1].isdigit():
                    k = stack.pop()+k
                #Append the substring k times to the stack 
                stack.append(int(k)*substr)
        return "".join(stack)


        