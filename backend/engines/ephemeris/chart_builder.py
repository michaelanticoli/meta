"""
Chart Builder - Calculates natal charts using Swiss Ephemeris.

This module provides the core functionality for calculating natal charts
from birth data (date, time, location). It uses the Swiss Ephemeris library
(pyswisseph) for accurate astronomical calculations.

TODO: Copy/integrate with quantumelodic-mvp/src/ephemeris_engine/
"""

from datetime import datetime
from typing import Optional

# Try to import optional dependencies
try:
    import swisseph as swe
    SWISSEPH_AVAILABLE = True
except ImportError:
    swe = None
    SWISSEPH_AVAILABLE = False

try:
    import pytz
    PYTZ_AVAILABLE = True
except ImportError:
    pytz = None
    PYTZ_AVAILABLE = False

from .models import NatalChart, PlanetPosition, HouseCusp, Aspect


# Planet codes for Swiss Ephemeris (only defined if available)
if SWISSEPH_AVAILABLE:
    PLANETS = {
        'Sun': swe.SUN,
        'Moon': swe.MOON,
        'Mercury': swe.MERCURY,
        'Venus': swe.VENUS,
        'Mars': swe.MARS,
        'Jupiter': swe.JUPITER,
        'Saturn': swe.SATURN,
        'Uranus': swe.URANUS,
        'Neptune': swe.NEPTUNE,
        'Pluto': swe.PLUTO,
        'North Node': swe.TRUE_NODE,
        'Chiron': swe.CHIRON
    }
else:
    # Placeholder when swisseph not available
    PLANETS = {
        'Sun': 0, 'Moon': 1, 'Mercury': 2, 'Venus': 3, 'Mars': 4,
        'Jupiter': 5, 'Saturn': 6, 'Uranus': 7, 'Neptune': 8, 'Pluto': 9,
        'North Node': 10, 'Chiron': 11
    }

