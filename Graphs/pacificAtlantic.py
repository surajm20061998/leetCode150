#Optimal Solution
#Time Complexity: O(m * n)
#Space Complexity: O(m * n)
class Solution:
    def pacificAtlantic(self, heights: List[List[int]]) -> List[List[int]]:

        ROWS, COLS = len(heights), len(heights[0])
        
        pac, atl = set(), set() #Two sets to store elements that can reach pacfic ocean and atlantic ocean

        def dfs(r,c, visit, prevHeight):
            if (((r,c) in visit) or #If already visited or in set then no need to process again
                (r<0 or c<0 or r==ROWS or c==COLS) or #Boundary Check
                heights[r][c] < prevHeight): # If the current cell is less than previous cell water wont flow 
                return
            visit.add((r,c)) # Add to set   
            dfs(r+1,c,visit,heights[r][c])
            dfs(r-1,c,visit,heights[r][c])
            dfs(r,c+1,visit,heights[r][c])
            dfs(r,c-1,visit,heights[r][c])

        for c in range(COLS):
            dfs(0,c,pac,heights[0][c]) # Do dfs and fill the pac set starting from top row of the grid
            dfs(ROWS-1,c,atl,heights[ROWS-1][c]) # Do dfs and fill the atl set starting from bottom row of the grid

        for r in range(ROWS):
            dfs(r,0,pac,heights[r][0]) # Do dfs and fill the pac set starting from the left column of the grid
            dfs(r,COLS-1,atl,heights[r][COLS-1]) # Do dfs and fill the atl set starting from the right column of the grid
        #Once we have both the sets filled out after traversing from all 4 directions, we just need to find the common pairs from both sets

        ans = []
        for r in range (ROWS):
            for c in range (COLS):
                if (r,c) in pac and (r,c) in atl:
                    ans.append([r,c])
        return ans

        