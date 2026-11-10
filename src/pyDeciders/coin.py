"""Coin flipping for the indecisive."""

import random

HEADS = "heads"
TAILS = "tails"

def flip_coin(times=1, bias=0.5, seed=None):
    """Flipping a coin one or more times.

    Args:
        times: how many flips to make. Must be a whole number of at least 1.
        bias: chance of landing heads, from 0.0 (always tails) to 1.0 (always heads).
            The default of 0.5 is a fair coin.
        seed: optional number that makes the result repeatable. The same seed
            always gives the same flips.

    Returns:
        A list of "heads" / "tails" strings, one per flip.

    Raises:
        TypeError: if times is not an int, or bias is not a number.
        ValueError: if times is less than 1, or bias is outside 0.0-1.0.
    """
    if isinstance(times, bool) or not isinstance(times, int):
        raise TypeError("times must be a whole number")
    if times < 1:
        raise ValueError("times must be at least 1")
    # checks for bool too as True == 1;
    if isinstance(bias, bool) or not isinstance(bias, (int, float)):
        raise TypeError("bias must be a number between 0 and 1")
    if not 0 <= bias <= 1:
        raise ValueError("bias must be between 0 and 1")

    # a private random generator, so seeding here never affects other code
    rng = random.Random(seed)

    results = []
    for _ in range(times):
        if rng.random() < bias:
            results.append(HEADS)
        else:
            results.append(TAILS)
    return results