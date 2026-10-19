import sys
sys.setrecursionlimit(1000000)
class Solution:

    def solve(self, n, arr):
        marray = [0]*n
        def dfs(index,mvalue):
            if index == len(arr):
                return
            mvalue = max(mvalue, arr[index])
            marray[index] = mvalue
            dfs(index+1, mvalue)
            
        dfs(0,arr[0])
        return marray
        
        

def main():
    input = sys.stdin.readline
    n = int(input())
    arr = list(map(int, input().split()))
    solution = Solution()
    print(*solution.solve(n,arr))

 
if __name__ == '__main__':
    main()