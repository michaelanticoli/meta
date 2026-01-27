-- Quantumelodic Database Schema
-- For use with Supabase PostgreSQL

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =====================================================
-- CORE TABLES
-- =====================================================

-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email TEXT UNIQUE NOT NULL,
    display_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Natal charts table
CREATE TABLE natal_charts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    chart_name TEXT NOT NULL,
    birth_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    timezone TEXT NOT NULL,
    location_name TEXT,
    chart_data JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Musical interpretations table
CREATE TABLE musical_interpretations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    chart_id UUID REFERENCES natal_charts(id) ON DELETE CASCADE,
    primary_mode TEXT NOT NULL,
    behavioral_mode TEXT,
    tension_index INTEGER CHECK (tension_index >= 0 AND tension_index <= 100),
    tempo_bpm INTEGER CHECK (tempo_bpm > 0 AND tempo_bpm <= 300),
    key_signature TEXT NOT NULL,
    dominant_element TEXT CHECK (dominant_element IN ('Fire', 'Earth', 'Air', 'Water')),
    harmonic_data JSONB,
    midi_data BYTEA,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- AI prompts table
CREATE TABLE ai_prompts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    interpretation_id UUID REFERENCES musical_interpretations(id) ON DELETE CASCADE,
    prompt_type TEXT CHECK (prompt_type IN ('suno', 'stable_audio', 'custom')),
    prompt_text TEXT NOT NULL,
    generated_audio_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =====================================================
-- REFERENCE TABLES (24-Mode System)
-- =====================================================

-- Pentatonic modes (12 modes)
CREATE TABLE pentatonic_modes (
    id SERIAL PRIMARY KEY,
    mode_id TEXT UNIQUE NOT NULL,
    zodiac_sign TEXT NOT NULL,
    semitone_pattern TEXT NOT NULL,
    archetype TEXT NOT NULL,
    emotional_color TEXT,
    sonic_role TEXT,
    waveform TEXT,
    timbre TEXT,
    key_root TEXT
);

-- Quadratonic modes (12 modes)
CREATE TABLE quadratonic_modes (
    id SERIAL PRIMARY KEY,
    mode_id TEXT UNIQUE NOT NULL,
    zodiac_sign TEXT NOT NULL,
    semitone_pattern TEXT NOT NULL,
    behavioral_pattern TEXT,
    rhythmic_emphasis TEXT
);

-- Element timbres mapping
CREATE TABLE element_timbres (
    id SERIAL PRIMARY KEY,
    element TEXT UNIQUE NOT NULL CHECK (element IN ('Fire', 'Earth', 'Air', 'Water')),
    primary_waveform TEXT NOT NULL,
    tempo_range_min INTEGER NOT NULL,
    tempo_range_max INTEGER NOT NULL,
    brightness DECIMAL(3, 2) CHECK (brightness >= 0 AND brightness <= 1),
    attack_time TEXT,
    decay_characteristics TEXT,
    recommended_instruments TEXT[]
);

-- Planetary aspects to sound mapping
CREATE TABLE aspect_sounds (
    id SERIAL PRIMARY KEY,
    aspect_type TEXT UNIQUE NOT NULL,
    harmonic_effect TEXT,
    tension_modifier INTEGER,
    interval_suggestion TEXT,
    sonic_descriptor TEXT
);

-- =====================================================
-- INDEXES
-- =====================================================

CREATE INDEX idx_natal_charts_user_id ON natal_charts(user_id);
CREATE INDEX idx_natal_charts_created_at ON natal_charts(created_at DESC);
CREATE INDEX idx_musical_interpretations_chart_id ON musical_interpretations(chart_id);
CREATE INDEX idx_ai_prompts_interpretation_id ON ai_prompts(interpretation_id);
CREATE INDEX idx_pentatonic_modes_zodiac ON pentatonic_modes(zodiac_sign);
CREATE INDEX idx_quadratonic_modes_zodiac ON quadratonic_modes(zodiac_sign);

