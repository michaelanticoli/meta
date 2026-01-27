"""
AI Music Prompt Builder - Generates prompts for AI music services.

Transforms harmonic analysis into optimized prompts for:
- Suno AI
- Stable Audio
- Udio
- Generic text-to-music prompts

TODO: Integrate with quantumelodic-mvp/src/ai_music_engine/
"""

from typing import Dict, Any


# Element to genre/style mapping
ELEMENT_STYLES = {
    'Fire': ['energetic', 'driving', 'powerful', 'triumphant'],
    'Earth': ['grounded', 'organic', 'natural', 'rich'],
    'Air': ['light', 'ethereal', 'flowing', 'airy'],
    'Water': ['dreamy', 'ambient', 'deep', 'emotional']
}

# Element to instrument suggestions
ELEMENT_INSTRUMENTS = {
    'Fire': ['brass', 'electric guitar', 'drums', 'synth leads'],
    'Earth': ['acoustic guitar', 'piano', 'strings', 'percussion'],
    'Air': ['flute', 'wind instruments', 'chimes', 'harp'],
    'Water': ['pads', 'cello', 'ambient synths', 'ocean sounds']
}

# Modality to tempo descriptions
MODALITY_TEMPO = {
    'Cardinal': 'driving, forward-moving',
    'Fixed': 'steady, grounded',
    'Mutable': 'flowing, adaptive'
}

# Tension to mood mapping
TENSION_MOODS = {
    (0, 30): ['peaceful', 'serene', 'calm', 'meditative'],
    (30, 50): ['balanced', 'contemplative', 'gentle', 'warm'],
    (50, 70): ['dynamic', 'expressive', 'building', 'moving'],
    (70, 100): ['intense', 'dramatic', 'powerful', 'climactic']
}


