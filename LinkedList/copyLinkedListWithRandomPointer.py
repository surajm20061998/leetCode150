

"""
# Definition for a Node.
class Node:
    def __init__(self, x: int, next: 'Node' = None, random: 'Node' = None):
        self.val = int(x)
        self.next = next
        self.random = random
"""

class Solution:
    def copyRandomList(self, head: 'Optional[Node]') -> 'Optional[Node]':
        nodeMap = {None : None}
        curr = head
        while curr : 
            copy = Node(curr.val)
            nodeMap[curr] = copy
            curr = curr.next
        curr = head
        while curr :
            copy = nodeMap[curr]
            copy.next = nodeMap[curr.next]
            copy.random = nodeMap[curr.random]
            curr = curr.next
        return nodeMap[head]
        