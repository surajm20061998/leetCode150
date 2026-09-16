# Need to check again
# 
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def kthSmallest(self, root: Optional[TreeNode], k: int) -> int:

        n = 0
        stack = []
        curr = root

        while curr and stack:
            # Traverse till the leftmost node and keep storing it in stack
            while curr:
                stack.append(curr)
                curr = curr.left
            
            # once done, start popping from stack
            curr = stack.pop()
            n+=1
            if n==k:
                return curr.val
            # if condition is not met then traverse to the right subtrees
            curr = curr.right
        