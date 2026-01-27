"""
MIDI Exporter - Generates MIDI files from harmonic analysis.

Transforms the harmonic analysis results into playable MIDI compositions
using the midiutil library.

TODO: Integrate with quantumelodic-mvp/src/midi_engine/
"""

from io import BytesIO
from typing import Dict, Any, List
from midiutil import MIDIFile


# MIDI note numbers for root notes (C3 = 60)
ROOT_NOTES = {
    'C': 60, 'C#': 61, 'Db': 61,
    'D': 62, 'D#': 63, 'Eb': 63,
    'E': 64,
    'F': 65, 'F#': 66, 'Gb': 66,
    'G': 67, 'G#': 68, 'Ab': 68,
    'A': 69, 'A#': 70, 'Bb': 70,
    'B': 71
}

# Key to root note mapping
KEY_ROOT = {
    'C major': 'C', 'C minor': 'C',
    'G major': 'G', 'G minor': 'G',
    'D major': 'D', 'D minor': 'D',
    'A major': 'A', 'A minor': 'A',
    'E major': 'E', 'E minor': 'E',
    'B major': 'B', 'B minor': 'B',
    'F major': 'F', 'F minor': 'F',
    'Bb major': 'Bb', 'Bb minor': 'Bb',
    'Eb major': 'Eb', 'Eb minor': 'Eb'
}

# Dynamics to velocity mapping
DYNAMICS_VELOCITY = {
    'pp': 30,
    'p': 50,
    'mp': 70,
    'mf': 85,
    'f': 100,
    'ff': 120
}

# Element to MIDI program/instrument mapping
ELEMENT_INSTRUMENTS = {
    'Fire': 80,    # Lead synth (square)
    'Earth': 48,   # Orchestral strings
    'Air': 73,     # Flute
    'Water': 88    # Pad (new age)
}


