# Linked List question
# Iterative solution

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev, curr = None, head

        while curr:
            tmp = curr.next #tmp storage for next node
            curr.next = prev # Link to previous node
            prev = curr # increment prev
            curr = tmp #increment step
        return prev

        
        