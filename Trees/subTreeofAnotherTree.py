# similar to the same binary tree question
# Need to review again

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:   
    def isSubtree(self, s: Optional[TreeNode], t: Optional[TreeNode]) -> bool:
        if not t:
            return True
            # empty tree is also a subtree
        if not s:
            return False
            # if t and not s, then false
        if self.isSameTree(s,t):
            return True
            # if s and t are equal then they are the subtress of each other as well
        return (self.isSubtree(s.left, t) or self.isSubtree(s.right, t))
        # Run the recursion, but move s.right and s.left

    
    def isSameTree(self, s, t):
        # same as the same binary tree question
        if not s and not t:
            return True
        if s and t and s.val == t.val:
            return (self.isSameTree(s.left, t.left) and self.isSameTree(s.right, t.right))
        return False

        