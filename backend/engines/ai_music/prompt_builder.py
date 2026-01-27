"""
AI Music Engine - Prompt Builder

Generates prompts for AI music generation services like Suno and Stable Audio
based on harmonic analysis results.
"""

from typing import Dict


class PromptBuilder:
    """
    Builds text prompts for AI music generation services.

    Translates musical parameters from harmonic analysis into
    natural language descriptions optimized for:
    - Suno AI
    - Stable Audio
    - Other text-to-music models
    """

    # Genre suggestions by element
    ELEMENT_GENRES = {
        "Fire": ["epic orchestral", "power metal", "electronic dance", "aggressive synth"],
        "Earth": ["ambient", "lo-fi", "acoustic folk", "classical piano"],
        "Air": ["jazz fusion", "progressive rock", "experimental electronic", "new age"],
        "Water": ["ambient soundscape", "dream pop", "ethereal vocals", "ocean waves"]
    }

    # Mood descriptors by archetype
    ARCHETYPE_MOODS = {
        "The Pioneer": "bold, adventurous, initiating, courageous",
        "The Builder": "grounded, sensual, patient, earthy",
        "The Messenger": "curious, quick, playful, communicative",
        "The Nurturer": "emotional, protective, nurturing, lunar",
        "The Sovereign": "regal, confident, dramatic, radiant",
        "The Analyst": "precise, detailed, pure, methodical",
        "The Harmonizer": "balanced, beautiful, diplomatic, graceful",
        "The Transformer": "intense, deep, mysterious, transformative",
        "The Explorer": "expansive, philosophical, adventurous, optimistic",
        "The Architect": "structured, ambitious, disciplined, enduring",
        "The Innovator": "revolutionary, unconventional, futuristic, electric",
        "The Dreamer": "ethereal, mystical, flowing, transcendent"
    }

    # Instrument suggestions by waveform
    WAVEFORM_INSTRUMENTS = {
        "Sawtooth": ["brass section", "distorted synth", "electric guitar", "lead synth"],
        "Sine": ["flute", "soft pads", "vibraphone", "clean piano"],
        "Triangle": ["woodwinds", "bells", "marimba", "acoustic guitar"],
        "Square": ["bass synth", "chiptune", "organ", "power chords"],
        "Noise/FM": ["glitch elements", "industrial percussion", "synthesizer textures", "white noise sweeps"]
    }

    def __init__(self):
        """Initialize the prompt builder."""
        pass

    def build_suno_prompt(self, harmonic_result) -> str:
        """
        Build a prompt optimized for Suno AI.

        Args:
            harmonic_result: HarmonicResult object or dict

        Returns:
            Text prompt for Suno
        """
        # Extract values (handle both object and dict)
        if hasattr(harmonic_result, 'mode_name'):
            mode_name = harmonic_result.mode_name
            archetype = harmonic_result.archetype
            emotional_color = harmonic_result.emotional_color
            tempo_bpm = harmonic_result.tempo_bpm
            key_signature = harmonic_result.key_signature
            dominant_element = harmonic_result.dominant_element
            tension_index = harmonic_result.harmonic_tension_index
            waveform = harmonic_result.waveform
            timbre = harmonic_result.timbre
        else:
            mode_name = harmonic_result.get('mode_name', 'Pentatonic')
            archetype = harmonic_result.get('archetype', 'The Dreamer')
            emotional_color = harmonic_result.get('emotional_color', 'Ethereal')
            tempo_bpm = harmonic_result.get('recommended_tempo', 90)
            key_signature = harmonic_result.get('key_signature', 'C major')
            dominant_element = harmonic_result.get('dominant_element', 'Water')
            tension_index = harmonic_result.get('tension_index', 50)
            waveform = harmonic_result.get('waveform', 'Sine')
            timbre = harmonic_result.get('timbre', 'Warm')

            # Handle nested mode_details
            mode_details = harmonic_result.get('mode_details', {})
            if mode_details:
                mode_name = mode_details.get('mode_name', mode_name)
                archetype = mode_details.get('archetype', archetype)
                emotional_color = mode_details.get('emotional_color', emotional_color)
                waveform = mode_details.get('waveform', waveform)
                timbre = mode_details.get('timbre', timbre)

        # Get mood descriptor
        mood = self.ARCHETYPE_MOODS.get(archetype, "evocative, cosmic, personal")

        # Get genre suggestions
        genres = self.ELEMENT_GENRES.get(dominant_element, ["ambient", "electronic"])
        genre_str = " and ".join(genres[:2])

        # Get instrument suggestions
        instruments = self.WAVEFORM_INSTRUMENTS.get(waveform, ["synthesizer", "piano"])
        instrument_str = ", ".join(instruments[:2])

        # Determine energy level from tension
        if tension_index < 30:
            energy = "calm, meditative"
        elif tension_index < 60:
            energy = "flowing, dynamic"
        elif tension_index < 80:
            energy = "energetic, powerful"
        else:
            energy = "intense, dramatic"

        # Build the prompt
        prompt = f"""Create a {genre_str} track that embodies {archetype.lower()} energy.

Mood: {mood}
Color palette: {emotional_color}
Energy: {energy}

Musical parameters:
- Tempo: {tempo_bpm} BPM
- Key: {key_signature}
- Lead instruments: {instrument_str}
- Sound texture: {timbre}

The composition should feel like a cosmic journey through personal destiny,
using {mode_name} intervals to create a unique tonal signature.
Include subtle evolving pads and rhythmic elements that pulse with {dominant_element.lower()} element energy."""

        return prompt.strip()

    def build_stable_audio_prompt(self, harmonic_result) -> str:
        """
        Build a prompt optimized for Stable Audio.

        Args:
            harmonic_result: HarmonicResult object or dict

        Returns:
            Text prompt for Stable Audio
        """
        # Extract values
        if hasattr(harmonic_result, 'mode_name'):
            archetype = harmonic_result.archetype
            tempo_bpm = harmonic_result.tempo_bpm
            dominant_element = harmonic_result.dominant_element
            tension_index = harmonic_result.harmonic_tension_index
            waveform = harmonic_result.waveform
        else:
            archetype = harmonic_result.get('archetype', 'The Dreamer')
            tempo_bpm = harmonic_result.get('recommended_tempo', 90)
            dominant_element = harmonic_result.get('dominant_element', 'Water')
            tension_index = harmonic_result.get('tension_index', 50)
            waveform = harmonic_result.get('waveform', 'Sine')

            mode_details = harmonic_result.get('mode_details', {})
            if mode_details:
                archetype = mode_details.get('archetype', archetype)
                waveform = mode_details.get('waveform', waveform)

        # Get genre
        genres = self.ELEMENT_GENRES.get(dominant_element, ["ambient"])

        # Get instruments
        instruments = self.WAVEFORM_INSTRUMENTS.get(waveform, ["synthesizer"])

        # Stable Audio prefers more concise prompts
        if tension_index < 50:
            style = "ambient, atmospheric, dreamy"
        else:
            style = "cinematic, epic, powerful"

        prompt = f"""{style}, {genres[0]}, {tempo_bpm} BPM, {instruments[0]}, {dominant_element.lower()} element energy, cosmic, ethereal, professional production quality"""

        return prompt.strip()

    def build_custom_prompt(
        self,
        harmonic_result,
        style: str = None,
        additional_instruments: list = None,
        mood_override: str = None
    ) -> str:
        """
        Build a customizable prompt with user overrides.

        Args:
            harmonic_result: HarmonicResult object or dict
            style: Optional style override
            additional_instruments: Additional instruments to include
            mood_override: Override the mood descriptor

        Returns:
            Customized text prompt
        """
        base_prompt = self.build_suno_prompt(harmonic_result)

        # Add customizations
        additions = []

        if style:
            additions.append(f"Style: {style}")

        if additional_instruments:
            additions.append(f"Additional instruments: {', '.join(additional_instruments)}")

        if mood_override:
            additions.append(f"Mood emphasis: {mood_override}")

        if additions:
            base_prompt += "\n\nCustomizations:\n" + "\n".join(additions)

        return base_prompt
