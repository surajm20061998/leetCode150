# Optimal Solution
# Time Complexity = O(n+p)
# Space Complexity = O(n+p)

# Topological Sort
# Cycle detection

class Solution:
    def findOrder(self, numCourses: int, prerequisites: List[List[int]]) -> List[int]:
        preMap = {i:[] for i in range(numCourses)}
        for crs,pre in prerequisites:
            preMap[crs].append(pre)
        
        output = []
        visited = set() # This will contain the node we have finished visiting (i.e after recursion)
        cycle = set() # This will contain nodes we are currently visiting (i.e during recursion)

        def dfs(crs):
            if crs in cycle:
                return False #Cycle detected
            if crs in visited:
                return True #Found a node that we have already visited before so preReqs are completed
            
            cycle.add(crs)
            for pre in preMap[crs]:
                if dfs(pre)==False:
                    return False
            cycle.remove(crs)
            visited.add(crs) # Remove from cycle set and add to visited set so that we dont detect false cycles
            output.append(crs) # append to answer
            return True
        
        for c in range(numCourses):
            if dfs(c)==False:
                return []
        return output

        