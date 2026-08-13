# My Solution
# Not the most optimal I guess
# Put the nums array in collections.counter and the just traverse the counter dict

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:

        rows = collections.defaultdict(set)
        cols = collections.defaultdict(set)
        squares = collections.defaultdict(set) # key here will be (r//3,c//3)

        for r in range(9):
            for c in range(9):
                if board[r][c]==".":
                    continue
                if (board[r][c] in rows[r] or
                    board[r][c] in cols[c] or
                    board[r][c] in squares[(r//3,c//3)]):
                    return False
                #else add it o the sets
                cols[c].add(board[r][c])
                rows[r].add(board[r][c])
                squares[(r//3,c//3)].add(board[r][c])
        return True        
    

# Optimal Solution
# Need to see this once again and understand

class Solution:
    def majorityElement(self, nums: List[int]) -> List[int]:
        count = collections.defaultdict(int)

        for n in nums:
            count[n]+=1

            if len(count)<=2:
                continue
            
            newCount = defaultdict(int)
            for n,c in count.items():
                if c>1:
                    newCount[n] = c-1
            count = newCount
        
        res = []
        for n in count:
            if nums.count(n) > len(nums)//3:
                res.append(n)
        return res