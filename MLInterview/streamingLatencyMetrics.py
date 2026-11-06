import math

def streaming_latency_metrics(start_time, events):
    """
    Compute latency metrics from a time-ordered event stream.
    Args:
        start_time: Request start timestamp.
        events: Iterable of (timestamp, token_count).
    Returns:
        {
            "ttft": float | None,
            "e2e": float | None,
            "gaps": list[float],
            "total_tokens": int
        }
    Rules:
        - token_count must be a nonnegative integer.
        - Event timestamps must be nondecreasing.
        - Event timestamps cannot precede start_time.
        - Zero-token events do not contribute to TTFT,
          E2E, or gaps.
        - Equal timestamps are allowed.
    """
    
    if not isinstance(start_time, (int, float)):
        raise TypeError("start_time must be numeric")
    if not math.isfinite(start_time):
        raise ValueError("start_time must be finite")
    
    ttft = None
    e2e = None
    gaps = []
    total_tokens = 0
    
    previous_event_time = start_time
    previous_token_time = None
    
    for timestamp, token_count in events:
         # Validate timestamp
        if not isinstance(timestamp, (int, float)):
            raise TypeError("timestamp must be numeric")
        if not math.isfinite(timestamp):
            raise ValueError("timestamp must be finite")
        if timestamp < start_time:
            raise ValueError(
                "Event timestamp cannot precede request start"
            )
        if timestamp < previous_event_time:
            raise ValueError(
                "Event timestamps must be nondecreasing"
            )
        # Validate token count
        if (
            not isinstance(token_count, int)
            or isinstance(token_count, bool)
            or token_count < 0
        ):
            raise ValueError(
                "token_count must be a nonnegative integer"
            )
        # Update timestamp ordering for ALL events,
        # including zero-token events.
        previous_event_time = timestamp
        total_tokens += token_count
        if token_count == 0:
            continue
        
        if ttft is None:
            ttft = timestamp - start_time
        if previous_token_time is not None:
            gaps.append(timestamp - previous_token_time)
            
        e2e = timestamp - start_time
        
        previous_token_time = timestamp
        
    return {
        "ttft" : ttft,
        "e2e" : e2e,
        "gaps" : gaps,
        "total_tokens" : total_tokens
    }