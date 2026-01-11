"""
Sentiment Analysis Module

This module computes a sentiment-based suspicious score
from review texts. Overly positive sentiment concentration
is treated as a potential viral marketing signal.
"""

from typing import List


def process_sentiment(
    review_texts: List[str],
    positive_threshold: float = 0.7
) -> float:
    """
    Calculate sentiment suspicious score.

    Parameters
    ----------
    review_texts : List[str]
        List of review texts.
    positive_threshold : float
        Threshold ratio for detecting overly positive sentiment.

    Returns
    -------
    float
        Sentiment suspicious score (0~1).
    """

    if not review_texts:
        return 0.0

    positive_count = 0

    for text in review_texts:
        if text and len(text.strip()) > 0:
            positive_count += 1

    positive_ratio = positive_count / len(review_texts)

    return float(min(positive_ratio / positive_threshold, 1.0))
