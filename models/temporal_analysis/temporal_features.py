"""
Temporal Analysis Module

This module analyzes temporal patterns of reviews
to detect abnormal burst behavior.
"""

import numpy as np
from datetime import datetime


def process_time(
    review_dates,
    interval_threshold=1,
    spike_weight=1.0
):
    """
    Calculate temporal suspicious score based on review timestamps.

    Parameters
    ----------
    review_dates : list
        List of review timestamps (datetime or string).
    interval_threshold : int
        Threshold (days) for detecting abnormal intervals.
    spike_weight : float
        Weight factor for burst amplification.

    Returns
    -------
    float
        Temporal suspicious score (0~1).
    """

    if len(review_dates) < 2:
        return 0.0

    timestamps = []
    for d in review_dates:
        if isinstance(d, str):
            timestamps.append(datetime.fromisoformat(d))
        else:
            timestamps.append(d)

    timestamps.sort()

    intervals = [
        (timestamps[i] - timestamps[i - 1]).days
        for i in range(1, len(timestamps))
    ]

    intervals = np.array(intervals)

    short_interval_ratio = np.mean(intervals <= interval_threshold)
    burst_score = short_interval_ratio * spike_weight

    return float(min(burst_score, 1.0))
