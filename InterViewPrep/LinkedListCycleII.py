# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, x):
#         self.val = x
#         self.next = None

# Fast and Slow pointer Solution
# Need to understand the return condition
class Solution:
    def detectCycle(self, head: Optional[ListNode]) -> Optional[ListNode]:
        fp = head
        sp = head
        prevsp = head

        while fp and fp.next:
            fp =fp.next.next
            sp = sp.next

            if fp == sp:
                sp = head
                while(sp!=fp):
                    sp = sp.next
                    fp = fp.next
                return sp
                
        return None

        