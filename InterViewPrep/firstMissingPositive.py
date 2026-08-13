# Solution passed but dont think its the most optimal
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:
        cmap = []
        for n in nums:
            if n>0:
                cmap.append(n)
        if not cmap:
            return 1
        n = len(cmap)
        tmp = set(cmap)
        print(tmp)
        for i in range(1,n+1):
            if i not in tmp:
                return i
        return n+1
    
    
    
# A better solution in terms of memory ->
class Solution:
    def firstMissingPositive(self, nums: List[int]) -> int:

        # Step 1:
        # We don't care about negative numbers.
        # Replace them with 0.
        for i in range(len(nums)):
            if nums[i] < 0:
                nums[i] = 0

        # Step 2:
        # Use indices to mark which numbers [1, n] exist.
        #
        # Number 1 -> index 0
        # Number 2 -> index 1
        # ...
        # Number n -> index n-1
        for i in range(len(nums)):
            val = abs(nums[i])

            if 1 <= val <= len(nums):

                # Positive means we haven't marked this number yet
                if nums[val - 1] > 0:
                    nums[val - 1] *= -1

                # Can't turn 0 negative, so use -(n+1)
                # as a negative marker instead.
                elif nums[val - 1] == 0:
                    nums[val - 1] = -(len(nums) + 1)

        # Step 3:
        # First non-negative position corresponds to
        # the first missing positive number.
        for i in range(len(nums)):
            if nums[i] >= 0:
                return i + 1

        # All numbers 1...n exist
        return len(nums) + 1