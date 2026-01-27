"""
Harmonic Engine - 24-Mode Pentatonic/Quadratonic Analysis System

This engine transforms natal chart data into musical parameters using
the Quantumelodic 24-mode system:
- 12 Pentatonic modes (one per zodiac sign) - melodic/harmonic dimension
- 12 Quadratonic modes (modality x element) - behavioral/rhythmic dimension

TODO: Integrate with quantumelodic-mvp/src/harmonic_engine/
"""

import os
import csv
from typing import Dict, Any, Optional
from pathlib import Path

from .models import HarmonicResult, PentatonicMode, QuadratonicMode


# Default pentatonic modes (zodiac-based)
DEFAULT_PENTATONIC_MODES = {
    'Aries': PentatonicMode(
        mode_id='P1_ARIES', mode_name='Aries Pentatonic', zodiac_sign='Aries',
        semitone_pattern='0-2-4-7-9', archetype='The Pioneer',
        emotional_color='Bold, Initiating, Courageous',
        sonic_role='Rhythmic Driver', waveform='sawtooth', timbre='brass', element='Fire'
    ),
    'Taurus': PentatonicMode(
        mode_id='P2_TAURUS', mode_name='Taurus Pentatonic', zodiac_sign='Taurus',
        semitone_pattern='0-2-5-7-9', archetype='The Builder',
        emotional_color='Grounded, Sensual, Steady',
        sonic_role='Harmonic Foundation', waveform='triangle', timbre='strings', element='Earth'
    ),
    'Gemini': PentatonicMode(
        mode_id='P3_GEMINI', mode_name='Gemini Pentatonic', zodiac_sign='Gemini',
        semitone_pattern='0-2-4-7-11', archetype='The Messenger',
        emotional_color='Curious, Adaptive, Communicative',
        sonic_role='Melodic Weaver', waveform='square', timbre='wind', element='Air'
    ),
    'Cancer': PentatonicMode(
        mode_id='P4_CANCER', mode_name='Cancer Pentatonic', zodiac_sign='Cancer',
        semitone_pattern='0-3-5-7-10', archetype='The Nurturer',
        emotional_color='Protective, Intuitive, Emotional',
        sonic_role='Emotional Core', waveform='sine', timbre='piano', element='Water'
    ),
    'Leo': PentatonicMode(
        mode_id='P5_LEO', mode_name='Leo Pentatonic', zodiac_sign='Leo',
        semitone_pattern='0-2-4-7-9', archetype='The Sovereign',
        emotional_color='Creative, Expressive, Regal',
        sonic_role='Melodic Leader', waveform='sawtooth', timbre='brass', element='Fire'
    ),
    'Virgo': PentatonicMode(
        mode_id='P6_VIRGO', mode_name='Virgo Pentatonic', zodiac_sign='Virgo',
        semitone_pattern='0-2-5-7-10', archetype='The Analyst',
        emotional_color='Precise, Practical, Healing',
        sonic_role='Harmonic Precision', waveform='triangle', timbre='harp', element='Earth'
    ),
    'Libra': PentatonicMode(
        mode_id='P7_LIBRA', mode_name='Libra Pentatonic', zodiac_sign='Libra',
        semitone_pattern='0-2-4-7-9', archetype='The Harmonizer',
        emotional_color='Balanced, Diplomatic, Aesthetic',
        sonic_role='Harmonic Balance', waveform='sine', timbre='strings', element='Air'
    ),
    'Scorpio': PentatonicMode(
        mode_id='P8_SCORPIO', mode_name='Scorpio Pentatonic', zodiac_sign='Scorpio',
        semitone_pattern='0-1-5-7-8', archetype='The Transformer',
        emotional_color='Intense, Transformative, Deep',
        sonic_role='Tension Builder', waveform='sawtooth', timbre='synth', element='Water'
    ),
    'Sagittarius': PentatonicMode(
        mode_id='P9_SAGITTARIUS', mode_name='Sagittarius Pentatonic', zodiac_sign='Sagittarius',
        semitone_pattern='0-2-4-7-11', archetype='The Explorer',
        emotional_color='Expansive, Optimistic, Philosophical',
        sonic_role='Melodic Expansor', waveform='triangle', timbre='brass', element='Fire'
    ),
    'Capricorn': PentatonicMode(
        mode_id='P10_CAPRICORN', mode_name='Capricorn Pentatonic', zodiac_sign='Capricorn',
        semitone_pattern='0-2-5-7-9', archetype='The Architect',
        emotional_color='Disciplined, Ambitious, Structured',
        sonic_role='Structural Foundation', waveform='square', timbre='organ', element='Earth'
    ),
    'Aquarius': PentatonicMode(
        mode_id='P11_AQUARIUS', mode_name='Aquarius Pentatonic', zodiac_sign='Aquarius',
        semitone_pattern='0-2-4-8-10', archetype='The Visionary',
        emotional_color='Innovative, Humanitarian, Eccentric',
        sonic_role='Harmonic Innovator', waveform='square', timbre='synth', element='Air'
    ),
    'Pisces': PentatonicMode(
        mode_id='P12_PISCES', mode_name='Pisces Pentatonic', zodiac_sign='Pisces',
        semitone_pattern='0-3-5-8-10', archetype='The Dreamer',
        emotional_color='Mystical, Compassionate, Transcendent',
        sonic_role='Ethereal Ambiance', waveform='sine', timbre='pad', element='Water'
    )
}

