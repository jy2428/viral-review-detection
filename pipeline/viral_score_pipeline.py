"""
Viral Review Scoring Pipeline

This module integrates morphological, sentiment,
and temporal analysis results to compute a final
viral review score.
"""

from models.morph_analysis.morph_model import process_morph
from models.sentiment_analysis.sentiment_model import process_sentiment
from models.temporal_analysis.temporal_features import process_time


def calculate_viral_score(
    morph_score: float,
    sentiment_score: float,
    temporal_score: float,
    weights=(0.4, 0.3, 0.3)
) -> float:
    """
    Calculate final viral score using weighted sum.
    """
    w_morph, w_sent, w_temp = weights
    return (
        w_morph * morph_score +
        w_sent * sentiment_score +
        w_temp * temporal_score
    )


def analyze_reviews(
    review_texts,
    review_dates
):
    """
    Run all analysis modules and return final viral score.
    """
    morph_score = process_morph(review_texts)
    sentiment_score = process_sentiment(review_texts)
    temporal_score = process_time(review_dates)

    final_score = calculate_viral_score(
        morph_score,
        sentiment_score,
        temporal_score
    )

    return {
        "morph_score": morph_score,
        "sentiment_score": sentiment_score,
        "temporal_score": temporal_score,
        "viral_score": final_score
    }


def get_viral_reviews(
    reviews,
    threshold=0.7
):
    """
    Filter reviews considered as viral based on score threshold.
    """
    viral_reviews = [
        r for r in reviews
        if r["viral_score"] >= threshold
    ]
    return viral_reviews
