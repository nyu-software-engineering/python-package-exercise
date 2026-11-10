import pytest
# from your_package import your_module


class Tests:
    #
    # Fixtures
    #

    @pytest.fixture
    def example_fixture(self):
        """
        Setup and teardown shared by any test that uses this fixture.
        """
        # setup

        yield

        # teardown

    #
    # Test functions
    #

    def test_sanity_check(self, example_fixture):
        """
        A test that always passes, to check that pytest runs.
        Run all tests from the main project directory with `python3 -m pytest`.
        """
        expected = True
        actual = True
        assert actual == expected, "Expected True to be equal to True!"

    def test_example(self):
        """
        Describe what this test checks.
        """
        expected = None  # replace with the expected value
        actual = None  # replace with a call to the code under test
        assert actual == expected, f"Expected {expected}, got {actual}"