# Default quadratonic modes (modality x element)
DEFAULT_QUADRATONIC_MODES = {
    ('Cardinal', 'Fire'): QuadratonicMode(
        mode_id='Q1_CARDINAL_FIRE', mode_name='Cardinal Fire', archetype='The Initiator',
        modality='Cardinal', element='Fire', semitone_pattern='0-4-7-11',
        rhythmic_emphasis='downbeat', dynamic_character='explosive'
    ),
    ('Cardinal', 'Earth'): QuadratonicMode(
        mode_id='Q2_CARDINAL_EARTH', mode_name='Cardinal Earth', archetype='The Achiever',
        modality='Cardinal', element='Earth', semitone_pattern='0-3-7-10',
        rhythmic_emphasis='steady', dynamic_character='determined'
    ),
    ('Cardinal', 'Air'): QuadratonicMode(
        mode_id='Q3_CARDINAL_AIR', mode_name='Cardinal Air', archetype='The Negotiator',
        modality='Cardinal', element='Air', semitone_pattern='0-4-7-9',
        rhythmic_emphasis='syncopated', dynamic_character='balanced'
    ),
    ('Cardinal', 'Water'): QuadratonicMode(
        mode_id='Q4_CARDINAL_WATER', mode_name='Cardinal Water', archetype='The Protector',
        modality='Cardinal', element='Water', semitone_pattern='0-3-5-10',
        rhythmic_emphasis='flowing', dynamic_character='nurturing'
    ),
    ('Fixed', 'Fire'): QuadratonicMode(
        mode_id='Q5_FIXED_FIRE', mode_name='Fixed Fire', archetype='The Performer',
        modality='Fixed', element='Fire', semitone_pattern='0-4-7-11',
        rhythmic_emphasis='strong', dynamic_character='dramatic'
    ),
    ('Fixed', 'Earth'): QuadratonicMode(
        mode_id='Q6_FIXED_EARTH', mode_name='Fixed Earth', archetype='The Sustainer',
        modality='Fixed', element='Earth', semitone_pattern='0-3-7-9',
        rhythmic_emphasis='grounded', dynamic_character='persistent'
    ),
    ('Fixed', 'Air'): QuadratonicMode(
        mode_id='Q7_FIXED_AIR', mode_name='Fixed Air', archetype='The Rebel',
        modality='Fixed', element='Air', semitone_pattern='0-4-8-10',
        rhythmic_emphasis='irregular', dynamic_character='electric'
    ),
    ('Fixed', 'Water'): QuadratonicMode(
        mode_id='Q8_FIXED_WATER', mode_name='Fixed Water', archetype='The Alchemist',
        modality='Fixed', element='Water', semitone_pattern='0-1-5-8',
        rhythmic_emphasis='intense', dynamic_character='transformative'
    ),
    ('Mutable', 'Fire'): QuadratonicMode(
        mode_id='Q9_MUTABLE_FIRE', mode_name='Mutable Fire', archetype='The Adventurer',
        modality='Mutable', element='Fire', semitone_pattern='0-4-7-11',
        rhythmic_emphasis='free', dynamic_character='expansive'
    ),
    ('Mutable', 'Earth'): QuadratonicMode(
        mode_id='Q10_MUTABLE_EARTH', mode_name='Mutable Earth', archetype='The Healer',
        modality='Mutable', element='Earth', semitone_pattern='0-2-5-10',
        rhythmic_emphasis='precise', dynamic_character='analytical'
    ),
    ('Mutable', 'Air'): QuadratonicMode(
        mode_id='Q11_MUTABLE_AIR', mode_name='Mutable Air', archetype='The Communicator',
        modality='Mutable', element='Air', semitone_pattern='0-2-4-11',
        rhythmic_emphasis='quick', dynamic_character='mercurial'
    ),
    ('Mutable', 'Water'): QuadratonicMode(
        mode_id='Q12_MUTABLE_WATER', mode_name='Mutable Water', archetype='The Mystic',
        modality='Mutable', element='Water', semitone_pattern='0-3-5-10',
        rhythmic_emphasis='fluid', dynamic_character='dreamy'
    )
}

