# Two Pointer Solution
# Need to understand this better

class Solution:
    def findLengthOfShortestSubarray(self, arr: List[int]) -> int:
        N = len(arr)
        # Remove Prefix Subarray
        r = N-1
        while r > 0 and arr[r-1] <= arr[r]:
            r-=1
        res = r
        # Remove Postfix Subarray
        l=0
        while l+1<N and arr[l+1]>=arr[l]:
            l+=1
        res = min(res, N-l-1)

        # Remove Middle Subarray
        l,r = 0, N-1
        while(l<r):
            #Shrink the valid window
            while r<N and l+1<r and arr[r-1]<=arr[r] and arr[l]<=arr[r]:
                r-=1
            # Epand the invalid window
            while r<N and arr[l] > arr[r]:
                r+=1
            res = min(res, r-l-1)
            if arr[l] > arr[l+1]:
                break
            l+=1
        return res



        