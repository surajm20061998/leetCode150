# need to understand again

class Solution:
    def combine(self, n: int, k: int) -> List[List[int]]:
        res = []

        def dfs(start, combinations):
            # Base case
            if len(combinations)==k:
                res.append(combinations.copy())
                return
            
            #Choices
            for i in range(start,n+1):
                combinations.append(i)
                dfs(i+1, combinations)
                combinations.pop()
        dfs(1,[])
        return res