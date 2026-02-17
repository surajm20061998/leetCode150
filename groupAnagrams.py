from collections import defaultdict
class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:
        ans = defaultdict(list)
        for s in strs:
            key = ''.join(sorted(s))
            print(key)
            ans[key].append(s)
        
        return list(ans.values())
        
        