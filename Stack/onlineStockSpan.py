# Similar Solution to the Daily Temperatures Problem
# Was able to get the general intuition before seeing the solution, needed help in code
class StockSpanner:

    def __init__(self):
        self.stk = []
        

    def next(self, price: int) -> int:
        span = 1
        while self.stk and price>=self.stk[-1][0]:
            span+=self.stk[-1][1]
            self.stk.pop()
        self.stk.append([price,span])
        return span

# Your StockSpanner object will be instantiated and called as such:
# obj = StockSpanner()
# param_1 = obj.next(price)