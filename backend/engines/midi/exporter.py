"""
MIDI Engine - MIDI File Generation

Generates MIDI files from harmonic analysis results using the
24-mode Quantumelodic system.
"""

from typing import Dict, List, Optional
from io import BytesIO

# Note: midiutil import will be available when dependencies are installed
# from midiutil import MIDIFile


class MIDIExporter:
    """
    Generates MIDI files from harmonic analysis data.

    Creates multi-track MIDI compositions based on:
    - Pentatonic mode scale
    - Tempo from element analysis
    - Chord progressions
    - Melodic patterns
    """

    # MIDI note values for root notes by key
    KEY_ROOT_NOTES = {
        "C major": 60, "C minor": 60,
        "D major": 62, "D minor": 62,
        "E major": 64, "E minor": 64,
        "F major": 65, "F minor": 65,
        "F# major": 66, "F# minor": 66,
        "G major": 67, "G minor": 67,
        "A major": 69, "A minor": 69,
        "Bb major": 70, "Bb minor": 70,
        "B major": 71, "B minor": 71
    }

    def __init__(self):
        """Initialize the MIDI exporter."""
        pass

    def generate(self, harmonic_result) -> bytes:
        """
        Generate MIDI file from harmonic analysis.

        Args:
            harmonic_result: HarmonicResult object or dict with analysis data

        Returns:
            MIDI file as bytes
        """
        # Handle both HarmonicResult object and dict
        if hasattr(harmonic_result, 'key_signature'):
            key = harmonic_result.key_signature
            tempo = harmonic_result.tempo_bpm
            scale_degrees = harmonic_result.scale_degrees
            chord_progression = harmonic_result.chord_progression
        else:
            key = harmonic_result.get('key_signature', 'C major')
            tempo = harmonic_result.get('recommended_tempo', 90)
            scale_degrees = harmonic_result.get('scale_degrees', [0, 2, 4, 7, 9])
            chord_progression = harmonic_result.get('chord_progression', ['I', 'IV', 'V', 'I'])

        # Get root note
        root_note = self.KEY_ROOT_NOTES.get(key, 60)

        # Build scale notes
        scale_notes = [root_note + degree for degree in scale_degrees]

        # Generate MIDI data
        midi_data = self._create_midi_composition(
            scale_notes=scale_notes,
            tempo=tempo,
            chord_progression=chord_progression,
            key=key
        )

        return midi_data

    def _create_midi_composition(
        self,
        scale_notes: List[int],
        tempo: int,
        chord_progression: List[str],
        key: str
    ) -> bytes:
        """Create a multi-track MIDI composition."""

        # Simplified MIDI generation without midiutil dependency
        # This creates a basic MIDI file structure

        output = BytesIO()

        # MIDI Header (MThd)
        output.write(b'MThd')                    # Chunk type
        output.write((6).to_bytes(4, 'big'))     # Chunk length
        output.write((1).to_bytes(2, 'big'))     # Format type 1
        output.write((2).to_bytes(2, 'big'))     # Number of tracks
        output.write((480).to_bytes(2, 'big'))   # Ticks per quarter note

        # Track 1 - Tempo track
        track1_data = BytesIO()

        # Tempo meta event (microseconds per quarter note)
        microseconds_per_beat = int(60000000 / tempo)
        track1_data.write(bytes([0x00]))  # Delta time
        track1_data.write(bytes([0xFF, 0x51, 0x03]))  # Tempo meta event
        track1_data.write(microseconds_per_beat.to_bytes(3, 'big'))

        # Time signature (4/4)
        track1_data.write(bytes([0x00]))  # Delta time
        track1_data.write(bytes([0xFF, 0x58, 0x04, 0x04, 0x02, 0x18, 0x08]))

        # End of track
        track1_data.write(bytes([0x00, 0xFF, 0x2F, 0x00]))

        # Write track 1
        track1_bytes = track1_data.getvalue()
        output.write(b'MTrk')
        output.write(len(track1_bytes).to_bytes(4, 'big'))
        output.write(track1_bytes)

        # Track 2 - Melody track
        track2_data = BytesIO()

        # Track name
        track_name = b"Cosmic Melody"
        track2_data.write(bytes([0x00]))  # Delta time
        track2_data.write(bytes([0xFF, 0x03, len(track_name)]))
        track2_data.write(track_name)

        # Program change (piano)
        track2_data.write(bytes([0x00]))  # Delta time
        track2_data.write(bytes([0xC0, 0x00]))  # Channel 0, Program 0 (Piano)

        # Generate melody using scale notes
        velocity = 80
        note_duration = 480  # Quarter note

        # Simple ascending/descending pattern
        melody_pattern = scale_notes + scale_notes[::-1]

        for i, note in enumerate(melody_pattern[:8]):  # First 8 notes
            # Note on
            if i == 0:
                track2_data.write(bytes([0x00]))  # First note, no delay
            else:
                # Variable length quantity for note duration
                track2_data.write(self._to_variable_length(note_duration))
            track2_data.write(bytes([0x90, note, velocity]))  # Note on

        # Note off for last note
        track2_data.write(self._to_variable_length(note_duration))
        track2_data.write(bytes([0x80, melody_pattern[7], 0x00]))  # Note off

        # End of track
        track2_data.write(bytes([0x00, 0xFF, 0x2F, 0x00]))

        # Write track 2
        track2_bytes = track2_data.getvalue()
        output.write(b'MTrk')
        output.write(len(track2_bytes).to_bytes(4, 'big'))
        output.write(track2_bytes)

        return output.getvalue()

    def _to_variable_length(self, value: int) -> bytes:
        """Convert an integer to MIDI variable length quantity."""
        result = []
        result.append(value & 0x7F)
        value >>= 7
        while value:
            result.append((value & 0x7F) | 0x80)
            value >>= 7
        return bytes(reversed(result))

    def _chord_to_notes(self, chord: str, root: int) -> List[int]:
        """Convert chord symbol to MIDI notes."""
        # Simplified chord mapping
        if chord == "I" or chord == "i":
            return [root, root + 4, root + 7]
        elif chord == "IV" or chord == "iv":
            return [root + 5, root + 9, root + 12]
        elif chord == "V":
            return [root + 7, root + 11, root + 14]
        elif chord == "vi" or chord == "VI":
            return [root + 9, root + 12, root + 16]
        elif chord == "III":
            return [root + 4, root + 7, root + 11]
        elif chord == "VII":
            return [root + 11, root + 14, root + 18]
        else:
            return [root, root + 4, root + 7]
