import re
from keywords import QUALITY_KEYWORDS


class Scorer:
    def __init__(self, min_score=30):
        self.min_score = min_score

    def score_text(self, text):
        score = 50
        t = (text or '').lower()
        for kw in QUALITY_KEYWORDS:
            if kw in t:
                score += 5
        if len(t) > 200:
            score += 10
        if len(t) > 500:
            score += 10
        if re.search(r'\b[\w.-]+@[\w.-]+\.\w+\b', t):
            score += 10
        if re.search(r'\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', t):
            score += 10
        return max(0, min(100, score))
