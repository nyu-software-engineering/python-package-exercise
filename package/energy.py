from .pet import check_count, check_pet, clamp

FREE_LINES = 50  # commits this size or smaller cost no energy
LINES_PER_POINT = 10  # every 10 lines over FREE_LINES costs 1 energy
MAX_DRAIN = 40  # most energy a single commit can take

POINTS_PER_PASS = 2
POINTS_PER_FAIL = 1


def drain_energy(pet, lines_changed):
    """Lower the pet's energy based on how big a commit was."""
    check_pet(pet, "energy")
    check_count(lines_changed, "lines_changed")

    extra_lines = max(lines_changed - FREE_LINES, 0)
    drain = min(extra_lines // LINES_PER_POINT, MAX_DRAIN)
    pet["energy"] = clamp(pet["energy"] - drain)
    return pet["energy"]


def restore_energy(pet, tests_passed, tests_failed=0):
    """Raise the pet's energy based on test results."""
    check_pet(pet, "energy")
    check_count(tests_passed, "tests_passed")
    check_count(tests_failed, "tests_failed")

    gain = tests_passed * POINTS_PER_PASS - tests_failed * POINTS_PER_FAIL
    pet["energy"] = clamp(pet["energy"] + max(gain, 0))
    return pet["energy"]