# Zodiac signs
ZODIAC_SIGNS = [
    'Aries', 'Taurus', 'Gemini', 'Cancer',
    'Leo', 'Virgo', 'Libra', 'Scorpio',
    'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

# Elements by sign
ELEMENTS = {
    'Aries': 'Fire', 'Leo': 'Fire', 'Sagittarius': 'Fire',
    'Taurus': 'Earth', 'Virgo': 'Earth', 'Capricorn': 'Earth',
    'Gemini': 'Air', 'Libra': 'Air', 'Aquarius': 'Air',
    'Cancer': 'Water', 'Scorpio': 'Water', 'Pisces': 'Water'
}

# Modalities by sign
MODALITIES = {
    'Aries': 'Cardinal', 'Cancer': 'Cardinal', 'Libra': 'Cardinal', 'Capricorn': 'Cardinal',
    'Taurus': 'Fixed', 'Leo': 'Fixed', 'Scorpio': 'Fixed', 'Aquarius': 'Fixed',
    'Gemini': 'Mutable', 'Virgo': 'Mutable', 'Sagittarius': 'Mutable', 'Pisces': 'Mutable'
}

# Aspect definitions (angle, orb)
ASPECTS = {
    'conjunction': (0, 8),
    'opposition': (180, 8),
    'trine': (120, 8),
    'square': (90, 7),
    'sextile': (60, 6),
    'quincunx': (150, 3),
    'semisextile': (30, 2)
}


class ChartBuilder:
    """
    Builds natal charts from birth data using Swiss Ephemeris.

    Usage:
        builder = ChartBuilder()
        chart = builder.build_chart(
            date="1961-08-04",
            time="19:24:00",
            latitude=21.3099,
            longitude=-157.8581,
            timezone="Pacific/Honolulu"
        )
    """

    def __init__(self, ephemeris_path: Optional[str] = None):
        """
        Initialize the chart builder.

        Args:
            ephemeris_path: Path to Swiss Ephemeris data files.
                           If None, uses default location.

        Raises:
            ImportError: If pyswisseph is not installed.
        """
        if not SWISSEPH_AVAILABLE:
            raise ImportError(
                "pyswisseph is required for natal chart calculations. "
                "Install with: pip install pyswisseph"
            )
        if not PYTZ_AVAILABLE:
            raise ImportError(
                "pytz is required for timezone handling. "
                "Install with: pip install pytz"
            )
        if ephemeris_path:
            swe.set_ephe_path(ephemeris_path)

    def build_chart(
        self,
        date: str,
        time: str,
        latitude: float,
        longitude: float,
        timezone: str
    ) -> NatalChart:
        """
        Build a complete natal chart from birth data.

        Args:
            date: Birth date in YYYY-MM-DD format
            time: Birth time in HH:MM:SS format
            latitude: Birth location latitude (-90 to 90)
            longitude: Birth location longitude (-180 to 180)
            timezone: IANA timezone string (e.g., "America/New_York")

        Returns:
            NatalChart object with all calculated positions
        """
        # Parse and convert datetime to Julian Day
        julian_day = self._calculate_julian_day(date, time, timezone)

        # Calculate planetary positions
        planets = self._calculate_planets(julian_day)

        # Calculate house cusps (using Placidus)
        houses = self._calculate_houses(julian_day, latitude, longitude)

        # Assign planets to houses
        self._assign_planets_to_houses(planets, houses)

        # Calculate aspects
        aspects = self._calculate_aspects(planets)

        # Get key positions
        sun_sign = self._get_planet_sign(planets, 'Sun')
        moon_sign = self._get_planet_sign(planets, 'Moon')
        rising_sign = houses[0].zodiac_sign if houses else ''

        # Calculate dominants
        dominant_element = self._calculate_dominant_element(planets)
        dominant_modality = self._calculate_dominant_modality(planets)

        return NatalChart(
            birth_date=date,
            birth_time=time,
            latitude=latitude,
            longitude=longitude,
            timezone=timezone,
            planets=planets,
            houses=houses,
            aspects=aspects,
            sun_sign=sun_sign,
            moon_sign=moon_sign,
            rising_sign=rising_sign,
            dominant_element=dominant_element,
            dominant_modality=dominant_modality,
            julian_day=julian_day
        )

    def _calculate_julian_day(self, date: str, time: str, timezone: str) -> float:
        """Convert date/time/timezone to Julian Day number."""
        # Parse datetime
        dt_str = f"{date} {time}"
        local_dt = datetime.strptime(dt_str, "%Y-%m-%d %H:%M:%S")

        # Localize to timezone
        tz = pytz.timezone(timezone)
        local_dt = tz.localize(local_dt)

        # Convert to UTC
        utc_dt = local_dt.astimezone(pytz.UTC)

        # Calculate decimal hours
        decimal_hours = utc_dt.hour + utc_dt.minute / 60.0 + utc_dt.second / 3600.0

        # Calculate Julian Day
        julian_day = swe.julday(
            utc_dt.year,
            utc_dt.month,
            utc_dt.day,
            decimal_hours
        )

        return julian_day

    def _calculate_planets(self, julian_day: float) -> list:
        """Calculate positions for all planets."""
        planets = []

        for name, code in PLANETS.items():
            try:
                # Calculate position (flag 0 for default)
                result, _ = swe.calc_ut(julian_day, code)

                longitude = result[0]
                latitude = result[1]
                speed = result[3]

                # Determine zodiac sign and degree
                sign_index = int(longitude / 30)
                zodiac_sign = ZODIAC_SIGNS[sign_index]
                zodiac_degree = longitude % 30

                # Check if retrograde (negative speed)
                retrograde = speed < 0

                planets.append(PlanetPosition(
                    planet=name,
                    longitude=longitude,
                    latitude=latitude,
                    speed=speed,
                    zodiac_sign=zodiac_sign,
                    zodiac_degree=zodiac_degree,
                    retrograde=retrograde
                ))

            except Exception as e:
                print(f"Error calculating {name}: {e}")
                continue

        return planets

    def _calculate_houses(self, julian_day: float, latitude: float, longitude: float) -> list:
        """Calculate house cusps using Placidus system."""
        houses = []

        try:
            # Calculate houses (P = Placidus)
            cusps, ascmc = swe.houses(julian_day, latitude, longitude, b'P')

            for i, cusp_long in enumerate(cusps[1:13], start=1):
                sign_index = int(cusp_long / 30)
                zodiac_sign = ZODIAC_SIGNS[sign_index]
                zodiac_degree = cusp_long % 30

                houses.append(HouseCusp(
                    house=i,
                    longitude=cusp_long,
                    zodiac_sign=zodiac_sign,
                    zodiac_degree=zodiac_degree
                ))

        except Exception as e:
            print(f"Error calculating houses: {e}")

        return houses

    def _assign_planets_to_houses(self, planets: list, houses: list) -> None:
        """Assign each planet to its house based on longitude."""
        if not houses:
            return

        house_cusps = [h.longitude for h in houses]

        for planet in planets:
            # Find which house the planet is in
            for i in range(12):
                cusp_start = house_cusps[i]
                cusp_end = house_cusps[(i + 1) % 12]

                # Handle wrap-around at 360 degrees
                if cusp_start > cusp_end:
                    if planet.longitude >= cusp_start or planet.longitude < cusp_end:
                        planet.house = i + 1
                        break
                else:
                    if cusp_start <= planet.longitude < cusp_end:
                        planet.house = i + 1
                        break

    def _calculate_aspects(self, planets: list) -> list:
        """Calculate aspects between all planet pairs."""
        aspects = []

        for i, p1 in enumerate(planets):
            for p2 in planets[i + 1:]:
                # Calculate angle between planets
                angle = abs(p1.longitude - p2.longitude)
                if angle > 180:
                    angle = 360 - angle

                # Check each aspect type
                for aspect_name, (aspect_angle, max_orb) in ASPECTS.items():
                    orb = abs(angle - aspect_angle)

                    if orb <= max_orb:
                        # Determine if applying or separating
                        # (simplified - would need more calculation for accuracy)
                        applying = p1.speed > p2.speed

                        aspects.append(Aspect(
                            planet1=p1.planet,
                            planet2=p2.planet,
                            aspect_type=aspect_name,
                            angle=angle,
                            orb=orb,
                            applying=applying
                        ))
                        break

        return aspects

    def _get_planet_sign(self, planets: list, planet_name: str) -> str:
        """Get the zodiac sign of a specific planet."""
        for planet in planets:
            if planet.planet == planet_name:
                return planet.zodiac_sign
        return ''

    def _calculate_dominant_element(self, planets: list) -> str:
        """Calculate the dominant element based on planet placements."""
        element_counts = {'Fire': 0, 'Earth': 0, 'Air': 0, 'Water': 0}

        # Weight personal planets more heavily
        weights = {
            'Sun': 3, 'Moon': 3, 'Mercury': 2, 'Venus': 2, 'Mars': 2,
            'Jupiter': 1, 'Saturn': 1, 'Uranus': 1, 'Neptune': 1, 'Pluto': 1
        }

        for planet in planets:
            weight = weights.get(planet.planet, 1)
            element = ELEMENTS.get(planet.zodiac_sign, '')
            if element:
                element_counts[element] += weight

        return max(element_counts, key=element_counts.get)

    def _calculate_dominant_modality(self, planets: list) -> str:
        """Calculate the dominant modality based on planet placements."""
        modality_counts = {'Cardinal': 0, 'Fixed': 0, 'Mutable': 0}

        for planet in planets:
            modality = MODALITIES.get(planet.zodiac_sign, '')
            if modality:
                modality_counts[modality] += 1

        return max(modality_counts, key=modality_counts.get)
