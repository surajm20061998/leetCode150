# backtracking
# Need to see again
class Solution:
    def makesquare(self, matchsticks: List[int]) -> bool:
        if sum(matchsticks)%4!=0:
            return False
        length = sum(matchsticks)//4
        sides = [0]*4
        matchsticks.sort(reverse=True)

        def dfs(index):
            if index == len(matchsticks):
                return True
            for j in range(4):
                if sides[j] + matchsticks[index]<=length:
                    sides[j]+=matchsticks[index]
                    if dfs(index+1):
                        return True
                    sides[j] -= matchsticks[index]
            return False
        return dfs(0)
        