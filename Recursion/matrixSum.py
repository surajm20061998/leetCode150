# Codeforces - 

import sys
sys.setrecursionlimit(1000000)
class Solution:
        
    def solve(self, A, B, R, C):
        def rec(row, col):
            if row == R:
                return
            if col == C:
                rec(row+1, 0)
                return
            A[row][col] += B[row][col]
            rec(row, col+1)
        rec(0,0)
        return A

def main():
    input = sys.stdin.readline
    R,C = map(int, input().split())
    A= []
    for _ in range(R):
        A.append(list(map(int, input().split())))
    B = []
    for _ in range(R):
        B.append(list(map(int, input().split())))
    solution = Solution()
    ans = solution.solve(A, B, R, C)
    for row in ans:
        print(*row)
 
if __name__ == '__main__':
    main()