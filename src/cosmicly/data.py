"""
Store orbital periods, surface gravity, distances from the Sun, and solar
day lengths for the planets and Earth's Moon.
"""

PLANETS = {
    "mercury": {
        "orbital_period_days": 88.0,
        "gravity_m_s2": 3.7,
        "distance_from_sun_km": 57_900_000,
        "solar_day_hours": 4222.6,
    },
    "moon": {
        "orbital_period_days": 365.2,
        "gravity_m_s2": 1.6,
        "distance_from_sun_km": 149_600_000,
        "solar_day_hours": 708.7,
    },
    "venus": {
        "orbital_period_days": 224.7,
        "gravity_m_s2": 8.9,
        "distance_from_sun_km": 108_200_000,
        "solar_day_hours": 2802.0,
    },
    "earth": {
        "orbital_period_days": 365.2,
        "gravity_m_s2": 9.8,
        "distance_from_sun_km": 149_600_000,
        "solar_day_hours": 24.0,
    },
    "mars": {
        "orbital_period_days": 687.0,
        "gravity_m_s2": 3.7,
        "distance_from_sun_km": 228_000_000,
        "solar_day_hours": 24.65979,
    },
    "jupiter": {
        "orbital_period_days": 4_331,
        "gravity_m_s2": 23.1,
        "distance_from_sun_km": 778_500_000,
        "solar_day_hours": 9.9,
    },
    "saturn": {
        "orbital_period_days": 10_747,
        "gravity_m_s2": 9.0,
        "distance_from_sun_km": 1_432_000_000,
        "solar_day_hours": 10.7,
    },
    "uranus": {
        "orbital_period_days": 30_589,
        "gravity_m_s2": 8.7,
        "distance_from_sun_km": 2_867_000_000,
        "solar_day_hours": 17.2,
    },
    "neptune": {
        "orbital_period_days": 59_800,
        "gravity_m_s2": 11.0,
        "distance_from_sun_km": 4_515_000_000,
        "solar_day_hours": 16.1,
    },
}
