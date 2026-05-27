# MY solution
# Just iterate every nums[i:i+k] for i in range(len(nums)-k+1)

class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        ans =[]

        for i in range(len(nums)-k+1):
            #print(nums[i:i+k], max(nums[i:i+k]))
            ans.append(max(nums[i:i+k]))
        return ans
        
# Optimal Solution
# Monotonically Decreasing Queues
# Time complexity = O(n)
# Space Complexity = O(k)
class Solution:
    def maxSlidingWindow(self, nums: List[int], k: int) -> List[int]:
        ans =[]
        q = deque() # store indices
        l=r=0
        while r < len(nums):
            # Since we are using a monotonically Decreasing queue if nums[r] > the right most element in the deque we keep popping
            while q and nums[q[-1]] < nums[r]:
                q.pop()
            
            #Once we are done with popping and criteria for monotonically decreasing deque is met we can add
            q.append(r)

            #Window has moved, so we delete the leftmost element
            if l>q[0]:
                q.popleft() 

            #Window has moved so we update our ans array with current max (which will always be nums[q[0]])
            # And increment l as well
            if r + 1 >= k:
                ans.append(nums[q[0]])
                l+=1
            r+=1
        return ans      