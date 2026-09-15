#lvl order traversal + print each level
# Optimal Solution
# Time Complexity - O(n) Recursion but every node is computed exactly once
# Space COmplexity - O(h) Height of the Tree

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
from collections import deque
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:
        if not root :
            return []

        result = []
        q = deque()
        q.append(root)
        while q:
            lvl = []
            qlen = len(q)
            for i in range(qlen): # since we ahve to print each level we add afor loop of size qlen here
                node = q.popleft()
                if node:
                    lvl.append(node.val)
                    q.append(node.left)
                    q.append(node.right)
            if lvl:
                result.append(lvl)
        return result
