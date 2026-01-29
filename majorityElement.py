from collections import defaultdict
class Solution:
    def majorityElement(self, nums: List[int]) -> int:

        n = len(nums)
        countList = defaultdict(int)

        for num in nums:
            countList[num]+=1
            if(countList[num] > n//2):
                return num
        