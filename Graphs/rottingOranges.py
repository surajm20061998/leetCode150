# Multi Source BFS
# Optimal Solution
# Time Complexity = O(m*n)
# Space Complexity = O(m*n)
class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        q = deque()
        time, fresh = 0,0
        ROWS, COLS = len(grid), len(grid[0])
        for r in range (ROWS):
            for c in range (COLS):
                if grid[r][c]==1:
                    fresh+=1
                if grid[r][c]==2:
                    q.append([r,c]) # Store the coordinates of initially rotten oranges in the queue directly
        
        directions = [[1,0],[-1,0],[0,1],[0,-1]] #directions in which rot can happen

        while q and fresh>0: #the conditions to break the loop
            #This for loop is basically 1 unit of time
            for i in range(len(q)):
                r,c = q.popleft()
                for dr,dc in directions:
                    row,col = r+dr, c+dc
                    #check for bounds and if grid[row][col] is fresh make it rotten
                    if (row<0 or row==len(grid) or
                        col<0 or col==len(grid[0]) or
                        grid[row][col]!=1):
                        continue
                    grid[row][col]=2
                    q.append([row,col]) # Since orange is rotten now, add it to queue
                    fresh-=1
            time+=1 #Increment time evrytime the loop ends
        return time if fresh==0 else -1

# Saw this again 
# multi source bfs without using visited set, probably since we already have 0,1,2 to track and only want to visit the 1s and turn them to 2 anyways once visited

class Solution:
    def orangesRotting(self, grid: List[List[int]]) -> int:
        ROWS, COLS = len(grid), len(grid[0])
        time = 0
        q = deque()
        fresh = 0

        for r in range(ROWS):
            for c in range(COLS):
                if grid[r][c] == 1:
                    fresh+=1
                if grid[r][c] == 2:
                    q.append([r,c])
        directions = [[1,0],[-1,0],[0,1],[0,-1]]
        while q and fresh>0:
            for i in range(len(q)):
                r,c = q.popleft()
                for dr,dc in directions:
                    row, col = r+dr, c+dc
                    if (row not in range(ROWS) or col not in range(COLS) or grid[row][col]!=1):
                        continue
                    grid[row][col] = 2
                    q.append([row,col])
                    fresh-=1
            time+=1
        return time if fresh==0 else -1
