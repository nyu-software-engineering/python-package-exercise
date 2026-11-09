import random


_STATISTIC_TEMPLATES = (
    "{percentage}% of {topic} believe {category} is secretly controlled by pigeons.",
    "{percentage}% of {topic} use {category} to communicate with aliens.",
    "{percentage}% of {topic} are convinced {category} was invented by time-traveling hamsters.",
    "{percentage}% of {topic} claim {category} works better when nobody is watching.",
    "A highly questionable survey found that {percentage}% of {topic} think {category} is a government conspiracy.",
)


def generate_statistic(topic: str, category: str) -> str:
    """Generate an obviously fictional statistic about a topic and category."""
    if not isinstance(topic, str):
        raise TypeError("topic must be a string")
    if not topic.strip():
        raise ValueError("topic must not be empty or whitespace-only")
    if not isinstance(category, str):
        raise TypeError("category must be a string")
    if not category.strip():
        raise ValueError("category must not be empty or whitespace-only")

    template = random.choice(_STATISTIC_TEMPLATES)
    return template.format(
        percentage=random.randint(1, 99),
        topic=topic.strip(),
        category=category.strip(),
    )
