import torch


def kmeans(
    X: torch.Tensor,
    initial_centroids: torch.Tensor,
    max_iter: int = 100,
    tol: float = 1e-5
):
    X = torch.as_tensor(X, dtype=torch.float64)

    centroids = torch.as_tensor(
        initial_centroids,
        dtype=torch.float64,
        device=X.device
    ).clone()

    if X.ndim != 2 or centroids.ndim != 2:
        raise ValueError("Expected 2D tensors")

    N, D = X.shape
    K = centroids.shape[0]

    if not (1 <= K <= N):
        raise ValueError("K must satisfy 1 <= K <= N")

    if centroids.shape[1] != D:
        raise ValueError("Feature dimensions must match")

    if max_iter < 0 or tol < 0:
        raise ValueError("Invalid max_iter or tol")

    if not torch.isfinite(X).all() or not torch.isfinite(centroids).all():
        raise ValueError("Inputs must be finite")

    def assign_labels(centers):
        distances = torch.empty(
            (N, K),
            dtype=X.dtype,
            device=X.device
        )

        for k in range(K):
            diff = X - centers[k]
            distances[:, k] = (diff ** 2).sum(dim=1)

        return torch.argmin(distances, dim=1)

    for _ in range(max_iter):

        # Step 1: Assign each point to its nearest centroid
        labels = assign_labels(centroids)

        # Step 2: Update centroids
        new_centroids = centroids.clone()

        for k in range(K):
            members = X[labels == k]

            if members.shape[0] > 0:
                new_centroids[k] = members.mean(dim=0)

        # Step 3: Calculate centroid movement
        movement = torch.linalg.vector_norm(
            new_centroids - centroids,
            dim=1
        )

        centroids = new_centroids

        # Step 4: Check convergence
        if movement.max().item() <= tol:
            break

    # Step 5: Recompute assignments using final centroids
    labels = assign_labels(centroids)

    return centroids, labels