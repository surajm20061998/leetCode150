import torch

def cosine_top_k(
    query: torch.Tensor,
    embeddings: torch.Tensor,
    k: int
):
    """
    Return top-k cosine similarities and indices.
    query: [D]
    embeddings: [N, D]
    k: integer satisfying 1 <= k <= N
    Returns:
        top_scores: [k]
        top_indices: [k]
    Ordering:
        1. Higher cosine similarity first.
        2. Smaller index first on ties.
    Zero-vector convention:
        Cosine similarity is 0 if either vector is zero.
    """
    # -------------------------
    # 1. Input validation
    # -------------------------
    
    if query.ndim != 1:
        raise ValueError("query must have shape [D]")
    if embeddings.ndim != 2:
        raise ValueError("embeddings must have shape [N, D]")

    N, D = embeddings.shape
    
    if D == 0:
        raise ValueError("D must be positive")
    if query.shape[0] != D:
        raise ValueError("Feature dimensions must match")
    if not (1 <= k <= N):
        raise ValueError("k must satisfy 1 <= k <= N")
    if not query.is_floating_point():
        raise TypeError("query must be floating-point")
    if not embeddings.is_floating_point():
        raise TypeError("embeddings must be floating-point")
    if query.dtype != embeddings.dtype:
        raise ValueError("Dtypes must match")
    if query.device != embeddings.device:
        raise ValueError("Devices must match")
    if not torch.isfinite(query).all().item():
        raise ValueError("query must contain finite values")
    if not torch.isfinite(embeddings).all().item():
        raise ValueError("embeddings must contain finite values")

    # -------------------------
    # 2. Compute cosine scores
    # -------------------------
    
    dot_products = embeddings @ query
    query_norm = torch.linalg.vector_norm(query)
    embedding_norms = torch.linalg.vector_norm(embeddings, dim=1)
    denominator = embedding_norms * query_norm
    
    safe_denominator = torch.where(
        denominator > 0,
        denominator,
        torch.ones_like(denominator)
    )
    
    similarities = dot_products/safe_denominator
    
    similarities = torch.where(
        denominator > 0,
        similarities,
        torch.zeros_like(similarities)
    )
    
    # -------------------------
    # 3. Stable descending sort
    # -------------------------
    
    sorted_indices = torch.argsort(
        similarities,
        descending = True,
        stable = True
    )
    
    top_indices = sorted_indices[:k]
    top_scores = similarities[top_indices]
    return top_scores, top_indices
    