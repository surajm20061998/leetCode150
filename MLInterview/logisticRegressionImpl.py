import torch

def stable_sigmoid(z):
    exp_neg = torch.exp(-torch.clamp(z, min=0))
    exp_pos = torch.exp(torch.clamp(z, max=0))
    return torch.where(z>=0,
                       1.0/(1.0 + exp_neg),
                       exp_pos/(1.0+exp_pos)
                       )
    
def bce_from_logits(z,y):
    losses = (
        torch.clamp(z,min=0) - z*y + torch.log1p(torch.exp(-torch.abs(z)))
    )
    return losses.mean()

def logistic_regression_step(X : torch.Tensor,
                             y : torch.Tensor,
                             w : torch.Tensor,
                             b : torch.Tensor,
                             learning_rate : float):
    """
    Perform one full-batch logistic regression gradient step.
    X: [N, D]
    y: [N], binary labels
    w: [D]
    b: scalar tensor
    Returns:
        loss: scalar, evaluated before the update
        new_w: [D]
        new_b: scalar
        grad_w: [D]
        grad_b: scalar
    """
    # -------------------------
    # 1. Input validation
    # -------------------------
    if X.ndim != 2:
        raise ValueError("X must have shape [N, D]")
    if y.ndim != 1:
        raise ValueError("y must have shape [N]")
    if w.ndim != 1:
        raise ValueError("w must have shape [D]")
    if b.ndim != 0:
        raise ValueError("b must be a scalar")
    
    N, D = X.shape
    
    if N == 0 or D == 0:
        raise ValueError("X must be nonempty")
    if y.shape[0] != N:
        raise ValueError("y must have N elements")
    if w.shape[0] != D:
        raise ValueError("w must have D elements")
    
    tensors = (X, y, w, b)
    if not all(t.is_floating_point() for t in tensors):
        raise TypeError("Inputs must be floating-point tensors")
    if not all(t.dtype == X.dtype for t in tensors):
        raise ValueError("All tensors must have the same dtype")
    if not all(t.device == X.device for t in tensors):
        raise ValueError("All tensors must be on the same device")
    if not all(torch.isfinite(t).all().item() for t in tensors):
        raise ValueError("Inputs must be finite")
    if not torch.all((y == 0) | (y == 1)).item():
        raise ValueError("Labels must be 0 or 1")
    if not (0 < learning_rate < float("inf")):
        raise ValueError("Learning rate must be positive and finite")
    
    # -------------------------
    # 2. Forward pass
    # -------------------------
    logits = X@w + b
    probabilities = stable_sigmoid(logits)
    loss = bce_from_logits(logits, y)
    
    # -------------------------
    # 3. Calculate gradients
    # -------------------------
    residuals = probabilities - y
    grad_w = (X.T@residuals)/N
    grad_b = residuals.mean()
    
    # -------------------------
    # 4. Gradient descent step
    # -------------------------
    new_w = w - learning_rate*grad_w
    new_b = b - learning_rate*grad_b
    return loss, new_w, new_b, grad_w, grad_b