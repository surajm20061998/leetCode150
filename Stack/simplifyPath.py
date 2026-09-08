# Need to review this question more and understand end to end
# Got some clue but need to review again
class Solution:
    def simplifyPath(self, path: str) -> str:
        stk = []
        curr = ""
        for c in path + "/":
            if c == "/":
                if curr == "..":
                    if stk : stk.pop()
                elif curr!="" and curr!=".":
                    stk.append(curr)
                curr = ""

            else:
                curr+=c
        return "/" + "/".join(stk)
        
        