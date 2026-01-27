// Quantumelodic Type Definitions

export interface BirthData {
  date: string;
  time: string;
  latitude: number;
  longitude: number;
  timezone: string;
  locationName?: string;
  chartName?: string;
}

export interface PlanetPosition {
  name: string;
  longitude: number;
  latitude: number;
  sign: string;
  degree_in_sign: number;
  retrograde: boolean;
  house: number | null;
}

export interface Aspect {
  planet1: string;
  planet2: string;
  aspect_type: string;
  orb: number;
  exact_degree: number;
}

export interface NatalChart {
  birth_data: {
    date: string;
    time: string;
    latitude: number;
    longitude: number;
    timezone: string;
  };
  planets: PlanetPosition[];
  houses: number[];
  ascendant: number;
  midheaven: number;
  aspects: Aspect[];
  sun_sign: string;
  moon_sign: string;
  rising_sign: string;
}

export interface ModeDetails {
  mode_name: string;
  archetype: string;
  emotional_color: string;
  sonic_role: string;
  waveform: string;
  timbre: string;
}

export interface HarmonicAnalysis {
  primary_mode: string;
  behavioral_mode: string;
  tension_index: number;
  dominant_element: 'Fire' | 'Earth' | 'Air' | 'Water';
  recommended_tempo: number;
  key_signature: string;
  mode_details: ModeDetails;
}

export interface MidiResult {
  midi_data: string;
  filename: string;
}

export interface AIPrompts {
  suno_prompt: string;
  stable_audio_prompt: string;
}

export interface FullWorkflowResult {
  chart: NatalChart;
  harmonic_analysis: HarmonicAnalysis;
  midi: MidiResult;
  ai_prompts: AIPrompts;
}

export interface LocationSearchResult {
  display_name: string;
  lat: string;
  lon: string;
  address?: {
    city?: string;
    state?: string;
    country?: string;
  };
}
