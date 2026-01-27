# Quantumelodic Engines Package
"""
Core engines for the Quantumelodic system:
- ephemeris: Natal chart calculations using Swiss Ephemeris
- harmonic: 24-mode pentatonic/quadratonic harmonic analysis
- midi: MIDI file generation from harmonic analysis
- ai_music: AI prompt generation for Suno, Stable Audio, etc.

Note: Imports are done lazily to handle missing dependencies gracefully.
"""

__all__ = ['ChartBuilder', 'HarmonicEngine', 'MIDIExporter', 'PromptBuilder']

# Lazy imports - import engines individually to handle missing deps
def __getattr__(name):
    if name == 'ChartBuilder':
        from .ephemeris.chart_builder import ChartBuilder
        return ChartBuilder
    elif name == 'HarmonicEngine':
        from .harmonic.engine import HarmonicEngine
        return HarmonicEngine
    elif name == 'MIDIExporter':
        from .midi.exporter import MIDIExporter
        return MIDIExporter
    elif name == 'PromptBuilder':
        from .ai_music.prompt_builder import PromptBuilder
        return PromptBuilder
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
