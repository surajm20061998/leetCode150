# Easy Graph Problem
# Just find the node with n-1 incoming edges and 0 outgoing edges

from collections import defaultdict
class Solution:
    def findJudge(self, n: int, trust: List[List[int]]) -> int:
        incomingList = [0]*(n+1)
        outgoingList = [0]*(n+1)
        for u,v in trust:
            incomingList[v]+=1
            outgoingList[u]+=1
        for i in range(1,n+1):
            if incomingList[i] == n-1 and outgoingList[i] == 0:
                return i
        return -1        