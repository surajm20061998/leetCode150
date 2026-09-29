# Need to review this again

class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:

        candidates.sort() # easy to eliminate duplicates

        res = []

        def dfs(curr, pos, target):
            if target == 0:
                res.append(curr.copy())
            if target <=0:
                return
            prev = -1
            for i in range(pos, len(candidates)):
                if candidates[i] == prev:
                    continue
                curr.append(candidates[i])
                dfs(curr, i+1, target-candidates[i])
                curr.pop()
                prev = candidates[i]
        dfs([],0, target)
        return res       



        