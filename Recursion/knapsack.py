# Codeforces Problem
import sys
sys.setrecursionlimit(1000000)
class Solution:

    def solve(self, weights, values, W):
        def dfs(i, capacity):
            # BASE CASE
            if i>=len(weights):
                return 0
            # Current item doesn't fit
            if weights[i] > capacity:
                return dfs(i+1, capacity)
            # TAKE
            take = values[i] + dfs(i+1, capacity-weights[i])
            # SKIP
            skip = dfs(i+1, capacity)
            return max(take, skip)
        return dfs(0, W)

def main():
    input = sys.stdin.readline
    n, w = map(int, input().split())
    weights = []
    values = []
    for _ in range(n):
        w1, v1 = map(int, input().split())
        weights.append(w1)
        values.append(v1)
    solution = Solution()
    print(solution.solve(weights, values, w))

 
if __name__ == '__main__':
    main()