# Sign to modality mapping
SIGN_MODALITY = {
    'Aries': 'Cardinal', 'Cancer': 'Cardinal', 'Libra': 'Cardinal', 'Capricorn': 'Cardinal',
    'Taurus': 'Fixed', 'Leo': 'Fixed', 'Scorpio': 'Fixed', 'Aquarius': 'Fixed',
    'Gemini': 'Mutable', 'Virgo': 'Mutable', 'Sagittarius': 'Mutable', 'Pisces': 'Mutable'
}

# Sign to element mapping
SIGN_ELEMENT = {
    'Aries': 'Fire', 'Leo': 'Fire', 'Sagittarius': 'Fire',
    'Taurus': 'Earth', 'Virgo': 'Earth', 'Capricorn': 'Earth',
    'Gemini': 'Air', 'Libra': 'Air', 'Aquarius': 'Air',
    'Cancer': 'Water', 'Scorpio': 'Water', 'Pisces': 'Water'
}

# Element to dynamics mapping
ELEMENT_DYNAMICS = {
    'Fire': 'f',    # forte
    'Earth': 'mf',  # mezzo-forte
    'Air': 'mp',    # mezzo-piano
    'Water': 'p'    # piano
}

# Key signatures by element
ELEMENT_KEYS = {
    'Fire': ['C major', 'G major', 'D major'],
    'Earth': ['F major', 'Bb major', 'Eb major'],
    'Air': ['A major', 'E major', 'B major'],
    'Water': ['A minor', 'D minor', 'E minor']
}

# Tempo ranges by modality
MODALITY_TEMPO = {
    'Cardinal': (120, 140),  # Energetic, initiating
    'Fixed': (80, 100),      # Steady, grounded
    'Mutable': (100, 130)    # Variable, adaptive
}


