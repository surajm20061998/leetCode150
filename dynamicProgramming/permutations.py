class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:

        # Base case:
        # one permutation of nothing = empty permutation
        if len(nums) == 0:
            return [[]]

        # Generate every permutation WITHOUT nums[0]
        perms = self.permute(nums[1:])

        res = []

        # For every smaller permutation
        for p in perms:

            # Insert nums[0] into every possible position
            for i in range(len(p) + 1):

                # Copy because we don't want to modify p
                p_copy = p.copy()

                # Insert current number
                p_copy.insert(i, nums[0])

                # This creates a new permutation
                res.append(p_copy)

        return res