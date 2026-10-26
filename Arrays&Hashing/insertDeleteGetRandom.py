class RandomizedSet:

    def __init__(self):
        self.hashSet = {} # val -> index
        self.indexArray = []

    def insert(self, val: int) -> bool:
        if val not in self.hashSet:
            self.indexArray.append(val)
            self.hashSet[val] = len(self.indexArray)-1
            return True
        return False
        

    def remove(self, val: int) -> bool:
        if val in self.hashSet:
            index = self.hashSet[val]
            lastVal = self.indexArray[-1]
            self.indexArray[index] = lastVal
            self.hashSet[lastVal] = index
            self.indexArray.pop()
            del self.hashSet[val]
            return True
        return False

    def getRandom(self) -> int:
        return random.choice(self.indexArray)


# Your RandomizedSet object will be instantiated and called as such:
# obj = RandomizedSet()
# param_1 = obj.insert(val)
# param_2 = obj.remove(val)
# param_3 = obj.getRandom()