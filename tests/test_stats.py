
from ascend import stats


class Tests:
    def test_studying(self):
        card = stats.make_stat_card("studying", 7)

        assert isinstance(card, str)
        assert "Activity: studying" in card
        assert "Level: 7" in card
        assert "Focus:" in card
        assert "Studymaxxing:" in card
        assert "Exam Aura:" in card

    def test_gym(self):
        card = stats.make_stat_card("gym", 3)

        assert "Activity: gym" in card
        assert "Strength:" in card
        assert "Gymmaxxing:" in card
        assert "Physique Aura:" in card

    def test_other_activity(self):
        card = stats.make_stat_card("cooking", 5)

        assert "Activity: cooking" in card
        assert "Effort:" in card
        assert "Maxxing:" in card
        assert "Aura:" in card

    def test_score_ranges(self):
        for level in range(1, 11):
            for i in range(100):
                card = stats.make_stat_card("studying", level)
                lines = card.split("\n")

                minimum_score = (level - 1) * 10 + 1
                maximum_score = level * 10

                for line in lines[4:7]:
                    score = int(line.split(": ")[1])
                    assert minimum_score <= score
                    assert score <= maximum_score

    def test_invalid_activity(self):
        try:
            stats.make_stat_card("", 5)
            assert False, "Expected ValueError for empty activity"
        except ValueError:
            pass

        try:
            stats.make_stat_card(123, 5)
            assert False, "Expected TypeError for non-string activity"
        except TypeError:
            pass

    def test_invalid_level(self):
        for level in [0, 11]:
            try:
                stats.make_stat_card("studying", level)
                assert False, "Expected ValueError for invalid level"
            except ValueError:
                pass

        try:
            stats.make_stat_card("studying", "five")
            assert False, "Expected TypeError for non-integer level"
        except TypeError:
            pass
