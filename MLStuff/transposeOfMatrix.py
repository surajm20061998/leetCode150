# Question at https://www.deep-ml.com/problems/2
def transpose_matrix(a: list[list[int|float]]) -> list[list[int|float]]:
    """
    Transpose a 2D matrix by swapping rows and columns.
    
    Args:
        a: A 2D matrix of shape (m, n)
    
    Returns:
        The transposed matrix of shape (n, m)
    """
    # Your code here
    rows = len(a)
    cols = len(a[0])
    res = [[0]* rows for _ in range(cols)]
    for i in range(rows):
        for j in range(cols):
            res[j][i] = a[i][j]
    return res


# Pytorch Implementation
import torch

def transpose_matrix(a) -> torch.Tensor:
    """
    Transpose a 2D matrix using PyTorch.
    
    Args:
        a: A 2D matrix (can be list, numpy array, or torch.Tensor)
    
    Returns:
        A transposed torch.Tensor
    """
    a_t = torch.as_tensor(a)
    # Your code here
    return a_t.T