-- =====================================================
-- ROW LEVEL SECURITY
-- =====================================================

ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE natal_charts ENABLE ROW LEVEL SECURITY;
ALTER TABLE musical_interpretations ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_prompts ENABLE ROW LEVEL SECURITY;

-- Users can only see their own data
CREATE POLICY "Users can view own profile" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own profile" ON users
    FOR UPDATE USING (auth.uid() = id);

-- Users can manage their own charts
CREATE POLICY "Users can view own charts" ON natal_charts
    FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY "Users can create own charts" ON natal_charts
    FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own charts" ON natal_charts
    FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own charts" ON natal_charts
    FOR DELETE USING (auth.uid() = user_id);

-- Users can access interpretations for their charts
CREATE POLICY "Users can view own interpretations" ON musical_interpretations
    FOR SELECT USING (
        chart_id IN (SELECT id FROM natal_charts WHERE user_id = auth.uid())
    );

CREATE POLICY "Users can create interpretations for own charts" ON musical_interpretations
    FOR INSERT WITH CHECK (
        chart_id IN (SELECT id FROM natal_charts WHERE user_id = auth.uid())
    );

-- Users can access AI prompts for their interpretations
CREATE POLICY "Users can view own prompts" ON ai_prompts
    FOR SELECT USING (
        interpretation_id IN (
            SELECT mi.id FROM musical_interpretations mi
            JOIN natal_charts nc ON mi.chart_id = nc.id
            WHERE nc.user_id = auth.uid()
        )
    );

-- Reference tables are public read
CREATE POLICY "Pentatonic modes are public" ON pentatonic_modes
    FOR SELECT USING (true);

CREATE POLICY "Quadratonic modes are public" ON quadratonic_modes
    FOR SELECT USING (true);

CREATE POLICY "Element timbres are public" ON element_timbres
    FOR SELECT USING (true);

CREATE POLICY "Aspect sounds are public" ON aspect_sounds
    FOR SELECT USING (true);

-- =====================================================
-- SEED DATA: Pentatonic Modes
-- =====================================================

INSERT INTO pentatonic_modes (mode_id, zodiac_sign, semitone_pattern, archetype, emotional_color, sonic_role, waveform, timbre, key_root) VALUES
('P01', 'Aries', '2-2-3-2-3', 'The Pioneer', 'Bold Red Fire', 'Initiator', 'Sawtooth', 'Bright, aggressive attack', 'C'),
('P02', 'Taurus', '2-3-2-2-3', 'The Builder', 'Earthy Green', 'Foundation', 'Sine', 'Warm, sustained resonance', 'G'),
('P03', 'Gemini', '3-2-2-3-2', 'The Messenger', 'Quick Silver', 'Connector', 'Triangle', 'Light, dancing quality', 'D'),
('P04', 'Cancer', '2-3-2-3-2', 'The Nurturer', 'Lunar Silver', 'Protector', 'Sine', 'Soft, enveloping warmth', 'F'),
('P05', 'Leo', '2-2-3-3-2', 'The Sovereign', 'Golden Radiance', 'Center Stage', 'Sawtooth', 'Rich, commanding presence', 'A'),
('P06', 'Virgo', '3-2-2-2-3', 'The Analyst', 'Forest Green', 'Refiner', 'Triangle', 'Pure, precise articulation', 'E'),
('P07', 'Libra', '2-3-3-2-2', 'The Harmonizer', 'Rose Pink', 'Balancer', 'Sine', 'Balanced, pleasing harmonics', 'Bb'),
('P08', 'Scorpio', '3-3-2-2-2', 'The Transformer', 'Deep Crimson', 'Depth Seeker', 'Square', 'Dark, intense resonance', 'E'),
('P09', 'Sagittarius', '2-2-2-3-3', 'The Explorer', 'Purple Horizon', 'Expander', 'Sawtooth', 'Expansive, soaring quality', 'B'),
('P10', 'Capricorn', '3-2-3-2-2', 'The Architect', 'Mountain Gray', 'Structure', 'Square', 'Solid, grounded bass', 'A'),
('P11', 'Aquarius', '2-3-2-2-3', 'The Innovator', 'Electric Blue', 'Disruptor', 'Noise/FM', 'Unusual, synthetic texture', 'F#'),
('P12', 'Pisces', '3-2-2-3-2', 'The Dreamer', 'Ocean Mist', 'Dissolver', 'Sine', 'Ethereal, reverberant', 'D');

