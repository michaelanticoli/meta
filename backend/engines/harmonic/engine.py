"""
Harmonic Engine - 24-Mode Musical System

Maps astrological chart data to musical modes using the Quantumelodic
24-mode system (12 pentatonic + 12 quadratonic modes).
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class HarmonicResult:
    """Result of harmonic analysis."""
    # Primary musical mode
    primary_pentatonic_mode: str
    primary_quadratonic_mode: str

    # Mode details
    mode_name: str
    archetype: str
    emotional_color: str
    sonic_role: str
    waveform: str
    timbre: str
    semitone_pattern: str

    # Musical parameters
    key_signature: str
    tempo_bpm: int
    harmonic_tension_index: int

    # Elemental analysis
    dominant_element: str
    element_balance: Dict[str, float]

    # Additional data
    scale_degrees: List[int]
    chord_progression: List[str]


class HarmonicEngine:
    """
    Maps natal chart data to musical parameters using the 24-mode system.

    The system consists of:
    - 12 Pentatonic Modes (one per zodiac sign) - Personality expression
    - 12 Quadratonic Modes (one per zodiac sign) - Behavioral patterns
    """

    # Pentatonic modes mapped to zodiac signs
    PENTATONIC_MODES = {
        "Aries": {
            "mode_id": "P01",
            "mode_name": "Aries Pentatonic",
            "semitone_pattern": "2-2-3-2-3",
            "archetype": "The Pioneer",
            "emotional_color": "Bold Red Fire",
            "sonic_role": "Initiator",
            "waveform": "Sawtooth",
            "timbre": "Bright, aggressive attack"
        },
        "Taurus": {
            "mode_id": "P02",
            "mode_name": "Taurus Pentatonic",
            "semitone_pattern": "2-3-2-2-3",
            "archetype": "The Builder",
            "emotional_color": "Earthy Green",
            "sonic_role": "Foundation",
            "waveform": "Sine",
            "timbre": "Warm, sustained resonance"
        },
        "Gemini": {
            "mode_id": "P03",
            "mode_name": "Gemini Pentatonic",
            "semitone_pattern": "3-2-2-3-2",
            "archetype": "The Messenger",
            "emotional_color": "Quick Silver",
            "sonic_role": "Connector",
            "waveform": "Triangle",
            "timbre": "Light, dancing quality"
        },
        "Cancer": {
            "mode_id": "P04",
            "mode_name": "Cancer Pentatonic",
            "semitone_pattern": "2-3-2-3-2",
            "archetype": "The Nurturer",
            "emotional_color": "Lunar Silver",
            "sonic_role": "Protector",
            "waveform": "Sine",
            "timbre": "Soft, enveloping warmth"
        },
        "Leo": {
            "mode_id": "P05",
            "mode_name": "Leo Pentatonic",
            "semitone_pattern": "2-2-3-3-2",
            "archetype": "The Sovereign",
            "emotional_color": "Golden Radiance",
            "sonic_role": "Center Stage",
            "waveform": "Sawtooth",
            "timbre": "Rich, commanding presence"
        },
        "Virgo": {
            "mode_id": "P06",
            "mode_name": "Virgo Pentatonic",
            "semitone_pattern": "3-2-2-2-3",
            "archetype": "The Analyst",
            "emotional_color": "Forest Green",
            "sonic_role": "Refiner",
            "waveform": "Triangle",
            "timbre": "Pure, precise articulation"
        },
        "Libra": {
            "mode_id": "P07",
            "mode_name": "Libra Pentatonic",
            "semitone_pattern": "2-3-3-2-2",
            "archetype": "The Harmonizer",
            "emotional_color": "Rose Pink",
            "sonic_role": "Balancer",
            "waveform": "Sine",
            "timbre": "Balanced, pleasing harmonics"
        },
        "Scorpio": {
            "mode_id": "P08",
            "mode_name": "Scorpio Pentatonic",
            "semitone_pattern": "3-3-2-2-2",
            "archetype": "The Transformer",
            "emotional_color": "Deep Crimson",
            "sonic_role": "Depth Seeker",
            "waveform": "Square",
            "timbre": "Dark, intense resonance"
        },
        "Sagittarius": {
            "mode_id": "P09",
            "mode_name": "Sagittarius Pentatonic",
            "semitone_pattern": "2-2-2-3-3",
            "archetype": "The Explorer",
            "emotional_color": "Purple Horizon",
            "sonic_role": "Expander",
            "waveform": "Sawtooth",
            "timbre": "Expansive, soaring quality"
        },
        "Capricorn": {
            "mode_id": "P10",
            "mode_name": "Capricorn Pentatonic",
            "semitone_pattern": "3-2-3-2-2",
            "archetype": "The Architect",
            "emotional_color": "Mountain Gray",
            "sonic_role": "Structure",
            "waveform": "Square",
            "timbre": "Solid, grounded bass"
        },
        "Aquarius": {
            "mode_id": "P11",
            "mode_name": "Aquarius Pentatonic",
            "semitone_pattern": "2-3-2-2-3",
            "archetype": "The Innovator",
            "emotional_color": "Electric Blue",
            "sonic_role": "Disruptor",
            "waveform": "Noise/FM",
            "timbre": "Unusual, synthetic texture"
        },
        "Pisces": {
            "mode_id": "P12",
            "mode_name": "Pisces Pentatonic",
            "semitone_pattern": "3-2-2-3-2",
            "archetype": "The Dreamer",
            "emotional_color": "Ocean Mist",
            "sonic_role": "Dissolver",
            "waveform": "Sine",
            "timbre": "Ethereal, reverberant"
        }
    }

    # Quadratonic modes for behavioral patterns
    QUADRATONIC_MODES = {
        "Aries": {"mode_id": "Q01", "pattern": "3-2-4-3", "behavioral": "Action-oriented"},
        "Taurus": {"mode_id": "Q02", "pattern": "2-4-3-3", "behavioral": "Stability-seeking"},
        "Gemini": {"mode_id": "Q03", "pattern": "4-3-2-3", "behavioral": "Information-gathering"},
        "Cancer": {"mode_id": "Q04", "pattern": "3-3-4-2", "behavioral": "Protection-focused"},
        "Leo": {"mode_id": "Q05", "pattern": "2-3-3-4", "behavioral": "Expression-driven"},
        "Virgo": {"mode_id": "Q06", "pattern": "4-2-3-3", "behavioral": "Analysis-oriented"},
        "Libra": {"mode_id": "Q07", "pattern": "3-4-2-3", "behavioral": "Harmony-seeking"},
        "Scorpio": {"mode_id": "Q08", "pattern": "3-3-2-4", "behavioral": "Transformation-focused"},
        "Sagittarius": {"mode_id": "Q09", "pattern": "2-3-4-3", "behavioral": "Expansion-driven"},
        "Capricorn": {"mode_id": "Q10", "pattern": "4-3-3-2", "behavioral": "Achievement-oriented"},
        "Aquarius": {"mode_id": "Q11", "pattern": "3-2-3-4", "behavioral": "Innovation-focused"},
        "Pisces": {"mode_id": "Q12", "pattern": "3-4-3-2", "behavioral": "Dissolution-seeking"}
    }

    # Element to musical mapping
    ELEMENT_MAPPING = {
        "Fire": {"waveform": "sawtooth", "tempo_range": (100, 140), "brightness": 0.8},
        "Earth": {"waveform": "sine", "tempo_range": (60, 90), "brightness": 0.4},
        "Air": {"waveform": "triangle", "tempo_range": (90, 120), "brightness": 0.6},
        "Water": {"waveform": "sine", "tempo_range": (50, 80), "brightness": 0.3}
    }

    SIGN_ELEMENTS = {
        "Aries": "Fire", "Leo": "Fire", "Sagittarius": "Fire",
        "Taurus": "Earth", "Virgo": "Earth", "Capricorn": "Earth",
        "Gemini": "Air", "Libra": "Air", "Aquarius": "Air",
        "Cancer": "Water", "Scorpio": "Water", "Pisces": "Water"
    }

    KEY_SIGNATURES = {
        "Aries": "C major", "Taurus": "G major", "Gemini": "D major",
        "Cancer": "F major", "Leo": "A major", "Virgo": "E major",
        "Libra": "Bb major", "Scorpio": "E minor", "Sagittarius": "B major",
        "Capricorn": "A minor", "Aquarius": "F# major", "Pisces": "D minor"
    }

    def __init__(self):
        """Initialize the harmonic engine."""
        pass

    def analyze(self, chart_data: Dict) -> HarmonicResult:
        """
        Analyze natal chart data and return musical mapping.

        Args:
            chart_data: Dictionary containing natal chart information

        Returns:
            HarmonicResult with all musical parameters
        """
        # Get sun sign for primary mode
        sun_sign = chart_data.get('sun_sign', 'Leo')
        moon_sign = chart_data.get('moon_sign', 'Taurus')

        # Get pentatonic mode from sun sign
        penta_mode = self.PENTATONIC_MODES.get(sun_sign, self.PENTATONIC_MODES['Leo'])
        quad_mode = self.QUADRATONIC_MODES.get(moon_sign, self.QUADRATONIC_MODES['Taurus'])

        # Calculate element balance
        element_balance = self._calculate_element_balance(chart_data)
        dominant_element = max(element_balance, key=element_balance.get)

        # Calculate tension index from aspects
        tension_index = self._calculate_tension_index(chart_data)

        # Determine tempo based on dominant element
        element_data = self.ELEMENT_MAPPING.get(dominant_element, self.ELEMENT_MAPPING['Fire'])
        tempo_range = element_data['tempo_range']
        base_tempo = (tempo_range[0] + tempo_range[1]) // 2
        tempo_bpm = base_tempo + int((tension_index / 100) * 20)

        # Get key signature
        key_signature = self.KEY_SIGNATURES.get(sun_sign, 'C major')

        # Calculate scale degrees from semitone pattern
        scale_degrees = self._pattern_to_degrees(penta_mode['semitone_pattern'])

        # Generate chord progression
        chord_progression = self._generate_chord_progression(sun_sign, tension_index)

        return HarmonicResult(
            primary_pentatonic_mode=penta_mode['mode_id'],
            primary_quadratonic_mode=quad_mode['mode_id'],
            mode_name=penta_mode['mode_name'],
            archetype=penta_mode['archetype'],
            emotional_color=penta_mode['emotional_color'],
            sonic_role=penta_mode['sonic_role'],
            waveform=penta_mode['waveform'],
            timbre=penta_mode['timbre'],
            semitone_pattern=penta_mode['semitone_pattern'],
            key_signature=key_signature,
            tempo_bpm=tempo_bpm,
            harmonic_tension_index=tension_index,
            dominant_element=dominant_element,
            element_balance=element_balance,
            scale_degrees=scale_degrees,
            chord_progression=chord_progression
        )

    def _calculate_element_balance(self, chart_data: Dict) -> Dict[str, float]:
        """Calculate the balance of elements in the chart."""
        elements = {"Fire": 0, "Earth": 0, "Air": 0, "Water": 0}

        planets = chart_data.get('planets', [])
        for planet in planets:
            sign = planet.get('sign', '')
            element = self.SIGN_ELEMENTS.get(sign)
            if element:
                # Weight by planet importance
                weight = 1.0
                if planet.get('name') == 'Sun':
                    weight = 2.0
                elif planet.get('name') == 'Moon':
                    weight = 1.5
                elements[element] += weight

        # Normalize
        total = sum(elements.values())
        if total > 0:
            elements = {k: v / total for k, v in elements.items()}

        return elements

    def _calculate_tension_index(self, chart_data: Dict) -> int:
        """Calculate harmonic tension from aspects."""
        aspects = chart_data.get('aspects', [])
        tension = 50  # Base tension

        for aspect in aspects:
            aspect_type = aspect.get('aspect_type', '')
            if aspect_type == 'square':
                tension += 5
            elif aspect_type == 'opposition':
                tension += 3
            elif aspect_type == 'conjunction':
                tension += 2
            elif aspect_type == 'trine':
                tension -= 3
            elif aspect_type == 'sextile':
                tension -= 2

        return max(0, min(100, tension))

    def _pattern_to_degrees(self, pattern: str) -> List[int]:
        """Convert semitone pattern to scale degrees."""
        intervals = [int(x) for x in pattern.split('-')]
        degrees = [0]
        current = 0
        for interval in intervals[:-1]:
            current += interval
            degrees.append(current)
        return degrees

    def _generate_chord_progression(self, sun_sign: str, tension: int) -> List[str]:
        """Generate a chord progression based on chart data."""
        # Simple progressions based on tension level
        if tension < 30:
            return ["I", "IV", "V", "I"]
        elif tension < 60:
            return ["I", "vi", "IV", "V"]
        elif tension < 80:
            return ["I", "V", "vi", "IV"]
        else:
            return ["i", "VI", "III", "VII"]
