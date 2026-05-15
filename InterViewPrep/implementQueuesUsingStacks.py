# Optimal Solution
# Jist of it is, use 2 stacks, iniitialize 2 stacks, during push -> simply push to stack1
#                                                    during pop and peek -> push to stack2 while popping from stack1
#                                                    for empty check -> simply do max(len(self.stack1),len(self.stack2))==0
class MyQueue:

    def __init__(self):
        self.stack1 = []
        self.stack2 = []

    def push(self, x: int) -> None:
        print(self.stack1, self.stack2)
        self.stack1.append(x)

        

    def pop(self) -> int:
        print(self.stack1, self.stack2)
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        return self.stack2.pop()
        
        

    def peek(self) -> int:
        if not self.stack2:
            while self.stack1:
                self.stack2.append(self.stack1.pop())
        return self.stack2[-1]
        

    def empty(self) -> bool:
        return max(len(self.stack1),len(self.stack2))==0
        


# Your MyQueue object will be instantiated and called as such:
# obj = MyQueue()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.peek()
# param_4 = obj.empty()