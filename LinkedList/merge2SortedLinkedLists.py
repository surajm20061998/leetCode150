# My Initial Solution, not sure if its the most optimal

# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

class Solution:
    def mergeTwoLists(self, list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:
        p1 = list1
        p2 = list2
        p3 = ListNode()
        dummy = p3

        while p1 and p2:
            if p1.val <= p2.val:
                newNode = ListNode(p1.val)
                p3.next = newNode
                p1 = p1.next
            else:
                newNode = ListNode(p2.val)
                p3.next = newNode
                p2 = p2.next
            p3=p3.next
        
        while p1:
            newNode = ListNode(p1.val)
            p3.next = newNode
            p1 = p1.next
            p3 = p3.next
        while p2:
            newNode = ListNode(p2.val)
            p3.next = newNode
            p2 = p2.next
            p3 = p3.next

        return dummy.next

        