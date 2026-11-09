"""Update the pet's hygiene based on commits behind origin."""

from .pet import MAX_STAT, check_count, check_pet, clamp

HYGIENE_LOSS_PER_COMMIT_BEHIND = 10


def update_hygiene(pet, commits_behind):
    """Lower hygiene as the number of commits behind origin increases."""
    check_pet(pet, "hygiene")
    check_count(commits_behind, "commits_behind")

    pet["hygiene"] = clamp(
        MAX_STAT - commits_behind * HYGIENE_LOSS_PER_COMMIT_BEHIND
    )
    return pet["hygiene"]