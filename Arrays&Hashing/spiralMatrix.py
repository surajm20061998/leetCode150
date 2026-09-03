# Pretty easy once the solution is figured out
# the only tricky part is after completing half the spiral
# if not is there to handle the moment when, halfway through a spiral iteration, there are no rows or columns left to traverse.
# Need to check that again

class Solution:
    def spiralOrder(self, matrix: List[List[int]]) -> List[int]:
        ans = []  
        left,right = 0, len(matrix[0])
        top,bot = 0,len(matrix)

        while left<right and top<bot:
            #top row left to right
            for i in range(left, right):
                ans.append(matrix[top][i])
            #top row done so increment top
            top+=1
            #last col top to bot
            for i in range(top,bot):
                ans.append(matrix[i][right-1])
            #last col done to decrement right
            right-=1

            if not (left <right and top<bot):
                break

            #bottom row right to left
            for i in range(right-1,left-1,-1):
                ans.append(matrix[bot-1][i])
            #last row done so decrement bot
            bot-=1

            #first col bot to top
            for i in range(bot-1,top-1,-1):
                ans.append(matrix[i][left])
            #first col done so increment left
            left+=1
        return ans

