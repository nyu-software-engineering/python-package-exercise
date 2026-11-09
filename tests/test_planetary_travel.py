"""Tests for the compare_planets module."""

import importlib
from datetime import date, datetime, timedelta

import pytest

from cosmicly.compare_planets import compare_planets, earth_age

# The module itself, so its teammate functions can be swapped for fakes.
COMPARE_MODULE = importlib.import_module("cosmicly.compare_planets")


def days_ago(days: int) -> date:
    """Return the date that was the given number of days before today."""
    return date.today() - timedelta(days=days)


def fake_age_on_planet(age, planet):
    """Stand-in for age_on_planet that just reports what it was given."""
    return (age, planet)


def fake_weight_on_planet(_type_, value, planet):
    """Stand-in for weight_on_planet that just reports what it was given."""
    return (_type_, value, planet)


def use_fakes(monkeypatch):
    """Replace the teammates' functions inside compare_planets with fakes."""
    monkeypatch.setattr(COMPARE_MODULE, "age_on_planet", fake_age_on_planet)
    monkeypatch.setattr(COMPARE_MODULE, "weight_on_planet", fake_weight_on_planet)


