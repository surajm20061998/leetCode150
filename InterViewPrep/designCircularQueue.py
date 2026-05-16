# Optimal Solution
# Most of the functions are simple if Doubly linked list implementation is clear
# Need to look at enQueue and deQueue again
class ListNode:
    def __init__(self, val,next,prev):
        self.val, self.next, self.prev = val, next, prev

class MyCircularQueue:

    def __init__(self, k: int):
        self.space = k #capacity of ring buffer
        self.left = ListNode(0,None,None)
        self.right = ListNode(0,None,self.left)
        self.left.next = self.right
        #setup the capacity and the left and right dummy pointers pointers are also set up

    def enQueue(self, value: int) -> bool:
        if self.isFull():return False
        curr = ListNode(value,self.right,self.right.prev)
        self.right.prev.next = curr
        self.right.prev = curr
        self.space-=1
        return True
        
    def deQueue(self) -> bool:
        if self.isEmpty():return False
        self.left.next = self.left.next.next
        self.left.next.prev = self.left
        self.space+=1
        return True

    def Front(self) -> int:
        if self.isEmpty():return -1
        return self.left.next.val
        #First element will be right next to the left dummy node

    def Rear(self) -> int:
        if self.isEmpty():return -1
        return self.right.prev.val
        #Rear element will be previous to the right dummy node

    def isEmpty(self) -> bool:
        return self.left.next==self.right
        # There is nothing between the dummy left and right nodes

    def isFull(self) -> bool:
        return self.space==0
        #Ideally reduce this space variable everytime an element is added and increase everytime an
        #element is popped out


# Your MyCircularQueue object will be instantiated and called as such:
# obj = MyCircularQueue(k)
# param_1 = obj.enQueue(value)
# param_2 = obj.deQueue()
# param_3 = obj.Front()
# param_4 = obj.Rear()
# param_5 = obj.isEmpty()
# param_6 = obj.isFull()