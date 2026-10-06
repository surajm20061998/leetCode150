# Codeforces Problem

import sys
sys.setrecursionlimit(1000000)
class Solution:

    def solve(self, nums, X):
        def dfs(index, currSum):
            if index>=len(nums):
                return currSum == X
            return dfs(index+1, currSum+nums[index]) or dfs(index+1, currSum-nums[index])
        return dfs(1, nums[0])

def main():
    input = sys.stdin.readline
    n, X = map(int, input().split())
    nums = list(map(int, input().split()))
    solution = Solution()
    if solution.solve(nums, X):
        print("YES")
    else : 
        print("NO")

 
if __name__ == '__main__':
    main()