# 3 Binary Search Solutions
# First loop to search for the peak elelement
# Once peak element is found we know that the array structure is [Ascending]-Peak-[Descending]
# Then Do binary Search on the left sorted array
# Then Do binary search on the right sorted array
# If the answer does not exist in the 2 sorted arrays return -1
class Solution:
    def findInMountainArray(self, target: int, mountainArr: 'MountainArray') -> int:
        n = mountainArr.length()
        l,r = 1, n-2
        # search for peak
        while l<=r:
            m=(l+r)//2
            left, mid, right = mountainArr.get(m-1),mountainArr.get(m),mountainArr.get(m+1)
            if left<mid<right:
                l=m+1
            elif left>mid>right:
                r = m-1
            else :
                break
        peak = m

        # search left portion
        l,r = 0, peak
        while l<=r:
            m = (l+r)//2
            val = mountainArr.get(m)
            if val<target:
                l=m+1
            elif val>target:
                r=m-1
            else:
                return m

        # search right portion
        l,r = peak, n-1
        while l<=r:
            m = (l+r)//2
            val = mountainArr.get(m)
            if val<target:
                r = m-1
            elif val>target:
                l=m+1
            else:
                return m
        return -1

        