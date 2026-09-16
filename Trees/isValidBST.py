#Optimal Solution
#TIme Complexity - O(n)
#Space COmplexity - O(h) h is height of tree logn

# During recursion need to make sure that each node follows bst rules compared to root rather than just the previous node

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isValidBST(self, root: Optional[TreeNode]) -> bool:

        def dfs(root, lower, upper):
            if not root:
                return True

            if not(lower<root.val<upper):
                return False

            return (dfs(root.left, lower, root.val) and dfs(root.right,root.val,upper))
        return dfs(root, float("-inf"), float("inf"))
        