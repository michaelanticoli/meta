"""
Ephemeris Engine - Natal Chart Builder

Uses Swiss Ephemeris (pyswisseph) to calculate planetary positions
for natal chart generation.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
import math

# Note: pyswisseph import will be available when dependencies are installed
# import swisseph as swe


@dataclass
class PlanetPosition:
    """Position of a celestial body."""
    name: str
    longitude: float
    latitude: float
    sign: str
    degree_in_sign: float
    retrograde: bool = False
    house: Optional[int] = None

    def to_dict(self) -> Dict:
        return {
            "name": self.name,
            "longitude": self.longitude,
            "latitude": self.latitude,
            "sign": self.sign,
            "degree_in_sign": self.degree_in_sign,
            "retrograde": self.retrograde,
            "house": self.house
        }


@dataclass
class Aspect:
    """Aspect between two celestial bodies."""
    planet1: str
    planet2: str
    aspect_type: str
    orb: float
    exact_degree: float

    def to_dict(self) -> Dict:
        return {
            "planet1": self.planet1,
            "planet2": self.planet2,
            "aspect_type": self.aspect_type,
            "orb": self.orb,
            "exact_degree": self.exact_degree
        }


@dataclass
class NatalChart:
    """Complete natal chart data."""
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone: str
    planets: List[PlanetPosition] = field(default_factory=list)
    houses: List[float] = field(default_factory=list)
    ascendant: float = 0.0
    midheaven: float = 0.0
    aspects: List[Aspect] = field(default_factory=list)
    sun_sign: str = ""
    moon_sign: str = ""
    rising_sign: str = ""

    def to_dict(self) -> Dict:
        return {
            "birth_data": {
                "date": self.birth_date,
                "time": self.birth_time,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "timezone": self.timezone
            },
            "planets": [p.to_dict() for p in self.planets],
            "houses": self.houses,
            "ascendant": self.ascendant,
            "midheaven": self.midheaven,
            "aspects": [a.to_dict() for a in self.aspects],
            "sun_sign": self.sun_sign,
            "moon_sign": self.moon_sign,
            "rising_sign": self.rising_sign
        }


class ChartBuilder:
    """
    Builds natal charts using Swiss Ephemeris calculations.

    This engine calculates:
    - Planetary positions (Sun through Pluto + lunar nodes)
    - House cusps (Placidus system by default)
    - Aspects between planets
    - Sign placements
    """

    ZODIAC_SIGNS = [
        "Aries", "Taurus", "Gemini", "Cancer",
        "Leo", "Virgo", "Libra", "Scorpio",
        "Sagittarius", "Capricorn", "Aquarius", "Pisces"
    ]

    PLANETS = [
        ("Sun", 0),
        ("Moon", 1),
        ("Mercury", 2),
        ("Venus", 3),
        ("Mars", 4),
        ("Jupiter", 5),
        ("Saturn", 6),
        ("Uranus", 7),
        ("Neptune", 8),
        ("Pluto", 9),
        ("North Node", 10),
        ("Chiron", 15)
    ]

    ASPECTS = {
        "conjunction": (0, 8),
        "sextile": (60, 6),
        "square": (90, 8),
        "trine": (120, 8),
        "opposition": (180, 8)
    }

    def __init__(self, ephemeris_path: Optional[str] = None):
        """Initialize the chart builder."""
        self.ephemeris_path = ephemeris_path
        # swe.set_ephe_path(ephemeris_path) when swisseph is available

    def build_chart(
        self,
        date: str,
        time: str,
        latitude: float,
        longitude: float,
        timezone: str
    ) -> NatalChart:
        """
        Build a complete natal chart.

        Args:
            date: Birth date in YYYY-MM-DD format
            time: Birth time in HH:MM:SS format
            latitude: Geographic latitude
            longitude: Geographic longitude
            timezone: IANA timezone string (e.g., 'America/New_York')

        Returns:
            NatalChart object with all calculated data
        """
        chart = NatalChart(
            birth_date=date,
            birth_time=time,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone
        )

        # Calculate Julian Day
        julian_day = self._calculate_julian_day(date, time, timezone)

        # Calculate planetary positions
        chart.planets = self._calculate_planets(julian_day)

        # Calculate houses
        houses_data = self._calculate_houses(julian_day, latitude, longitude)
        chart.houses = houses_data['cusps']
        chart.ascendant = houses_data['ascendant']
        chart.midheaven = houses_data['midheaven']

        # Assign planets to houses
        for planet in chart.planets:
            planet.house = self._get_house(planet.longitude, chart.houses)

        # Calculate aspects
        chart.aspects = self._calculate_aspects(chart.planets)

        # Set main sign placements
        for planet in chart.planets:
            if planet.name == "Sun":
                chart.sun_sign = planet.sign
            elif planet.name == "Moon":
                chart.moon_sign = planet.sign

        chart.rising_sign = self._longitude_to_sign(chart.ascendant)

        return chart

    def _calculate_julian_day(self, date: str, time: str, timezone: str) -> float:
        """Convert date/time to Julian Day."""
        # Parse date and time
        dt = datetime.fromisoformat(f"{date}T{time}")

        # Simplified JD calculation (proper implementation uses pytz + swisseph)
        year = dt.year
        month = dt.month
        day = dt.day + dt.hour / 24 + dt.minute / 1440 + dt.second / 86400

        if month <= 2:
            year -= 1
            month += 12

        a = int(year / 100)
        b = 2 - a + int(a / 4)

        jd = int(365.25 * (year + 4716)) + int(30.6001 * (month + 1)) + day + b - 1524.5

        return jd

    def _calculate_planets(self, julian_day: float) -> List[PlanetPosition]:
        """Calculate positions for all planets."""
        planets = []

        # Placeholder calculations - real implementation uses swisseph
        # For demo, using approximate positions
        base_positions = {
            "Sun": 132.5,      # Leo
            "Moon": 45.3,      # Taurus
            "Mercury": 140.2,  # Leo
            "Venus": 98.7,     # Cancer
            "Mars": 210.4,     # Scorpio
            "Jupiter": 285.6,  # Capricorn
            "Saturn": 320.1,   # Aquarius
            "Uranus": 45.8,    # Taurus
            "Neptune": 353.2,  # Pisces
            "Pluto": 298.5,    # Capricorn
            "North Node": 65.3,  # Gemini
            "Chiron": 12.4     # Aries
        }

        for name, _ in self.PLANETS:
            longitude = base_positions.get(name, 0)
            sign = self._longitude_to_sign(longitude)
            degree_in_sign = longitude % 30

            planet = PlanetPosition(
                name=name,
                longitude=longitude,
                latitude=0.0,
                sign=sign,
                degree_in_sign=degree_in_sign,
                retrograde=False
            )
            planets.append(planet)

        return planets

    def _calculate_houses(
        self,
        julian_day: float,
        latitude: float,
        longitude: float
    ) -> Dict:
        """Calculate house cusps using Placidus system."""
        # Placeholder - real implementation uses swe.houses()
        ascendant = 135.0  # Leo rising for demo
        midheaven = 45.0   # Taurus MC

        # Generate 12 house cusps (30 degrees apart from ascendant)
        cusps = []
        for i in range(12):
            cusp = (ascendant + i * 30) % 360
            cusps.append(cusp)

        return {
            "cusps": cusps,
            "ascendant": ascendant,
            "midheaven": midheaven
        }

    def _calculate_aspects(self, planets: List[PlanetPosition]) -> List[Aspect]:
        """Calculate aspects between planets."""
        aspects = []

        for i, planet1 in enumerate(planets):
            for planet2 in planets[i + 1:]:
                for aspect_name, (exact_angle, orb) in self.ASPECTS.items():
                    diff = abs(planet1.longitude - planet2.longitude)
                    if diff > 180:
                        diff = 360 - diff

                    aspect_orb = abs(diff - exact_angle)
                    if aspect_orb <= orb:
                        aspect = Aspect(
                            planet1=planet1.name,
                            planet2=planet2.name,
                            aspect_type=aspect_name,
                            orb=round(aspect_orb, 2),
                            exact_degree=exact_angle
                        )
                        aspects.append(aspect)

        return aspects

    def _longitude_to_sign(self, longitude: float) -> str:
        """Convert ecliptic longitude to zodiac sign."""
        sign_index = int(longitude / 30) % 12
        return self.ZODIAC_SIGNS[sign_index]

    def _get_house(self, longitude: float, house_cusps: List[float]) -> int:
        """Determine which house a planet is in."""
        for i in range(12):
            next_i = (i + 1) % 12
            cusp1 = house_cusps[i]
            cusp2 = house_cusps[next_i]

            if cusp2 < cusp1:  # Crosses 0°
                if longitude >= cusp1 or longitude < cusp2:
                    return i + 1
            else:
                if cusp1 <= longitude < cusp2:
                    return i + 1

        return 1  # Default to first house
