"""Generate fictional facts."""

import random


_FACT_TEMPLATES = (
    "According to {category} experts, {topic} secretly control the weather.",
    "A fictional {category} study found that {topic} can communicate with aliens.",
    "Researchers in {category} claim that {topic} invented the weekend.",
)


def generate_fact(topic: str, category: str) -> str:
    """Generate a fictional fact containing a topic and category."""
    template = random.choice(_FACT_TEMPLATES)

    return template.format(
        topic=topic,
        category=category,
    )