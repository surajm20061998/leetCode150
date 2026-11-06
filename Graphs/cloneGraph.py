"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""
# Optimal Solution
# Time Complexity - O(V+E)
# Space Complexity - O(V)
from typing import Optional
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:
        oldToNew = {}

        def dfs(node):
            if node in oldToNew:
                return oldToNew[node]
            copy = Node(node.val)
            oldToNew[node] = copy
            for nei in node.neighbors:
                copy.neighbors.append(dfs(nei))
            return copy
        return dfs(node) if node else None
    
# Saw it again, similar idea as above
# if node in bookeeping return it else create it and add all the neighbors recursively
"""
# Definition for a Node.
class Node:
    def __init__(self, val = 0, neighbors = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []
"""
class Solution:
    def cloneGraph(self, node: Optional['Node']) -> Optional['Node']:

        if not node:
            return None

        nodeMap = {} # node and copy structures
        def dfs(node):
            if node in nodeMap: # copy already exists
                return nodeMap[node]
            copy = Node(node.val)
            nodeMap[node] = copy
            for nei in node.neighbors: # for the given node, make sure the copy also makes all the nodes
                copy.neighbors.append(dfs(nei))
            return copy
        return dfs(node)

        

        