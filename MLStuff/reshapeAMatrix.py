# Question at https://www.deep-ml.com/problems/3

import numpy as np

def reshape_matrix(a: list[list[int|float]], new_shape: tuple[int, int]) -> list[list[int|float]]:
	#Write your code here and return a python list after reshaping by using numpy's tolist() method
	rows = len(a)
	cols = len(a[0])
	r,c = new_shape
	if r*c == rows*cols:
		flat = []
		for i in range(rows):
			for j in range(cols):
				flat.append(a[i][j])
		
		reshaped_matrix = []
		for i in range(0, len(flat), c):
			reshaped_matrix.append(flat[i:i+c])
		# do
		return reshaped_matrix
	else:
		return []

# pytorch Implementation

import torch

def reshape_matrix(a, new_shape) -> torch.Tensor:
    """
    Reshape a 2D matrix `a` to shape `new_shape` using PyTorch.
    Inputs can be Python lists, NumPy arrays, or torch Tensors.
    Returns a tensor of shape `new_shape`, or an empty tensor on mismatch.
    """
    # Dimension check
    if len(a) * len(a[0]) != new_shape[0] * new_shape[1]:
        return torch.tensor([])
    # Convert to tensor and reshape
    a_t = torch.as_tensor(a, dtype=torch.float)
    # Your implementation here
    return a_t.reshape(new_shape[0], new_shape[1])
