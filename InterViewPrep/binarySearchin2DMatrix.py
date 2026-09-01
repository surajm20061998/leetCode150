# Binary Search in 2 D Matrix

class Solution:
    def searchMatrix(self, matrix: List[List[int]], target: int) -> bool:
        ROWS = len(matrix)
        COLS = len(matrix[0])
        top, bot = 0, ROWS-1
        while top <=bot:
            row = (top+bot)//2 # Try to Find mid row
            if target > matrix[row][-1]:
                top = row+1
            elif target < matrix[row][0]:
                bot = row-1 
            else:
                break # If we find a row where the element could exist we exit to do ID binary search on that specific row
        
        if not (top<=bot): # The above loop could have exhausted in that case we should  just return false
            return False
        
        row = (top+bot)//2 # The above loop has not exhausted, so we do 1D binary search on the mid row
        l,r = 0, COLS-1
        while l<=r:
            m = (l+r)//2
            if target > matrix[row][m]:
                l=m+1
            elif target < matrix[row][m]:
                r = m-1
            else : 
                return True
        return False
        