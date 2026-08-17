# Question at https://github.com/doocs/leetcode/blob/main/solution/0200-0299/0281.Zigzag%20Iterator/README_EN.md
# locked by leetcode premium

# Solution 
 # Take from v1 if:
        # 1. It's v1's turn and v1 has elements, OR
        # 2. v2 is exhausted
        
class ZigzagIterator:
    def __init__(self, v1: List[int], v2: List[int]):
        self.v1 = v1
        self.v2 = v2
        self.i1 = 0
        self.i2 = 0
        self.turn = 0 # 0 or 1


    def next(self) -> int:
        if (self.turn == 0 and self.i1<len(self.v1)) or self.i2 >= len(self.v2):
            val = self.v1[self.i1]
            self.i1+=1
            self.turn = 1
            return val
        val = self.v2[self.i2]
        self.i2+=1
        self.turn = 0
        return val         
        

    def hasNext(self) -> bool:
        return self.i1<len(self.v1) or self.i2<len(self.v2)


# Your ZigzagIterator object will be instantiated and called as such:
# i, v = ZigzagIterator(v1, v2), []
# while i.hasNext(): v.append(i.next())




# Anothe Solution - 
class ZigzagIterator:
    def __init__(self, v1: List[int], v2: List[int]):
        self.res = deque()
        i1, n1 = 0, len(v1)
        i2, n2 = 0, len(v2)
        while i1 < n1 and i2 < n2:
            self.res.append(v1[i1])
            i1 += 1
            self.res.append(v2[i2])
            i2 += 1
        while i1 < n1:
            self.res.append(v1[i1])
            i1 += 1
        while i2 < n2:
            self.res.append(v2[i2])
            i2 += 1
            
    def next(self) -> int:
        return self.res.popleft()
    
    def hasNext(self) -> bool:
        return len(self.res) > 0
