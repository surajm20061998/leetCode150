# Binary Search Solution

# Binary Search to find the lowest possible rate (bananas/hr) to finish all bananas in given time

# rate = bananas/time so time = bananas/rate

# Need see and understand this again

class Solution:
    def minEatingSpeed(self, piles: List[int], h: int) -> int:
        l,r = 1, max(piles) # l, r are searching for the min k such that all bananas are done within h hours
        res = r

        while l<=r:
            k = (l+r)//2
            hours = 0
            for p in piles:
                hours += math.ceil(p/k)
            # If banans are finished in less time than h, update result and move the search space to the left side
            if hours <= h:
                res = min(res,k)
                r = k-1
            # Else continue searching on the right side
            else:
                l = k+1
        return res        