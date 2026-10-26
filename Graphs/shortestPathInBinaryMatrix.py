class Solution:
    def shortestPathBinaryMatrix(self, grid: list[list[int]]) -> int:
        N = len(grid)
        q = deque([(0,0,1)]) 
        visited = set((0,0))
        directions = [[0,1],[1,0],[0,-1],[-1,0],[1,1],[-1,-1],[1,-1],[-1,1]]
        while q:
            r,c,length = q.popleft()
            if r not in range(N) or c not in range(N) or grid[r][c] == 1:
                continue
            if r==N-1 and c==N-1:
                return length
            for dr,dc in directions:
                if (r+dr, c+dc) not in visited:
                    q.append((r+dr, c+dc, length+1))
                    visited.add((r+dr, c+dc))
        return -1        