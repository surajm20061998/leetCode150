# Difficult wording, becomes very easy once the problem is split into the 3 parts
# basic idea is that find cells on the edge of the grid where board[r][c] == "O" and do a dfs to find more such areas
# and make them into "T"s
# Then capture the rest of the "O"s since they are not connected to the edge means they are surrounded
# lastly turn all the "T"s back to "O"s 

class Solution:
    def solve(self, board: List[List[str]]) -> None:
        ROWS, COLS = len(board), len(board[0])

        def capture(r,c):
            if (r not in range(ROWS) or c not in range(COLS) or board[r][c]!="O") :
                return
            board[r][c] = "T"
            capture(r+1,c)
            capture(r-1,c)
            capture(r,c+1)
            capture(r,c-1)

        # 1 . Capture unsurrounded regions (O->T)
        for r in range(ROWS):
            for c in range(COLS):
                if (board[r][c] == "O" and 
                    (r in [0,ROWS-1] or c in [0,COLS-1])):
                    capture(r,c)

        # 2 . Capture surrounded regions (O->X)
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] == "O":
                    board[r][c] = "X"
        # 3 . Uncapture unsurrounded regions (T->O)
        for r in range(ROWS):
            for c in range(COLS):
                if board[r][c] == "T":
                    board[r][c] = "O"
        