import sys
sys.setrecursionlimit(1000000)
class Solution:

    def solve(self, N,M,matrix):
        def dfs(r,c):
            if r>=N or c>=M:
                return float('-inf')
            if r==N-1 and c==M-1:
                return matrix[r][c]
            right = dfs(r,c+1)
            down = dfs(r+1, c)
            return matrix[r][c]+max(right, down)
        return dfs(0,0)
        

def main():
    input = sys.stdin.readline
    N,M = map(int, input().split())
    matrix = []
    for _ in range(N):
        row = list(map(int, input().split()))
        matrix.append(row)
    solution = Solution()
    print(solution.solve(N,M,matrix))

 
if __name__ == '__main__':
    main()