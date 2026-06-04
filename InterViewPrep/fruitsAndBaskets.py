# Sliding Window with K = 2
# Basically the question is about longest subaary with only 2 unique elements
# Time Complexity: O(n)
# Space Complexity: O(1)
from collections import defaultdict
class Solution:
    def totalFruit(self, fruits: List[int]) -> int:

        start = 0 
        freq = defaultdict(int)
        ans = -1
        count = 0

        for end in range(len(fruits)):
            freq[fruits[end]] += 1
            count +=1

            while len(freq) > 2:
                freq[fruits[start]] -= 1
                count -= 1
                if freq[fruits[start]] == 0:
                    del freq[fruits[start]]
                
                start +=1
            ans = max(ans, count)
        return ans if ans!=-1 else 1


        