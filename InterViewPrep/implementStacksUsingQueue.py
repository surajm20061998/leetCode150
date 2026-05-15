# Optimal Solution, but not that efficient (the problem itself isnt that efficient)
# Basically use a single queue
# For push -> just append to q
# for top -> just return q[-1]
# for empty -> just return len(q)==0
# for pop -> (trick one) do popleft till the last element, and keep pusing these elements back to the queue while doing so 
# in the end just return q.popleft()

class MyStack:

    def __init__(self):
        self.q = deque()
        

    def push(self, x: int) -> None:
        self.q.append(x)
        

    def pop(self) -> int:
        for i in range(len(self.q)-1):
            self.push(self.q.popleft())
        return self.q.popleft()
        

    def top(self) -> int:
        return self.q[-1]
        

    def empty(self) -> bool:
        return len(self.q)==0


# Your MyStack object will be instantiated and called as such:
# obj = MyStack()
# obj.push(x)
# param_2 = obj.pop()
# param_3 = obj.top()
# param_4 = obj.empty()