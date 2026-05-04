#Implement the MinStack class:

# MinStack() initializes the stack object.
# void push(int val) pushes the element val onto the stack.
# void pop() removes the element on the top of the stack.
# int top() gets the top element of the stack.
# int getMin() retrieves the minimum element in the stack.

#Idea is to treat it as a real stack and not just return min value always

#Store all elements as a stack of List where the list is structured as [val, minVal of the Stack]

#Rest all operations remain the same
class MinStack:

    def __init__(self):
        self.stack = []
        

    def push(self, val: int) -> None:
        minimum = val if not self.stack else min(val, self.stack[-1][1])
        self.stack.append([val,minimum])

    def pop(self) -> None:
        self.stack.pop()

    def top(self) -> int:
        return self.stack[-1][0]
        

    def getMin(self) -> int:
        return self.stack[-1][1]


# Your MinStack object will be instantiated and called as such:
# obj = MinStack()
# obj.push(val)
# obj.pop()
# param_3 = obj.top()
# param_4 = obj.getMin()