-- =====================================================
-- SEED DATA: Quadratonic Modes
-- =====================================================

INSERT INTO quadratonic_modes (mode_id, zodiac_sign, semitone_pattern, behavioral_pattern, rhythmic_emphasis) VALUES
('Q01', 'Aries', '3-2-4-3', 'Action-oriented', 'Driving, forward momentum'),
('Q02', 'Taurus', '2-4-3-3', 'Stability-seeking', 'Steady, grounded pulse'),
('Q03', 'Gemini', '4-3-2-3', 'Information-gathering', 'Quick, varied patterns'),
('Q04', 'Cancer', '3-3-4-2', 'Protection-focused', 'Flowing, protective cycles'),
('Q05', 'Leo', '2-3-3-4', 'Expression-driven', 'Bold, dramatic accents'),
('Q06', 'Virgo', '4-2-3-3', 'Analysis-oriented', 'Precise, detailed rhythms'),
('Q07', 'Libra', '3-4-2-3', 'Harmony-seeking', 'Balanced, symmetrical phrases'),
('Q08', 'Scorpio', '3-3-2-4', 'Transformation-focused', 'Deep, pulsing intensity'),
('Q09', 'Sagittarius', '2-3-4-3', 'Expansion-driven', 'Galloping, expansive feel'),
('Q10', 'Capricorn', '4-3-3-2', 'Achievement-oriented', 'Climbing, structured builds'),
('Q11', 'Aquarius', '3-2-3-4', 'Innovation-focused', 'Unexpected, syncopated breaks'),
('Q12', 'Pisces', '3-4-3-2', 'Dissolution-seeking', 'Dissolving, ambient flow');

-- =====================================================
-- SEED DATA: Element Timbres
-- =====================================================

INSERT INTO element_timbres (element, primary_waveform, tempo_range_min, tempo_range_max, brightness, attack_time, decay_characteristics, recommended_instruments) VALUES
('Fire', 'sawtooth', 100, 140, 0.80, 'Fast attack', 'Quick decay, sustain', ARRAY['brass', 'distorted guitar', 'synth lead']),
('Earth', 'sine', 60, 90, 0.40, 'Slow attack', 'Long sustain, slow release', ARRAY['bass', 'cello', 'piano', 'acoustic guitar']),
('Air', 'triangle', 90, 120, 0.60, 'Medium attack', 'Medium decay', ARRAY['flute', 'bells', 'harp', 'woodwinds']),
('Water', 'sine', 50, 80, 0.30, 'Slow attack', 'Long reverberant tail', ARRAY['pads', 'strings', 'ocean sounds', 'ambient synth']);

-- =====================================================
-- SEED DATA: Aspect Sounds
-- =====================================================

INSERT INTO aspect_sounds (aspect_type, harmonic_effect, tension_modifier, interval_suggestion, sonic_descriptor) VALUES
('conjunction', 'Fusion/Blend', 2, 'Unison/Octave', 'Unified, powerful resonance'),
('sextile', 'Supportive harmony', -2, 'Major third/sixth', 'Pleasant, flowing connection'),
('square', 'Dynamic tension', 5, 'Tritone', 'Friction, creative conflict'),
('trine', 'Easy flow', -3, 'Perfect fifth', 'Effortless, harmonious'),
('opposition', 'Polarity', 3, 'Octave with tension', 'Push-pull dynamic');

-- =====================================================
-- FUNCTIONS
-- =====================================================

-- Function to update timestamps
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Triggers for updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_natal_charts_updated_at
    BEFORE UPDATE ON natal_charts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
