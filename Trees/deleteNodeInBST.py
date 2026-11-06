# Time Complexity -> O(h) -> h=height of the BST

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
            if not root.right: # If the right subtree is empty return the left subtree
                return root.left
            elif not root.left: # If the left subtree is empty return the right subtree
                return root.right
            else : # Final condition -> Just find the min from the right subtree and return it
                curr = root.right
                while curr.left:
                    curr = curr.left
                root.val = curr.val
                root.right = self.deleteNode(root.right, root.val)
        return root
    
        