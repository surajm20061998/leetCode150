# Efficient way to solve it
# using union find to count connected components
# need to understand this solution

class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        par = [i for i in range(n)]
        rank = [1]*n

        def find(n1):
            res = n1
            while res!=par[res]:
                par[res] = par[par[res]]
                res = par[res]
            return res
        def union(n1,n2):
            p1, p2 = find(n1), find(n2)
            if p1==p2:
                return 0
            if rank[p2] > rank[p1]:
                par[p1] = p2
                rank[p2] += rank[p1]
            else:
                par[p2] = p1
                rank[p1] += rank[p2]
            return 1
        res = n
        for n1,n2 in edges:
            res -= union(n1,n2)
        return res
        

# my solution -
# just run dfs on every node that is not in the visited set and increment count

class Solution:
    def countComponents(self, n: int, edges: List[List[int]]) -> int:
        adj = defaultdict(list)
        for u,v in edges:
            adj[u].append(v)
            adj[v].append(u)
        visited = set()

        def dfs(node):
            visited.add(node)
            for nei in adj[node]:
                if nei not in visited:
                    visited.add(nei)
                    dfs(nei)

        count = 0
        for i in range(n):
            if i not in visited:
                count+=1
                dfs(i)
        return count


        