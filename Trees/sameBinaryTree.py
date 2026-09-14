# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isSameTree(self, p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:
        if not p and not q: # Both nodes are null so return true
            return True
        if not p or not q: # Either one node is null so return False
            return False
        if p.val!=q.val: # Valuse Differ so false
            return False
        # Finally Recursively do the same for left and right node of p and q till they both are null
        return (self.isSameTree(p.left,q.left) and self.isSameTree(p.right, q.right))
        