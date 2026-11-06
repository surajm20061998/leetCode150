import torch 

def linear_regression_step(X : torch.Tensor,
                           y : torch.Tensor,
                           w : torch.Tensor,
                           b : torch.Tensor) :
    """
    Compute predictions, MSE loss, and analytical gradients.
    X: [N, D]
    y: [N]
    w: [D]
    b: scalar tensor []
    Returns:
        predictions: [N]
        loss: scalar
        grad_w: [D]
        grad_b: scalar
    """
    
    # Step 1: Validate shapes

    if X.ndim != 2:
        raise ValueError("X must have shape [N, D]")
    if y.ndim != 1:
        raise ValueError("y must have shape [N]")
    if w.ndim != 1:
        raise ValueError("w must have shape [D]")
    if b.ndim != 0:
        raise ValueError("b must be a scalar tensor")
    
    N, D = X.shape
    
    if N == 0 or D == 0:
        raise ValueError("X must be nonempty")
    if y.shape[0] != N:
        raise ValueError("y must contain N targets")
    if w.shape[0] != D:
        raise ValueError("w must contain D weights")
    
    # Validate floating-point tensors
    tensors = (X, y, w, b)
    
    if not all(t.is_floating_point() for t in tensors):
        raise TypeError("All inputs must be floating-point tensors")
    if not all(t.device == X.device for t in tensors):
        raise ValueError("All inputs must be on the same device")
    if not all(t.dtype == X.dtype for t in tensors):
        raise ValueError("All inputs must have the same dtype")
    if not all(torch.isfinite(t).all().item() for t in tensors):
        raise ValueError("All inputs must be finite")
    
    predictions = X@w + b
    residuals = predictions-y
    loss = (residuals**2).mean()
    grad_w = (2.0/N)*(X.T@residuals)
    grad_b = (2.0)*residuals.mean()
    return predictions, loss, grad_w, grad_b

