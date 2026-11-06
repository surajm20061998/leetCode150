import torch

def classification_metrics(y_true : torch.Tensor,
                           scores : torch.Tensor,
                           threshold : float = 0.5):
    """
    Compute binary classification metrics.
    Args:
        y_true: [N], binary labels (0 or 1)
        scores: [N], finite prediction scores
        threshold: Predict positive when score >= threshold
    Returns:
        Dictionary containing:
        TP, FP, TN, FN, precision, recall, F1
    Empty-input policy:
        Reject empty inputs with ValueError.
    Zero-denominator policy:
        Return 0.0.
    """
    # Step 1: Validate shapes
    if y_true.ndim != 1 or scores.ndim != 1:
        raise ValueError("Inputs must be 1D tensors")
    if y_true.shape != scores.shape:
        raise ValueError("Labels and scores must have matching shapes")
    if y_true.numel() == 0:
        raise ValueError("Inputs cannot be empty")
    if y_true.device != scores.device:
        raise ValueError("Inputs must be on the same device")
    if not torch.all((y_true == 0) | (y_true == 1)).item():
        raise ValueError("Labels must be binary: 0 or 1")
    if not scores.is_floating_point():
        raise TypeError("Scores must be floating-point")
    if not torch.isfinite(scores).all().item():
        raise ValueError("Scores must be finite")
    threshold_tensor = torch.as_tensor(
        threshold,
        dtype=scores.dtype,
        device=scores.device
    )
    if threshold_tensor.ndim != 0:
        raise ValueError("Threshold must be scalar")
    if not torch.isfinite(threshold_tensor).item():
        raise ValueError("Threshold must be finite")
    
    # Step 2: Convert scores to predictions
    y_pred = scores >= threshold_tensor
    actual_positive = y_true == 1
    actual_negative = y_true == 0
    
    # Step 3: Compute confusion matrix
    TP = int((y_pred & actual_positive).sum().item())
    FP = int((y_pred & actual_negative).sum().item())
    TN = int((~y_pred & actual_negative).sum().item())
    FN = int((~y_pred & actual_positive).sum().item())
    
    precision = TP/(TP+FP) if TP+FP > 0 else 0.0
    recall = TP/(TP+FN) if TP+FN > 0 else 0.0
    f1 = 2*(precision*recall/(precision + recall)) if precision + recall > 0 else 0.0
    
    return {
        "TP": TP,
        "FP": FP,
        "TN": TN,
        "FN": FN,
        "precision": precision,
        "recall": recall,
        "f1": f1
    }