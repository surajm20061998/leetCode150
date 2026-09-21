# Need to understand the delete conditions again
# 
# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
class Solution:
    def deleteNode(self, root: Optional[TreeNode], key: int) -> Optional[TreeNode]:

        if not root:
            return 

        if key > root.val: # Traverse Right
            root.right = self.deleteNode(root.right, key)
        elif key < root.val: # Traverse left
            root.left = self.deleteNode(root.left, key)
        else : # Key found
            if not root.right:
                return root.left
            elif not root.left:
                return root.right
            
            curr = root.right
            while curr.left:
                curr = curr.left
            root.val = curr.val
            root.right = self.deleteNode(root.right, root.val)
        return root
    
        