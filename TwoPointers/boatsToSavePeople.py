# Pretty simple 2 pointer solution
# First sort the array
# then in a loop place heaviest person and if there is more space for a luighter person place the lighter person


class Solution:
    def numRescueBoats(self, people: List[int], limit: int) -> int:
        people.sort()
        res = 0
        l,r = 0, len(people)-1
        while(l<=r):
            remain = limit - people[r]
            r-=1
            res+=1
            if l<=r and remain >= people[l]:
                l+=1
        return res
