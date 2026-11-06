# My solution not sure if most optimal
class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        if not grid:
            return 0
        rows, cols = len(grid), len(grid[0])
        visited = set()
        ans = 0

        def dfs(r,c):
            area = 1
            stack = []
            visited.add((r,c))
            stack.append((r,c))
            while stack:
                row,col = stack.pop()
                directions = [[1,0],[-1,0],[0,1],[0,-1]]
                for dr,dc in directions:
                    r = row+dr
                    c = col+dc
                    if r in range(rows) and c in range(cols) and grid[r][c] == 1 and (r,c) not in visited:
                        area+=1
                        stack.append((r,c))
                        visited.add((r,c))
                        grid[r][c] = 0
            return area
        for r in range(rows):
            for c in range(cols):
                if grid[r][c] == 1:
                    ans = max(ans,dfs(r,c))
        return ans
    
# Recursive way to do it -> 

class Solution:
    def maxAreaOfIsland(self, grid: List[List[int]]) -> int:
        area = -1
        ROWS,COLS = len(grid), len(grid[0])
        visited = set()
        directions = [[1,0],[0,1],[-1,0],[0,-1]]

        def dfs(r,c):
            if (r,c) not in visited:
                islandArea = 1
                visited.add((r,c))
                for dr,dc in directions:
                    if (r+dr in range(ROWS) and c+dc in range(COLS) and (r+dr, c+dc) not in visited and grid[r+dr][c+dc]==1) :
                        
                        islandArea+=dfs(r+dr, c+dc)
                return islandArea

        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == 1 and (r,c) not in visited:
                    area = max(area, dfs(r,c))
        return area if area!=-1 else 0


        