class HarmonicEngine:
    """
    Analyzes natal charts and produces musical parameters using
    the 24-mode Quantumelodic system.

    Usage:
        engine = HarmonicEngine()
        result = engine.analyze(chart_data)
    """

    def __init__(self, mappings_path: Optional[str] = None):
        """
        Initialize the harmonic engine.

        Args:
            mappings_path: Path to CSV mapping files. If None, uses defaults.
        """
        self.pentatonic_modes = DEFAULT_PENTATONIC_MODES.copy()
        self.quadratonic_modes = DEFAULT_QUADRATONIC_MODES.copy()

        if mappings_path:
            self._load_mappings(mappings_path)

    def _load_mappings(self, path: str) -> None:
        """Load custom mode mappings from CSV files."""
        mappings_dir = Path(path)

        # Load pentatonic modes
        pentatonic_file = mappings_dir / 'pentatonic_modes.csv'
        if pentatonic_file.exists():
            self._load_pentatonic_csv(pentatonic_file)

        # Load quadratonic modes
        quadratonic_file = mappings_dir / 'quadratonic_modes.csv'
        if quadratonic_file.exists():
            self._load_quadratonic_csv(quadratonic_file)

    def _load_pentatonic_csv(self, filepath: Path) -> None:
        """Load pentatonic modes from CSV."""
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                sign = row['zodiac_sign']
                self.pentatonic_modes[sign] = PentatonicMode(
                    mode_id=row['mode_id'],
                    mode_name=row['mode_name'],
                    zodiac_sign=sign,
                    semitone_pattern=row['semitone_pattern'],
                    archetype=row['archetype'],
                    emotional_color=row['emotional_color'],
                    sonic_role=row['sonic_role'],
                    waveform=row['waveform'],
                    timbre=row['timbre'],
                    element=row['element']
                )

    def _load_quadratonic_csv(self, filepath: Path) -> None:
        """Load quadratonic modes from CSV."""
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                key = (row['modality'], row['element'])
                self.quadratonic_modes[key] = QuadratonicMode(
                    mode_id=row['mode_id'],
                    mode_name=row['mode_name'],
                    archetype=row['archetype'],
                    modality=row['modality'],
                    element=row['element'],
                    semitone_pattern=row['semitone_pattern'],
                    rhythmic_emphasis=row['rhythmic_emphasis'],
                    dynamic_character=row['dynamic_character']
                )

    def analyze(self, chart_data: Dict[str, Any]) -> HarmonicResult:
        """
        Analyze natal chart data and produce harmonic parameters.

        Args:
            chart_data: Natal chart data dictionary from ChartBuilder

        Returns:
            HarmonicResult with all musical parameters
        """
        # Extract key data from chart
        sun_sign = self._get_sun_sign(chart_data)
        moon_sign = self._get_moon_sign(chart_data)
        rising_sign = self._get_rising_sign(chart_data)
        dominant_element = self._get_dominant_element(chart_data)
        dominant_modality = self._get_dominant_modality(chart_data)

        # Determine primary pentatonic mode (based on Sun sign)
        primary_pentatonic = self.pentatonic_modes.get(
            sun_sign,
            list(self.pentatonic_modes.values())[0]
        )

        # Determine secondary pentatonic mode (based on Moon sign)
        secondary_pentatonic = self.pentatonic_modes.get(moon_sign)

        # Determine quadratonic mode (based on dominant modality x element)
        quadratonic_key = (dominant_modality, dominant_element)
        primary_quadratonic = self.quadratonic_modes.get(
            quadratonic_key,
            list(self.quadratonic_modes.values())[0]
        )

        # Determine secondary quadratonic (based on rising sign)
        rising_modality = SIGN_MODALITY.get(rising_sign, 'Cardinal')
        rising_element = SIGN_ELEMENT.get(rising_sign, 'Fire')
        secondary_quadratonic = self.quadratonic_modes.get(
            (rising_modality, rising_element)
        )

        # Calculate harmonic tension from aspects
        tension_index = self._calculate_tension_index(chart_data)

        # Determine tempo based on modality
        tempo_range = MODALITY_TEMPO.get(dominant_modality, (100, 120))
        # Adjust tempo based on tension (higher tension = faster)
        tempo_bpm = tempo_range[0] + int((tempo_range[1] - tempo_range[0]) * (tension_index / 100))

        # Determine key signature based on element
        key_options = ELEMENT_KEYS.get(dominant_element, ['C major'])
        key_signature = key_options[0]  # Could randomize or calculate further

        # Determine time signature (4/4 default, modify based on aspects)
        time_signature = self._determine_time_signature(chart_data)

        # Get dynamics from element
        dynamics = ELEMENT_DYNAMICS.get(dominant_element, 'mf')

        # Calculate elemental balance
        elemental_balance = self._calculate_elemental_balance(chart_data)

        return HarmonicResult(
            primary_pentatonic_mode=primary_pentatonic,
            primary_quadratonic_mode=primary_quadratonic,
            secondary_pentatonic_mode=secondary_pentatonic,
            secondary_quadratonic_mode=secondary_quadratonic,
            harmonic_tension_index=tension_index,
            tempo_bpm=tempo_bpm,
            key_signature=key_signature,
            time_signature=time_signature,
            dominant_element=dominant_element,
            waveform=primary_pentatonic.waveform,
            timbre=primary_pentatonic.timbre,
            dynamics=dynamics,
            modal_blend=self._calculate_modal_blend(sun_sign, moon_sign, rising_sign),
            aspect_tensions=self._extract_aspect_tensions(chart_data),
            elemental_balance=elemental_balance
        )

    def _get_sun_sign(self, chart_data: Dict) -> str:
        """Extract Sun sign from chart data."""
        # Handle different chart data formats
        if 'summary' in chart_data:
            return chart_data['summary'].get('sun_sign', 'Aries')
        if 'sun_sign' in chart_data:
            return chart_data['sun_sign']
        # Look in planets list
        planets = chart_data.get('planets', [])
        for p in planets:
            if p.get('planet') == 'Sun':
                return p.get('zodiac_sign', 'Aries')
        return 'Aries'

    def _get_moon_sign(self, chart_data: Dict) -> str:
        """Extract Moon sign from chart data."""
        if 'summary' in chart_data:
            return chart_data['summary'].get('moon_sign', 'Cancer')
        if 'moon_sign' in chart_data:
            return chart_data['moon_sign']
        planets = chart_data.get('planets', [])
        for p in planets:
            if p.get('planet') == 'Moon':
                return p.get('zodiac_sign', 'Cancer')
        return 'Cancer'

    def _get_rising_sign(self, chart_data: Dict) -> str:
        """Extract rising sign from chart data."""
        if 'summary' in chart_data:
            return chart_data['summary'].get('rising_sign', 'Aries')
        if 'rising_sign' in chart_data:
            return chart_data['rising_sign']
        houses = chart_data.get('houses', [])
        if houses:
            return houses[0].get('zodiac_sign', 'Aries')
        return 'Aries'

    def _get_dominant_element(self, chart_data: Dict) -> str:
        """Get dominant element from chart or calculate it."""
        if 'summary' in chart_data:
            return chart_data['summary'].get('dominant_element', 'Fire')
        if 'dominant_element' in chart_data:
            return chart_data['dominant_element']

        # Calculate from planets
        element_counts = {'Fire': 0, 'Earth': 0, 'Air': 0, 'Water': 0}
        for planet in chart_data.get('planets', []):
            sign = planet.get('zodiac_sign', '')
            element = SIGN_ELEMENT.get(sign, '')
            if element:
                element_counts[element] += 1

        return max(element_counts, key=element_counts.get)

    def _get_dominant_modality(self, chart_data: Dict) -> str:
        """Get dominant modality from chart or calculate it."""
        if 'summary' in chart_data:
            return chart_data['summary'].get('dominant_modality', 'Cardinal')
        if 'dominant_modality' in chart_data:
            return chart_data['dominant_modality']

        # Calculate from planets
        modality_counts = {'Cardinal': 0, 'Fixed': 0, 'Mutable': 0}
        for planet in chart_data.get('planets', []):
            sign = planet.get('zodiac_sign', '')
            modality = SIGN_MODALITY.get(sign, '')
            if modality:
                modality_counts[modality] += 1

        return max(modality_counts, key=modality_counts.get)

    def _calculate_tension_index(self, chart_data: Dict) -> int:
        """
        Calculate harmonic tension index (0-100) based on aspects.
        Squares and oppositions increase tension; trines and sextiles decrease it.
        """
        aspects = chart_data.get('aspects', [])
        if not aspects:
            return 50  # Neutral

        tension_score = 50  # Start neutral

        for aspect in aspects:
            aspect_type = aspect.get('aspect_type', '')
            orb = aspect.get('orb', 5)

            # Tighter orbs have stronger effect
            orb_multiplier = max(0.2, 1 - (orb / 10))

            if aspect_type in ['square', 'opposition']:
                tension_score += int(10 * orb_multiplier)
            elif aspect_type in ['trine', 'sextile']:
                tension_score -= int(5 * orb_multiplier)
            elif aspect_type == 'conjunction':
                # Conjunctions can go either way - slight tension increase
                tension_score += int(3 * orb_multiplier)

        return max(0, min(100, tension_score))

    def _determine_time_signature(self, chart_data: Dict) -> str:
        """Determine time signature based on chart characteristics."""
        dominant_modality = self._get_dominant_modality(chart_data)

        if dominant_modality == 'Cardinal':
            return '4/4'  # Strong, driving
        elif dominant_modality == 'Fixed':
            return '4/4'  # Steady, grounded
        else:  # Mutable
            # More variety for mutable signs
            return '3/4'  # Flowing, adaptive

    def _calculate_modal_blend(self, sun_sign: str, moon_sign: str, rising_sign: str) -> Dict[str, float]:
        """Calculate percentage blend of modal influences."""
        # Simple weighting: Sun 50%, Moon 30%, Rising 20%
        return {
            sun_sign: 0.5,
            moon_sign: 0.3,
            rising_sign: 0.2
        }

    def _extract_aspect_tensions(self, chart_data: Dict) -> list:
        """Extract aspect tension data for detailed analysis."""
        aspects = chart_data.get('aspects', [])
        tensions = []

        for aspect in aspects:
            tensions.append({
                'planets': f"{aspect.get('planet1', '')} - {aspect.get('planet2', '')}",
                'type': aspect.get('aspect_type', ''),
                'orb': aspect.get('orb', 0),
                'applying': aspect.get('applying', False)
            })

        return tensions

    def _calculate_elemental_balance(self, chart_data: Dict) -> Dict[str, float]:
        """Calculate percentage of each element in the chart."""
        element_counts = {'Fire': 0, 'Earth': 0, 'Air': 0, 'Water': 0}

        for planet in chart_data.get('planets', []):
            sign = planet.get('zodiac_sign', '')
            element = SIGN_ELEMENT.get(sign, '')
            if element:
                element_counts[element] += 1

        total = sum(element_counts.values()) or 1
        return {k: v / total for k, v in element_counts.items()}
