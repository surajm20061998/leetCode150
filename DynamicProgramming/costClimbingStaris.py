# O(n)
# Add a 0 to end of cost array
# To reach to beyond end of cost array, it ll be min(cost[i]+cost[i+1], cost[i]+cost[i+2]) starting from end of the array
# Return min of the first 2 elements of the array
class Solution:
    def minCostClimbingStairs(self, cost: List[int]) -> int:
        cost.append(0)
        for i in range(len(cost)-3,-1,-1):
            cost[i] = min((cost[i] + cost[i+1]), (cost[i] + cost[i+2]))
        return min(cost[0], cost[1])
        