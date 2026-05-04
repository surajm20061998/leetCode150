# Optimal Solution - ?
# Time Complexity - O(n) Recursion but every node is computed exactly once
# Space COmplexity - O(h) Height of the Tree

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def maxDepth(self, root: Optional[TreeNode]) -> int:
        if not root:
            return 0

        return max(self.maxDepth(root.left)+1, self.maxDepth(root.right)+1)
        