class PromptBuilder:
    """
    Builds optimized prompts for AI music generation services.

    Usage:
        builder = PromptBuilder()
        suno_prompt = builder.build_suno_prompt(harmonic_result)
    """

    def __init__(self):
        """Initialize the prompt builder."""
        pass

    def build_suno_prompt(self, harmonic_data: Dict[str, Any]) -> str:
        """
        Build a prompt optimized for Suno AI.

        Suno works best with:
        - Genre and style descriptions
        - Mood and emotional descriptors
        - Tempo and energy level
        - Instrument suggestions

        Args:
            harmonic_data: Harmonic analysis result dictionary

        Returns:
            Suno-optimized prompt string
        """
        element = harmonic_data.get('dominant_element', 'Fire')
        tension = harmonic_data.get('tension_index', 50)
        tempo = harmonic_data.get('tempo_bpm', 120)
        key = harmonic_data.get('key_signature', 'C major')

        primary_mode = harmonic_data.get('primary_mode', {})
        archetype = primary_mode.get('archetype', 'The Pioneer')
        emotional_color = primary_mode.get('emotional_color', 'Bold, Initiating')

        # Get style words
        styles = ELEMENT_STYLES.get(element, ['atmospheric'])
        instruments = ELEMENT_INSTRUMENTS.get(element, ['piano'])
        mood = self._get_mood_from_tension(tension)

        # Determine genre hint based on element
        genre_hints = {
            'Fire': 'cinematic epic',
            'Earth': 'organic acoustic',
            'Air': 'ambient electronic',
            'Water': 'ethereal ambient'
        }
        genre = genre_hints.get(element, 'atmospheric')

        # Build prompt
        prompt = f"{genre}, {styles[0]} {styles[1] if len(styles) > 1 else 'atmospheric'} "
        prompt += f"instrumental at {tempo} BPM, "
        prompt += f"{mood[0]} and {mood[1] if len(mood) > 1 else 'expressive'}, "
        prompt += f"featuring {instruments[0]} and {instruments[1] if len(instruments) > 1 else 'synths'}, "
        prompt += f"in {key}, "
        prompt += f"evoking {archetype.lower()} energy, "
        prompt += f"{emotional_color.lower()}"

        return prompt

    def build_stable_audio_prompt(self, harmonic_data: Dict[str, Any]) -> str:
        """
        Build a prompt optimized for Stable Audio.

        Stable Audio works best with:
        - Detailed musical descriptions
        - Production quality terms
        - Specific genre tags
        - Duration hints

        Args:
            harmonic_data: Harmonic analysis result dictionary

        Returns:
            Stable Audio-optimized prompt string
        """
        element = harmonic_data.get('dominant_element', 'Fire')
        tension = harmonic_data.get('tension_index', 50)
        tempo = harmonic_data.get('tempo_bpm', 120)
        key = harmonic_data.get('key_signature', 'C major')
        dynamics = harmonic_data.get('dynamics', 'mf')

        primary_mode = harmonic_data.get('primary_mode', {})
        waveform = primary_mode.get('waveform', 'sine')
        timbre = primary_mode.get('timbre', 'piano')

        styles = ELEMENT_STYLES.get(element, ['atmospheric'])
        mood = self._get_mood_from_tension(tension)

        # Map dynamics to production terms
        dynamics_terms = {
            'pp': 'very soft, intimate',
            'p': 'soft, gentle',
            'mp': 'moderate, warm',
            'mf': 'full, present',
            'f': 'loud, powerful',
            'ff': 'very loud, intense'
        }
        production = dynamics_terms.get(dynamics, 'full')

        # Build prompt
        prompt = f"High quality {styles[0]} instrumental music, "
        prompt += f"{tempo} BPM, {key}, "
        prompt += f"{mood[0]} mood, {production} production, "
        prompt += f"featuring {timbre} with {waveform} characteristics, "
        prompt += f"professional studio recording, "
        prompt += f"no vocals, instrumental only"

        return prompt

    def build_udio_prompt(self, harmonic_data: Dict[str, Any]) -> str:
        """
        Build a prompt optimized for Udio.

        Udio works well with:
        - Genre-specific language
        - Artist/style references (general, not specific)
        - Mood and vibe descriptions

        Args:
            harmonic_data: Harmonic analysis result dictionary

        Returns:
            Udio-optimized prompt string
        """
        element = harmonic_data.get('dominant_element', 'Fire')
        tension = harmonic_data.get('tension_index', 50)
        tempo = harmonic_data.get('tempo_bpm', 120)

        primary_mode = harmonic_data.get('primary_mode', {})
        archetype = primary_mode.get('archetype', 'The Pioneer')

        styles = ELEMENT_STYLES.get(element, ['atmospheric'])
        instruments = ELEMENT_INSTRUMENTS.get(element, ['piano'])
        mood = self._get_mood_from_tension(tension)

        # Element to genre style
        element_genres = {
            'Fire': 'epic cinematic score',
            'Earth': 'acoustic folk ambient',
            'Air': 'electronic ambient chill',
            'Water': 'downtempo ambient emotional'
        }
        genre = element_genres.get(element, 'ambient')

        # Build prompt
        prompt = f"{genre}, "
        prompt += f"{styles[0]} {mood[0]} instrumental, "
        prompt += f"{tempo} bpm, "
        prompt += f"featuring {instruments[0]}, "
        prompt += f"{archetype.lower().replace('the ', '')} vibes, "
        prompt += f"no lyrics"

        return prompt

    def build_generic_prompt(self, harmonic_data: Dict[str, Any]) -> str:
        """
        Build a generic prompt suitable for any AI music service.

        Args:
            harmonic_data: Harmonic analysis result dictionary

        Returns:
            Generic prompt string
        """
        element = harmonic_data.get('dominant_element', 'Fire')
        tension = harmonic_data.get('tension_index', 50)
        tempo = harmonic_data.get('tempo_bpm', 120)
        key = harmonic_data.get('key_signature', 'C major')

        primary_mode = harmonic_data.get('primary_mode', {})
        archetype = primary_mode.get('archetype', 'The Pioneer')
        emotional_color = primary_mode.get('emotional_color', 'Bold')

        behavioral_mode = harmonic_data.get('behavioral_mode', {})
        modality = behavioral_mode.get('modality', 'Cardinal')

        styles = ELEMENT_STYLES.get(element, ['atmospheric'])
        instruments = ELEMENT_INSTRUMENTS.get(element, ['piano'])
        mood = self._get_mood_from_tension(tension)
        tempo_desc = MODALITY_TEMPO.get(modality, 'steady')

        # Build descriptive prompt
        lines = [
            f"An instrumental composition embodying {archetype}.",
            f"Style: {styles[0]}, {styles[1] if len(styles) > 1 else 'expressive'}",
            f"Mood: {mood[0]}, {emotional_color.split(',')[0].lower()}",
            f"Tempo: {tempo} BPM ({tempo_desc})",
            f"Key: {key}",
            f"Instruments: {', '.join(instruments[:3])}",
            f"Element: {element}",
            f"Tension Level: {tension}/100"
        ]

        return "\n".join(lines)

    def build_extended_prompt(self, harmonic_data: Dict[str, Any]) -> Dict[str, str]:
        """
        Build an extended set of prompts with variations.

        Args:
            harmonic_data: Harmonic analysis result dictionary

        Returns:
            Dictionary of prompt variations
        """
        return {
            'suno': self.build_suno_prompt(harmonic_data),
            'stable_audio': self.build_stable_audio_prompt(harmonic_data),
            'udio': self.build_udio_prompt(harmonic_data),
            'generic': self.build_generic_prompt(harmonic_data),
            'short': self._build_short_prompt(harmonic_data),
            'detailed': self._build_detailed_prompt(harmonic_data)
        }

    def _get_mood_from_tension(self, tension: int) -> list:
        """Get mood descriptors based on tension level."""
        for (low, high), moods in TENSION_MOODS.items():
            if low <= tension < high:
                return moods
        return ['expressive', 'dynamic']

    def _build_short_prompt(self, harmonic_data: Dict[str, Any]) -> str:
        """Build a minimal, short prompt."""
        element = harmonic_data.get('dominant_element', 'Fire')
        tension = harmonic_data.get('tension_index', 50)
        tempo = harmonic_data.get('tempo_bpm', 120)

        styles = ELEMENT_STYLES.get(element, ['atmospheric'])
        mood = self._get_mood_from_tension(tension)

        return f"{styles[0]} {mood[0]} instrumental, {tempo} bpm"

    def _build_detailed_prompt(self, harmonic_data: Dict[str, Any]) -> str:
        """Build a highly detailed prompt for maximum control."""
        element = harmonic_data.get('dominant_element', 'Fire')
        tension = harmonic_data.get('tension_index', 50)
        tempo = harmonic_data.get('tempo_bpm', 120)
        key = harmonic_data.get('key_signature', 'C major')
        time_sig = harmonic_data.get('time_signature', '4/4')
        dynamics = harmonic_data.get('dynamics', 'mf')

        primary_mode = harmonic_data.get('primary_mode', {})
        archetype = primary_mode.get('archetype', 'The Pioneer')
        emotional_color = primary_mode.get('emotional_color', 'Bold')
        waveform = primary_mode.get('waveform', 'sine')
        timbre = primary_mode.get('timbre', 'piano')
        zodiac = primary_mode.get('zodiac_sign', 'Aries')

        behavioral_mode = harmonic_data.get('behavioral_mode', {})
        modality = behavioral_mode.get('modality', 'Cardinal')
        rhythmic_emphasis = behavioral_mode.get('rhythmic_emphasis', 'steady')

        styles = ELEMENT_STYLES.get(element, ['atmospheric'])
        instruments = ELEMENT_INSTRUMENTS.get(element, ['piano'])
        mood = self._get_mood_from_tension(tension)

        prompt = f"""Create an instrumental composition with the following specifications:

MUSICAL IDENTITY:
- Archetype: {archetype}
- Zodiac Influence: {zodiac}
- Emotional Color: {emotional_color}
- Dominant Element: {element}

TECHNICAL PARAMETERS:
- Key Signature: {key}
- Tempo: {tempo} BPM
- Time Signature: {time_sig}
- Dynamics: {dynamics}
- Tension Level: {tension}/100

SONIC CHARACTERISTICS:
- Primary Timbre: {timbre}
- Waveform Character: {waveform}
- Suggested Instruments: {', '.join(instruments)}
- Style: {', '.join(styles)}
- Mood: {', '.join(mood[:2])}

RHYTHMIC PROFILE:
- Modality: {modality}
- Rhythmic Emphasis: {rhythmic_emphasis}

PRODUCTION NOTES:
- This is an instrumental piece, no vocals
- Professional studio quality
- Focus on emotional expression and sonic storytelling
"""
        return prompt
