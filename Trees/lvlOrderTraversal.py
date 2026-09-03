#lvl order traversal + print each level
# Optimal Solution
# Time Complexity - O(n) Recursion but every node is computed exactly once
# Space COmplexity - O(h) Height of the Tree

from collections import deque
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def levelOrder(self, root: Optional[TreeNode]) -> List[List[int]]:

        if not root:
            return []

        q = deque()
        q.append(root)
        ans = []
        while q:
            tmpAns = []
            qlen = len(q)
            for i in range(qlen):
                node = q.popleft()
                if node:
                    tmpAns.append(node.val)
                    q.append(node.left)
                    q.append(node.right)
            if tmpAns:
                ans.append(tmpAns)
            
        return ans
        