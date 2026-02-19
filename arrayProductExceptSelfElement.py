class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:
        n = len(nums)
        preArr = [1]*(n)
        suffArr = [1]*(n)
        finArr = [0]*n

        preArr[0] = 1
        suffArr[-1] = 1

        for i in range(1,n):
            preArr[i] = preArr[i-1]*nums[i-1]

        print(preArr)

        for i in range(n-2,-1,-1):
            suffArr[i] = suffArr[i+1]*nums[i+1]
        
        print(suffArr)

        for i in range(n):
            finArr[i] = preArr[i]*suffArr[i]

        return finArr

        