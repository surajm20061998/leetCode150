class TimeMap:

    def __init__(self):
        self.tvstore = {} # key = string : values = [list of pairs of [val,timestamp]]

    def set(self, key: str, value: str, timestamp: int) -> None:
        if key not in self.tvstore:
            self.tvstore[key] = []
        self.tvstore[key].append([value, timestamp])
        

    def get(self, key: str, timestamp: int) -> str:
        res = ""
        values = self.tvstore.get(key,[])

        # Now do a binay search over the given list of pairs
        l, r = 0, len(values)-1
        while l<=r:
            m = (l+r)//2
            if values[m][1] <= timestamp:
                res = values[m][0]
                l=m+1
            else : 
                r = m-1
        return res
        
