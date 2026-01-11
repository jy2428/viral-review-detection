"""
Morphological Analysis Module

This module computes a stylistic suspicious score
based on linguistic patterns in review texts.
Repetitive and uniform writing styles are treated
as potential viral marketing signals.
"""

from typing import List


def process_morph(
    review_texts: List[str],
    repetition_threshold: float = 0.6
) -> float:
    """
    Calculate morphological (stylistic) suspicious score.

    Parameters
    ----------
    review_texts : List[str]
        List of review texts.
    repetition_threshold : float
        Threshold ratio for detecting repetitive writing styles.

    Returns
    -------
    float
        Morphological suspicious score (0~1).
    """

    if not review_texts:
        return 0.0

    unique_texts = set()
    for text in review_texts:
        if text and text.strip():
            unique_texts.add(text.strip())

    repetition_ratio = 1 - (len(unique_texts) / len(review_texts))

    return float(min(repetition_ratio / repetition_threshold, 1.0))
