import sys

def dotProduct (u,v):
    if len(u)!=len(v):
        raise ValueError("Vectors must have the same length")
    result = 0
    for i in range(len(u)):
        result+=u[i]*v[i]
    return result

def projectionOfvOntoU(u,v):
    return [i * (dotProduct(u,v)/dotProduct(u,u)) for i in u]

def isOrthogonal(u,v):
    if dotProduct(u,v) == 0:
        return True
    else :
        return False

def main():
    input = sys.stdin.readline
    u = list(map(int, input().split()))
    v = list(map(int, input().split()))
    print(dotProduct(u,v))
    print(projectionOfvOntoU(v,u))
    print(isOrthogonal(u,v))

 
if __name__ == '__main__':
    main()