"""Generate fictional facts."""

import random


_FACT_TEMPLATES = (
    "According to {category} experts, {topic} secretly control the weather.",
    "A fictional {category} study found that {topic} can communicate with aliens.",
    "Researchers in {category} claim that {topic} invented the weekend.",
)


def generate_fact(topic: str, category: str) -> str:
    """Generate a fictional fact containing a topic and category.

    Args:
        topic: Nonempty text describing the subject.
        category: Nonempty text describing the category.

    Returns:
        A fictional fact with surrounding input whitespace removed.
        Internal whitespace and capitalization are preserved.

    Raises:
        TypeError: If either argument is not a string.
        ValueError: If either argument is empty after trimming.
    """
    if not isinstance(topic, str):
        raise TypeError("topic must be a string")

    if not isinstance(category, str):
        raise TypeError("category must be a string")

    topic = topic.strip()
    category = category.strip()

    if not topic:
        raise ValueError("topic must not be empty or whitespace-only")

    if not category:
        raise ValueError("category must not be empty or whitespace-only")

    template = random.choice(_FACT_TEMPLATES)

    return template.format(
        topic=topic,
        category=category,
    )