# BFS solution
# Basically do a bfs on each node and increment count only if node not in visited

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        visited = set()
        countIslands = 0

        def bfs(r,c):
            q = collections.deque()
            visited.add((r,c))
            q.append((r,c))

            while q:
                row, col = q.popleft()
                directions = [[1,0],[-1,0],[0,1],[0,-1]] # Directios where we can move int the grid

                for dr, dc in directions:
                    if (row+dr in range(rows) and #Out of bounds check for rows
                        col +dc in range(cols) and #Out of bounds check for cols
                        grid[row+dr][col+dc]=="1" and #Check if land or not
                        (row+dr,col+dc) not in visited): #Check for node being visited or not, if visited then dont appendd to queue
                        q.append((row+dr,col+dc))
                        visited.add((row+dr,col+dc))

        for r in range(rows):
            for c in range(cols):
                if grid[r][c]=="1" and (r,c) not in visited:
                    bfs(r,c)
                    countIslands+=1
        return countIslands 
    
    
    
# DFS Solution 
# Not very different from BFS solution, just changed Queue to Stack and popleft to pop
# rest remains the same

class Solution:
    def numIslands(self, grid: List[List[str]]) -> int:
        if not grid:
            return 0

        rows, cols = len(grid), len(grid[0])
        visited = set()
        countIslands = 0

        def dfs(r,c):
            stack = []
            visited.add((r,c))
            stack.append((r,c))

            while stack:
                row, col = stack.pop()
                directions = [[1,0],[-1,0],[0,1],[0,-1]]

                for dr, dc in directions:
                    if (row+dr in range(rows) and
                        col +dc in range(cols) and
                        grid[row+dr][col+dc]=="1" and 
                        (row+dr,col+dc) not in visited):
                        stack.append((row+dr,col+dc))
                        visited.add((row+dr,col+dc))

        for r in range(rows):
            for c in range(cols):
                if grid[r][c]=="1" and (r,c) not in visited:
                    dfs(r,c)
                    countIslands+=1
        return countIslands 