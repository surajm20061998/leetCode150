# Optimal Solution
# Time Complexity - O(n+p) n=numCourses anf p = number of preReqs
# Space Complexity - O(n+p)

from collections import defaultdict
class Solution:
    def canFinish(self, numCourses: int, prerequisites: List[List[int]]) -> bool:
        preMap = {i:[] for i in range(numCourses)}
        for crs,pre in prerequisites:
            preMap[crs].append(pre)
        visited = set()

        def dfs(crs):
            if crs in visited:
                return False #cycle detected
            if preMap[crs]==[]:
                return True #condition is that if we have a course with no prerequisites then its do-able

            visited.add(crs)
            for pre in preMap[crs]:
                if not dfs(pre) : return False
            
            visited.remove(crs) # Finished all operations and not visiting anymore so just remove it
            preMap[crs]=[] #same condition as above if the course is doa-able set its preReq list to None
            return True
        
        for crs in range(numCourses): # loop this way do deal with multiple connected components
            if not dfs(crs):
                return False
        return True