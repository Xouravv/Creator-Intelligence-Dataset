import re

REVIEW_WORDS = {
    "review",
    "unboxing",
    "hands on",
    "hands-on",
    "first impressions",
    "comparison",
    "vs",
    "testing",
    "tested"
}

def normalize(text):
    text = text.lower()
    text = re.sub(r'[^a-z0-9 ]', ' ', text)
    return ' '.join(text.split())


def validate_video(title, product):

    title_norm = normalize(title)
    title_words = set(title_norm.split())

    product_words = normalize(product).split()

    matched_words = sum(
        1 for word in product_words
        if word in title_words
    )

    product_score = matched_words / len(product_words)

    review_found = any(
        keyword in title_norm
        for keyword in REVIEW_WORDS
    )

    confidence = product_score * 80

    if review_found:
        confidence += 20

    confidence = round(confidence, 2)

    is_match = (
        product_score == 1.0
        and review_found
    )

    return {
        "is_match": is_match,
        "confidence_score": confidence,
        "validation_logic":
            f"{matched_words}/{len(product_words)} product words matched; "
            f"review keyword found={review_found}",
        "assumptions":
            "Video title accurately describes the reviewed product"
    }