class MIDIExporter:
    """
    Generates MIDI files from harmonic analysis results.

    Usage:
        exporter = MIDIExporter()
        midi_bytes = exporter.generate(harmonic_result)
    """

    def __init__(self):
        """Initialize the MIDI exporter."""
        self.default_tempo = 120
        self.default_duration = 16  # 16 beats (4 bars in 4/4)

    def generate(self, harmonic_data: Dict[str, Any], duration_bars: int = 8) -> bytes:
        """
        Generate a MIDI file from harmonic analysis data.

        Args:
            harmonic_data: Harmonic analysis result dictionary
            duration_bars: Number of bars to generate

        Returns:
            MIDI file as bytes
        """
        # Extract parameters from harmonic data
        tempo = harmonic_data.get('tempo_bpm', self.default_tempo)
        key = harmonic_data.get('key_signature', 'C major')
        time_sig = harmonic_data.get('time_signature', '4/4')
        dynamics = harmonic_data.get('dynamics', 'mf')
        element = harmonic_data.get('dominant_element', 'Fire')

        # Get mode data
        primary_mode = harmonic_data.get('primary_mode', {})
        semitone_pattern = primary_mode.get('semitone_pattern', '0-2-4-7-9')

        # Parse time signature
        beats_per_bar = int(time_sig.split('/')[0])
        total_beats = duration_bars * beats_per_bar

        # Create MIDI file
        midi = MIDIFile(numTracks=3)  # Melody, Harmony, Bass

        # Set tempo
        midi.addTempo(0, 0, tempo)
        midi.addTempo(1, 0, tempo)
        midi.addTempo(2, 0, tempo)

        # Set instruments
        melody_instrument = ELEMENT_INSTRUMENTS.get(element, 0)
        midi.addProgramChange(0, 0, 0, melody_instrument)  # Melody
        midi.addProgramChange(1, 1, 0, 48)  # Harmony (strings)
        midi.addProgramChange(2, 2, 0, 32)  # Bass (acoustic bass)

        # Get scale notes
        root = KEY_ROOT.get(key, 'C')
        root_note = ROOT_NOTES.get(root, 60)
        scale = self._parse_semitone_pattern(semitone_pattern, root_note)

        # Get velocity from dynamics
        velocity = DYNAMICS_VELOCITY.get(dynamics, 85)

        # Generate tracks
        self._generate_melody(midi, scale, total_beats, velocity)
        self._generate_harmony(midi, scale, total_beats, int(velocity * 0.7))
        self._generate_bass(midi, root_note, total_beats, velocity)

        # Write to bytes
        buffer = BytesIO()
        midi.writeFile(buffer)
        buffer.seek(0)
        return buffer.read()

    def _parse_semitone_pattern(self, pattern: str, root: int) -> List[int]:
        """
        Parse a semitone pattern string into MIDI note numbers.

        Args:
            pattern: Semitone pattern like "0-2-4-7-9"
            root: Root MIDI note number

        Returns:
            List of MIDI note numbers
        """
        intervals = [int(x) for x in pattern.split('-')]
        return [root + interval for interval in intervals]

    def _generate_melody(self, midi: MIDIFile, scale: List[int], total_beats: float, velocity: int):
        """Generate melody track using the pentatonic scale."""
        track = 0
        channel = 0
        time = 0.0

        # Simple generative melody algorithm
        import random
        random.seed(42)  # Consistent generation for same input

        scale_extended = scale + [n + 12 for n in scale]  # Add octave

        while time < total_beats:
            # Choose note from scale
            note = random.choice(scale_extended)

            # Vary duration (quarter, half, whole notes)
            duration_options = [0.5, 1.0, 1.5, 2.0]
            duration = random.choice(duration_options)

            # Vary velocity slightly
            note_velocity = max(40, min(127, velocity + random.randint(-15, 15)))

            # Add note
            midi.addNote(track, channel, note, time, duration, note_velocity)

            # Occasional rests
            if random.random() < 0.2:
                time += random.choice([0.5, 1.0])

            time += duration

    def _generate_harmony(self, midi: MIDIFile, scale: List[int], total_beats: float, velocity: int):
        """Generate harmony track with sustained chords."""
        track = 1
        channel = 1
        time = 0.0

        # Build simple triads from scale
        chord_duration = 4.0  # Whole notes

        while time < total_beats:
            # Root position chord from scale
            if len(scale) >= 3:
                chord = [scale[0], scale[2], scale[4] if len(scale) > 4 else scale[2] + 3]

                for note in chord:
                    midi.addNote(track, channel, note, time, chord_duration, velocity)

            # Move through scale positions
            scale = scale[1:] + [scale[0] + 12]

            time += chord_duration

    def _generate_bass(self, midi: MIDIFile, root: int, total_beats: float, velocity: int):
        """Generate bass track with root movement."""
        track = 2
        channel = 2
        time = 0.0

        bass_root = root - 24  # Two octaves down
        bass_fifth = bass_root + 7

        while time < total_beats:
            # Alternate root and fifth
            midi.addNote(track, channel, bass_root, time, 2.0, velocity)
            time += 2.0

            if time < total_beats:
                midi.addNote(track, channel, bass_fifth, time, 2.0, int(velocity * 0.8))
                time += 2.0

    def generate_from_tension(
        self,
        harmonic_data: Dict[str, Any],
        tension_level: int
    ) -> bytes:
        """
        Generate MIDI with composition style based on tension level.

        Args:
            harmonic_data: Harmonic analysis result
            tension_level: 0-100 tension index

        Returns:
            MIDI file as bytes
        """
        # Adjust parameters based on tension
        if tension_level > 70:
            # High tension: faster, more dissonant
            harmonic_data = dict(harmonic_data)
            harmonic_data['tempo_bpm'] = min(180, harmonic_data.get('tempo_bpm', 120) + 20)
            harmonic_data['dynamics'] = 'f'
        elif tension_level < 30:
            # Low tension: slower, more consonant
            harmonic_data = dict(harmonic_data)
            harmonic_data['tempo_bpm'] = max(60, harmonic_data.get('tempo_bpm', 120) - 20)
            harmonic_data['dynamics'] = 'p'

        return self.generate(harmonic_data)
