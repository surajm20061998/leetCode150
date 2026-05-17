# My Solution
# Maybe not most optimal but no sorting involved
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        heapify(nums)
        while len(nums) > k:
            heappop(nums)
        return nums[0]

# Another solution
# Just sort the solution as is and return kth largest element
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        nums.sort()
        return nums[len(nums) - k]
    
#Better solution is using Quick Select (See and do question again)
class Solution:
    def findKthLargest(self, nums: List[int], k: int) -> int:
        pivot = random.choice(nums)
        left = [num for num in nums if num > pivot]
        mid = [num for num in nums if num == pivot]
        right = [num for num in nums if num < pivot]

        length_left = len(left)
        length_right = len(right)
        length_mid = len(mid)
        if k <= length_left:
            return self.findKthLargest(left, k)
        elif k > length_left + length_mid:
            return self.findKthLargest(right, k - length_mid - length_left)
        else:
            return mid[0]
