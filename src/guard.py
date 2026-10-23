
"""Simple rule-based scope guard for customer support questions."""

import re

from src.prompts import FALLBACK_SENTENCE

# Terms associated with the fictional store's supported topics.
SUPPORT_TERMS = {
    "order", "orders", "shipping", "delivery", "delivered",
    "dispatch", "courier", "tracking", "refund", "refunds",
    "return", "returns", "exchange", "damaged", "defective",
    "broken", "wrong item", "incorrect item", "warranty",
    "payment", "payments", "transaction", "product", "products",
    "headphones", "keyboard", "keyboards", "speaker", "speakers",
    "webcam", "accessories", "business hours", "opening hours",
    "support", "customer service", "store", "store policy",
    "cancel", "cancellation", "packaging", "replacement",
    "public holiday", "charge", "charges", "order confirmation",
}

# These phrases often signal an unrelated request.
OUT_OF_SCOPE_PATTERNS = [
    r"\bwrite (me )?(a |an )?(poem|song|essay|story)\b",
    r"\bsolve (this |my )?(math|maths|equation|homework)\b",
    r"\bwhat is (the )?(capital|weather|time) of\b",
    r"\bwho (is|was) the president\b",
    r"\bcreate (a |an )?(game|website|malware)\b",
    r"\bdebug (my |this )?(python|javascript|java) code\b",
]


def is_in_scope(message: str) -> bool:
    """
    Return True when a message appears related to store support.

    This is a simple heuristic, not a security boundary or a semantic
    classifier. Unknown queries should be escalated or reviewed.
    """
    text = message.casefold().strip()

    if not text:
        return False

    # Reject obvious unrelated requests unless store context is present.
    if any(re.search(pattern, text) for pattern in OUT_OF_SCOPE_PATTERNS):
        if not any(term in text for term in SUPPORT_TERMS):
            return False

    return any(term in text for term in SUPPORT_TERMS)


def check_scope(message: str) -> tuple[bool, str | None]:
    """Return (allowed, fallback); fallback is provided if blocked."""
    if not is_in_scope(message):
        return False, FALLBACK_SENTENCE

    return True, None
