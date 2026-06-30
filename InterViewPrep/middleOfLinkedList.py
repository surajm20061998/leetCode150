# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

# Fast + Slow pointer Solution
# Pretty straigh forward
class Solution:
    def middleNode(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fp = head
        sp = head

        while fp and fp.next:
            fp=fp.next.next
            sp=sp.next
        return sp
        