# TLEd bbut still correct solution - TLEd because of .index method

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def buildTree(self, preorder: List[int], inorder: List[int]) -> Optional[TreeNode]:

        if not preorder or not inorder:
            return None

        root = TreeNode(preorder[0])
        mid = inorder.index(preorder[0])
        root.left = self.buildTree(preorder[1:mid+1], inorder[:mid])
        root.right = self.buildTree(preorder[mid+1:], inorder[mid+1:])
        return root
        





# Correct Solution - GPT

# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

class Solution:
    def buildTree(
        self,
        preorder: List[int],
        inorder: List[int]
    ) -> Optional[TreeNode]:

        inorderMap = {
            val: i
            for i, val in enumerate(inorder)
        }

        preorderIndex = 0

        def dfs(left, right):
            nonlocal preorderIndex

            if left > right:
                return None

            # Preorder tells us the next root
            rootVal = preorder[preorderIndex]
            preorderIndex += 1

            root = TreeNode(rootVal)

            # Inorder tells us where to split
            mid = inorderMap[rootVal]

            root.left = dfs(left, mid - 1)
            root.right = dfs(mid + 1, right)

            return root

        return dfs(0, len(inorder) - 1)