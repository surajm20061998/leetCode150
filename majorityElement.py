from collections import defaultdict
class Solution:
    def majorityElement(self, nums: List[int]) -> int:

        n = len(nums)
        countList = defaultdict(int)

        for num in nums:
            countList[num]+=1
            if(countList[num] > n//2):
                return num
            
# majority element solution in constant space
class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        count = 0
        candidate = None

        for n in nums:
            if count == 0:
                candidate = n

            if n == candidate:
                count +=1
            else :
                count -=1
        return candidate
        