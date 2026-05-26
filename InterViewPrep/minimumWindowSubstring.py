# Optimal Solution
# Time Complexity = O(n)
# Space Complexity = O(n)

class Solution:
    def minWindow(self, s: str, t: str) -> str:
        if t=="" : return ""

        tWindow, sWindow = {},{}

        for c in t:
            tWindow[c] = tWindow.get(c,0) + 1 # if c exists in map return value of c else 0
        
        have, need = 0, len(tWindow)
        res, resLen = [-1,-1], float("infinity")
        l = 0

        for r in range(len(s)):
            c = s[r]
            sWindow[c] = sWindow.get(c,0) + 1 # if c exists in map return value of c else 0

            #See if condition for this charecter is fulfilled
            if c in tWindow and sWindow[c] == tWindow[c]:
                have+=1 #Meaning we have completed the requirement for 1 charecter

            while have == need: # Condition is satisfied
                if (r-l+1) < resLen: # New satisfying window is lesser in size than the older one
                    res = [l,r] #Update
                    resLen = r-l+1 #Update

                #Start shrinking the sWindow from left
                sWindow[s[l]] -= 1
                if s[l] in tWindow and sWindow[s[l]] < tWindow[s[l]]: # If we shrink and pop out the charecter that was in our target window
                    have-=1
                l+=1 
        l,r = res
        return s[l:r+1] if resLen != float("infinity") else ""

        