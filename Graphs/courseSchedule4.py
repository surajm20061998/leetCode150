# Need to see this Solution again

class Solution:
    def checkIfPrerequisite(self, numCourses: int, prerequisites: List[List[int]], queries: List[List[int]]) -> List[bool]:
        adj = defaultdict(list)
        for prereq, crs in prerequisites:
            adj[crs].append(prereq)

        def dfs(crs):
            if crs not in preReqMap:
                preReqMap[crs] = set()
                for prereq in adj[crs]:
                    preReqMap[crs] = preReqMap[crs] | dfs(prereq)
                preReqMap[crs].add(crs)
            return preReqMap[crs]

        preReqMap = {}
        for crs in range(numCourses):
            dfs(crs)
        res = []
        for u,v in queries:
            res.append(u in preReqMap[v])
        return res
        