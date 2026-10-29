# Question at https://www.deep-ml.com/problems/1
def dotProduct (u,v):
    if len(u)!=len(v):
        raise ValueError("Vectors must have the same length")
    result = 0
    for i in range(len(u)):
        result+=u[i]*v[i]
    return result

def matrix_dot_vector(a: list[list[int|float]], b: list[int|float]) -> list[int|float]:
	# Return a list where each element is the dot product of a row of 'a' with 'b'.
	# If the number of columns in 'a' does not match the length of 'b', return -1.
	if len(a[0])!=len(b):
		return -1
	result = []
	for row in a:
		result.append(dotProduct(row,b))
	return result



# PyTorch Implementation 
import torch

def matrix_dot_vector(a, b) -> torch.Tensor:
    """
    Compute the product of matrix `a` and vector `b` using PyTorch.
    Inputs can be Python lists, NumPy arrays, or torch Tensors.
    Returns a 1-D tensor of length m, or tensor(-1) if dimensions mismatch.
    """
    a_t = torch.as_tensor(a, dtype=torch.float)
    b_t = torch.as_tensor(b, dtype=torch.float)
    # Dimension mismatch check
    if a_t.size(1) != b_t.size(0):
        return torch.tensor(-1)
    # Your implementation here
    return a_t@b_t
    pass
