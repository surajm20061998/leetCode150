# need to see this again
# Initially used unidirected cycle detection, that was wrong, need to think of this as a bidirectional graph problem
# Also did not account for spare nodes earlier, need to make sure that all nodes are connected.

class Solution:
    def validTree(self, n: int, edges: List[List[int]]) -> bool:
        hmap = {i:[] for i in range(n)}
        for u,v in edges:
            hmap[u].append(v)
            hmap[v].append(u)
        visited = set()

        def dfs(node, parent):
            if node in visited:
                return False
            visited.add(node)
            for nei in hmap[node]:
                if nei == parent:
                    continue
                if not dfs(nei, node):
                    return False
            return True
        if not dfs(0,-1):
            return False
        return len(visited) == n