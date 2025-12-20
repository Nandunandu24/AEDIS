from textblob import TextBlob


def analyze_sentiment(text: str) -> float:
    """
    Returns sentiment polarity in range [-1, 1]
    """
    if not text.strip():
        return 0.0
    return round(TextBlob(text).sentiment.polarity, 2)
