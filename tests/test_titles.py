from ascend import titles


class Tests:
    def test_win_title(self):
        self.check_title("win", [
            "ascension confirmed",
            "brutal mog",
            "halo activated",
            "psl went up",
            "chadlite unlocked",
            "mog streak started",
        ])

    def test_loss_title(self):
        self.check_title("loss", [
            "its over",
            "pure cope",
            "never began",
            "got mogged",
            "brutal failo",
            "psl dropped",
        ])

    def test_grind_title(self):
        self.check_title("grind", [
            "ascension pending",
            "mogging in progress",
            "softmaxxing arc",
            "halo under construction",
            "psl gains pending",
            "mewing streak",
        ])

    def check_title(self, outcome, phrases):
        expected = []
        for phrase in phrases:
            expected.append(f"pov laundrymaxxing {phrase}")
            expected.append(f"laundrymaxxing update {phrase}")
            expected.append(f"{phrase} after laundrymaxxing")

        for _ in range(20):
            assert titles.make_title(" Laundry ", outcome) in expected

    def test_multiword_activity(self):
        assert "meal prepmaxxing" in titles.make_title("Meal Prep", "win")

    def test_blank_activity(self):
        assert titles.make_title("", "win") is None
        assert titles.make_title("   ", "win") is None

    def test_unsupported_outcome(self):
        assert titles.make_title("laundry", "unknown") is None
        assert titles.make_title("laundry", "WIN") is None

    def test_non_string_inputs(self):
        assert titles.make_title([], "win") is None
        assert titles.make_title("laundry", []) is None
