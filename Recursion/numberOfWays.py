# Kind of stupid way to do it but very simple to think of - lol!!

import sys
sys.setrecursionlimit(1000000)
class Solution:

    def solve(self, source, target):
        count = 0
        def dfs(num):
            nonlocal count
            if num > target:
                return
            if num == target:
                count+=1
                return
            
            dfs(num+1)
            dfs(num+2)
            dfs(num+3)
        dfs(source)
        return count
        

def main():
    input = sys.stdin.readline
    s,e = map(int, input().split())
    solution = Solution()
    print(solution.solve(s,e))

 
if __name__ == '__main__':
    main()
    
    
# better way to do it - 

