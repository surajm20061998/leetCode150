# Binary Search Problem

class Solution:
    def mySqrt(self, x: int) -> int:
        if x == 1:
            return 1
        l=1
        r=x//2
        res = 0
        while (l<=r):
            m = l + ((r-l)//2)
            if m*m == x:
                return m # This is the definite answer
            elif m*m<x:
                l = m+1
                res = m # This could be a possible answer
            else :
                r = m-1
        return res

        