# Binary Search problem

# Understood the Binary Search Part, need to understand the capacity function
# Binary search part is similar to coco eating bananas

class Solution:
    def shipWithinDays(self, weights: List[int], days: int) -> int:
        # function to determine if current capacity can ship it in given days
        def canShip(cap):
            ships, currCap = 1,cap
            for w in weights:
                if currCap -w <0:   # if capacity is -ive means the ship cannot hold anymore so just add a new ship
                    ships+=1
                    currCap = cap   # Since a new ship is added current capacity is reset
                currCap -=w
            return ships<=days

        # Search Space is [max(weights), sum(weights)]
        l,r = max(weights), sum(weights)
        res = r
        while l<=r:
            cap = (l+r)//2
            if canShip(cap):
                res = min(res,cap)
                r= cap-1
            else:
                l=cap+1
        return res
        