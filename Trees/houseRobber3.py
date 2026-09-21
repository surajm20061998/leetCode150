# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# DFS Post order traversal
# For every subtree we need to take a look at 2 cases -> [maxAmtWithRoot, maxAmtWithoutRoot]
# Need to skim thorigh again
class Solution:
    def rob(self, root: Optional[TreeNode]) -> int:

        # This will return a pair [maxAmtWithRoot, maxAmtWithoutRoot]
        def dfs(root):
            if not root:
                return [0,0]

            leftPair = dfs(root.left)
            rightPair = dfs(root.right)

            withRoot = root.val + leftPair[1] + rightPair[1]
            withoutRoot = max(leftPair) + max(rightPair)

            return [withRoot, withoutRoot]
        return max(dfs(root))
        