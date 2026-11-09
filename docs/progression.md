# XP and leveling

Each planned minute is worth 1 XP. Users start at level 1 with 0 XP.
Every 100 total XP increases the level by 1.

## Usage

```python
from progression import calculate_xp, calculate_level

reward = calculate_xp(60)  # 60 XP
level = calculate_level(160)  # Level 2
```

## Input rules

- Duration must be a positive integer.
- Total XP must be a nonnegative integer.
- Booleans, floats, strings, and None raise TypeError.
- Zero or negative durations raise ValueError.
- Negative total XP raises ValueError.

## Integration

Store the calculated reward as the quest's xpReward.
Persist totalXP and calculate the level from that total.

These functions only calculate values. The completion code must
save quest completion and award XP together, ensuring that completing
the same quest again does not award extra XP.

## Testing

From the repository root:

```sh
pipenv install --dev
pipenv run python -m pytest -q
```
