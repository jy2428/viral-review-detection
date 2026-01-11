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

    # 문자열 날짜 → datetime 변환
    timestamps = []
    for d in review_dates:
        if isinstance(d, str):
            timestamps.append(datetime.fromisoformat(d))
        else:
            timestamps.append(d)

    # 시간순 정렬
    timestamps.sort()

    # 리뷰 간 시간 간격 (일 단위)
    intervals = [
        (timestamps[i] - timestamps[i - 1]).days
        for i in range(1, len(timestamps))
    ]

    intervals = np.array(intervals)

    # 짧은 간격 비율 계산
    short_interval_ratio = np.mean(intervals <= interval_threshold)

    # burst 점수 계산
    burst_score = short_interval_ratio * spike_weight

    # 0~1 범위로 클리핑
    return float(min(burst_score, 1.0))
