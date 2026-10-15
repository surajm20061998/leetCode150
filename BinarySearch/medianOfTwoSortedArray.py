# Hard Problem, need to see the solution again
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        A, B = nums1, nums2
        total = len(nums1)+ len(nums2)
        half = total // 2

        if len(B)<len(A):
            A, B = B, A
        
        l, r = 0, len(A)-1

        while True:
            i = (l+r)//2 # for A array
            j = half - i - 2 # for B array
            
            #Boundary Conditions
            Aleft = A[i] if i>=0 else float("-inf")
            Aright = A[i+1] if i+1<len(A) else float("inf")
            Bleft = B[j] if j>=0 else float("-inf")
            Bright = B[j+1] if j+1<len(B) else float("inf")

            if Aleft <= Bright and Bleft <= Aright:
                if total%2: # Oddlength
                    return min(Aright, Bright)
                else : #even length
                    return (max(Aleft, Bleft) + min(Aright, Bright))/2
            elif Aleft > Bright:
                r = i-1
            else :
                l = i+1


# An easier acceptable solution as well
# Use Two pointer approach to merge 2 sorted arrays
# Then just find the median
# uses extra space and is not the most efficient, but an acceptable brute force solution
class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:

        #merge
        nums3 = []
        l1,l2 = 0,0
        while l1<len(nums1) and l2<len(nums2):
            if nums1[l1] < nums2[l2]:
                nums3.append(nums1[l1])
                l1+=1
            else:
                nums3.append(nums2[l2])
                l2+=1
        while l1<len(nums1):
            nums3.append(nums1[l1])
            l1+=1
        while l2<len(nums2):
            nums3.append(nums2[l2])
            l2+=1
        print(nums3)
        n = len(nums3) 
        mid = n//2
        if n%2==0:
            return (nums3[mid-1] + nums3[mid])/2
        else:
            return nums3[mid]    