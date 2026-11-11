"""Update the pet's hygiene based on commits behind origin."""

from .history import record_event
from .pet import MAX_STAT, check_count, check_pet, clamp

HYGIENE_LOSS_PER_COMMIT_BEHIND = 10


def clean(pet):
    """Set hygiene to full and record a clean event."""
    check_pet(pet, "hygiene")
    before = pet["hygiene"]
    pet["hygiene"] = MAX_STAT
    record_event(pet, "clean", stat="hygiene", before=before, after=pet["hygiene"])
    return pet["hygiene"]


def update_hygiene(pet, commits_behind):
    """Lower hygiene as the number of commits behind origin increases."""
    check_pet(pet, "hygiene")
    check_count(commits_behind, "commits_behind")

    before = pet["hygiene"]
    pet["hygiene"] = clamp(
        MAX_STAT - commits_behind * HYGIENE_LOSS_PER_COMMIT_BEHIND
    )
    return pet["hygiene"]
