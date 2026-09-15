# Definition for a binary tree node.
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right

# When we do BFS, the last node of the level is the rightmost Node, that is all we have to record and return in the result

class Solution:
    def rightSideView(self, root: Optional[TreeNode]) -> List[int]:

        result = []
        q = collections.deque()
        q.append(root)

        while q:
            rightSide = None
            qlen = len(q)

            for i in range(qlen):
                node = q.popleft()
                if node:
                    rightSide = node
                    q.append(node.left)
                    q.append(node.right)
            if rightSide:
                result.append(rightSide.val)
        return result
            