"""
Data models for ephemeris calculations.
"""

from dataclasses import dataclass, field, asdict
from typing import List, Optional, Dict, Any


@dataclass
class PlanetPosition:
    """Represents a planetary position in a natal chart."""
    planet: str
    longitude: float  # 0-360 degrees
    latitude: float
    speed: float  # degrees per day
    zodiac_sign: str
    zodiac_degree: float  # 0-30 within sign
    retrograde: bool = False
    house: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HouseCusp:
    """Represents a house cusp position."""
    house: int  # 1-12
    longitude: float
    zodiac_sign: str
    zodiac_degree: float

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Aspect:
    """Represents an aspect between two planets."""
    planet1: str
    planet2: str
    aspect_type: str  # conjunction, opposition, trine, square, sextile
    angle: float  # exact angle
    orb: float  # deviation from exact
    applying: bool  # True if aspect is applying, False if separating

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class NatalChart:
    """Complete natal chart data."""
    # Birth data
    birth_date: str
    birth_time: str
    latitude: float
    longitude: float
    timezone: str

    # Calculated positions
    planets: List[PlanetPosition] = field(default_factory=list)
    houses: List[HouseCusp] = field(default_factory=list)
    aspects: List[Aspect] = field(default_factory=list)

    # Derived data
    sun_sign: str = ""
    moon_sign: str = ""
    rising_sign: str = ""
    dominant_element: str = ""
    dominant_modality: str = ""

    # Julian day for reference
    julian_day: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "birth_data": {
                "date": self.birth_date,
                "time": self.birth_time,
                "latitude": self.latitude,
                "longitude": self.longitude,
                "timezone": self.timezone
            },
            "planets": [p.to_dict() for p in self.planets],
            "houses": [h.to_dict() for h in self.houses],
            "aspects": [a.to_dict() for a in self.aspects],
            "summary": {
                "sun_sign": self.sun_sign,
                "moon_sign": self.moon_sign,
                "rising_sign": self.rising_sign,
                "dominant_element": self.dominant_element,
                "dominant_modality": self.dominant_modality
            },
            "julian_day": self.julian_day
        }
