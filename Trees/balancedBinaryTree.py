# My Solution

# A height-balanced binary tree is defined as a binary tree in which the left and right subtrees of every node differ in height by no more than 1.

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def isBalanced(self, root: Optional[TreeNode]) -> bool:

        self.res = True

        def dfs(curr):
            if not curr : 
                return 0

            print(dfs(curr.left), dfs(curr.right))
            if (abs(dfs(curr.left) - dfs(curr.right)) > 1):
                self.res = False

            return 1+max(dfs(curr.left), dfs(curr.right))

        dfs(root)
        return self.res
        