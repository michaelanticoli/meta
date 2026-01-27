"""
Data models for the harmonic analysis system.
"""

from dataclasses import dataclass, asdict
from typing import List, Optional, Dict, Any


@dataclass
class PentatonicMode:
    """
    Represents one of the 12 pentatonic modes in the Quantumelodic system.
    Each zodiac sign maps to a unique pentatonic mode with specific
    musical and archetypal characteristics.
    """
    mode_id: str  # e.g., "P1_ARIES"
    mode_name: str  # e.g., "Aries Pentatonic"
    zodiac_sign: str
    semitone_pattern: str  # e.g., "0-2-4-7-9"
    archetype: str  # e.g., "The Pioneer"
    emotional_color: str  # e.g., "Bold, Initiating"
    sonic_role: str  # e.g., "Rhythmic Driver"
    waveform: str  # e.g., "sawtooth"
    timbre: str  # e.g., "brass"
    element: str  # Fire, Earth, Air, Water

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class QuadratonicMode:
    """
    Represents one of the 12 quadratonic (behavioral) modes.
    These modes represent the behavioral/action dimension of the chart.
    """
    mode_id: str  # e.g., "Q1_CARDINAL_FIRE"
    mode_name: str  # e.g., "Cardinal Fire Quadratonic"
    archetype: str  # e.g., "The Initiator"
    modality: str  # Cardinal, Fixed, Mutable
    element: str  # Fire, Earth, Air, Water
    semitone_pattern: str  # 4-note pattern
    rhythmic_emphasis: str  # e.g., "downbeat"
    dynamic_character: str  # e.g., "explosive"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class HarmonicResult:
    """
    Complete harmonic analysis result combining pentatonic and quadratonic modes.
    """
    # Primary modes
    primary_pentatonic_mode: PentatonicMode
    primary_quadratonic_mode: QuadratonicMode

    # Secondary influences
    secondary_pentatonic_mode: Optional[PentatonicMode] = None
    secondary_quadratonic_mode: Optional[QuadratonicMode] = None

    # Musical parameters
    harmonic_tension_index: int = 50  # 0-100 scale
    tempo_bpm: int = 120
    key_signature: str = "C major"
    time_signature: str = "4/4"

    # Timbre and dynamics
    dominant_element: str = "Fire"
    waveform: str = "sine"
    timbre: str = "piano"
    dynamics: str = "mf"  # pp, p, mp, mf, f, ff

    # Additional harmonic data
    modal_blend: Dict[str, float] = None  # Percentage contribution of each mode
    aspect_tensions: List[Dict] = None  # Tensions from planetary aspects
    elemental_balance: Dict[str, float] = None  # Element percentages

    def __post_init__(self):
        if self.modal_blend is None:
            self.modal_blend = {}
        if self.aspect_tensions is None:
            self.aspect_tensions = []
        if self.elemental_balance is None:
            self.elemental_balance = {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "primary_mode": self.primary_pentatonic_mode.to_dict(),
            "behavioral_mode": self.primary_quadratonic_mode.to_dict(),
            "secondary_pentatonic": self.secondary_pentatonic_mode.to_dict() if self.secondary_pentatonic_mode else None,
            "secondary_quadratonic": self.secondary_quadratonic_mode.to_dict() if self.secondary_quadratonic_mode else None,
            "tension_index": self.harmonic_tension_index,
            "tempo_bpm": self.tempo_bpm,
            "key_signature": self.key_signature,
            "time_signature": self.time_signature,
            "dominant_element": self.dominant_element,
            "waveform": self.waveform,
            "timbre": self.timbre,
            "dynamics": self.dynamics,
            "modal_blend": self.modal_blend,
            "aspect_tensions": self.aspect_tensions,
            "elemental_balance": self.elemental_balance
        }
