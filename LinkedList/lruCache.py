#Need to practice and try again, complext problem

class ListNode:
    def __init__(self, key, value):
        self.key, self.val = key, value
        self.prev = self.nxt = None

class LRUCache:

    def __init__(self, capacity: int):
        self.cap = capacity # capacity of my cache
        self.cache = {} # map to store key values
        self.left = ListNode(0,0) # left Dummy Node
        self.right = ListNode(0,0) #right Dummy Node
        self.left.nxt = self.right # pointer Setup doubly linked list
        self.right.prev = self.left # pointer Setup doubly linked list

    # Remove and insert are just helper functions to do repeated remove and delete operations from the linkedList
    def remove(self, node):
        tmpPrev, tmpNxt = node.prev, node.nxt
        tmpPrev.nxt, tmpNxt.prev = tmpNxt, tmpPrev

    def insert(self, node):
        tmpPrev, tmpNxt = self.right.prev, self.right
        tmpPrev.nxt = tmpNxt.prev = node
        node.nxt, node.prev = tmpNxt, tmpPrev

        
    def get(self, key: int) -> int:
        # if key in cache return key and update usage
        # else return -1

        if key in self.cache:
            # Remove from list and then add it back to the right most position
            self.remove(self.cache[key])
            self.insert(self.cache[key])
            return self.cache[key].val
        return -1
        

    def put(self, key: int, value: int) -> None:
        # if key already in cache, remove it and add it back to the right most position
        if key in self.cache:
            self.remove(self.cache[key])
        self.cache[key] = ListNode(key,value)
        self.insert(self.cache[key])
        
        #if we breach capacity then find and remove the lru node from list and cache
        if len(self.cache) > self.cap:
            lru = self.left.nxt
            self.remove(lru)
            del self.cache[lru.key]
        
