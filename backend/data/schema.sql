-- Quantumelodic Database Schema
-- For use with Supabase (PostgreSQL)

-- =============================================================================
-- Core Tables
-- =============================================================================

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email TEXT UNIQUE NOT NULL,
    display_name TEXT,
    avatar_url TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE users ENABLE ROW LEVEL SECURITY;

-- Users can only see/edit their own data
CREATE POLICY "Users can view own data" ON users
    FOR SELECT USING (auth.uid() = id);

CREATE POLICY "Users can update own data" ON users
    FOR UPDATE USING (auth.uid() = id);

-- =============================================================================
-- Natal Charts
-- =============================================================================

CREATE TABLE IF NOT EXISTS natal_charts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    chart_name TEXT NOT NULL DEFAULT 'Natal Chart',

    -- Birth data
    birth_datetime TIMESTAMP WITH TIME ZONE NOT NULL,
    latitude DECIMAL(9, 6) NOT NULL,
    longitude DECIMAL(9, 6) NOT NULL,
    timezone TEXT NOT NULL,
    location_name TEXT,

    -- Calculated chart data (stored as JSONB for flexibility)
    chart_data JSONB NOT NULL,

    -- Summary fields for quick access
    sun_sign TEXT,
    moon_sign TEXT,
    rising_sign TEXT,
    dominant_element TEXT,
    dominant_modality TEXT,

    -- Metadata
    is_public BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE natal_charts ENABLE ROW LEVEL SECURITY;

-- Users can view their own charts and public charts
CREATE POLICY "Users can view own or public charts" ON natal_charts
    FOR SELECT USING (user_id = auth.uid() OR is_public = TRUE);

CREATE POLICY "Users can insert own charts" ON natal_charts
    FOR INSERT WITH CHECK (user_id = auth.uid());

CREATE POLICY "Users can update own charts" ON natal_charts
    FOR UPDATE USING (user_id = auth.uid());

CREATE POLICY "Users can delete own charts" ON natal_charts
    FOR DELETE USING (user_id = auth.uid());

-- Index for faster queries
CREATE INDEX idx_natal_charts_user_id ON natal_charts(user_id);
CREATE INDEX idx_natal_charts_sun_sign ON natal_charts(sun_sign);

-- =============================================================================
-- Musical Interpretations
-- =============================================================================

CREATE TABLE IF NOT EXISTS musical_interpretations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chart_id UUID REFERENCES natal_charts(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,

    -- Primary mode data
    primary_mode_id TEXT NOT NULL,
    primary_mode_name TEXT,
    primary_mode_archetype TEXT,

    -- Behavioral mode data
    behavioral_mode_id TEXT,
    behavioral_mode_archetype TEXT,

    -- Musical parameters
    tension_index INTEGER CHECK (tension_index >= 0 AND tension_index <= 100),
    tempo_bpm INTEGER CHECK (tempo_bpm > 0 AND tempo_bpm < 300),
    key_signature TEXT,
    time_signature TEXT,
    dynamics TEXT,
    waveform TEXT,
    timbre TEXT,

    -- Element data
    dominant_element TEXT,
    elemental_balance JSONB,

    -- Full harmonic analysis (JSONB for flexibility)
    full_analysis JSONB,

    -- Generated content
    midi_data BYTEA,
    ai_prompts JSONB,

    -- Metadata
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security
ALTER TABLE musical_interpretations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view interpretations for accessible charts" ON musical_interpretations
    FOR SELECT USING (
        user_id = auth.uid() OR
        chart_id IN (SELECT id FROM natal_charts WHERE is_public = TRUE)
    );

CREATE POLICY "Users can insert interpretations" ON musical_interpretations
    FOR INSERT WITH CHECK (user_id = auth.uid());

-- Index for faster queries
CREATE INDEX idx_interpretations_chart_id ON musical_interpretations(chart_id);
CREATE INDEX idx_interpretations_user_id ON musical_interpretations(user_id);

-- =============================================================================
-- Reference Tables: Pentatonic Modes
-- =============================================================================

CREATE TABLE IF NOT EXISTS pentatonic_modes (
    id SERIAL PRIMARY KEY,
    mode_id TEXT UNIQUE NOT NULL,
    mode_name TEXT NOT NULL,
    zodiac_sign TEXT NOT NULL,
    semitone_pattern TEXT NOT NULL,
    archetype TEXT NOT NULL,
    emotional_color TEXT,
    sonic_role TEXT,
    waveform TEXT,
    timbre TEXT,
    element TEXT NOT NULL
);

-- Insert default pentatonic modes
INSERT INTO pentatonic_modes (mode_id, mode_name, zodiac_sign, semitone_pattern, archetype, emotional_color, sonic_role, waveform, timbre, element)
VALUES
    ('P1_ARIES', 'Aries Pentatonic', 'Aries', '0-2-4-7-9', 'The Pioneer', 'Bold, Initiating, Courageous', 'Rhythmic Driver', 'sawtooth', 'brass', 'Fire'),
    ('P2_TAURUS', 'Taurus Pentatonic', 'Taurus', '0-2-5-7-9', 'The Builder', 'Grounded, Sensual, Steady', 'Harmonic Foundation', 'triangle', 'strings', 'Earth'),
    ('P3_GEMINI', 'Gemini Pentatonic', 'Gemini', '0-2-4-7-11', 'The Messenger', 'Curious, Adaptive, Communicative', 'Melodic Weaver', 'square', 'wind', 'Air'),
    ('P4_CANCER', 'Cancer Pentatonic', 'Cancer', '0-3-5-7-10', 'The Nurturer', 'Protective, Intuitive, Emotional', 'Emotional Core', 'sine', 'piano', 'Water'),
    ('P5_LEO', 'Leo Pentatonic', 'Leo', '0-2-4-7-9', 'The Sovereign', 'Creative, Expressive, Regal', 'Melodic Leader', 'sawtooth', 'brass', 'Fire'),
    ('P6_VIRGO', 'Virgo Pentatonic', 'Virgo', '0-2-5-7-10', 'The Analyst', 'Precise, Practical, Healing', 'Harmonic Precision', 'triangle', 'harp', 'Earth'),
    ('P7_LIBRA', 'Libra Pentatonic', 'Libra', '0-2-4-7-9', 'The Harmonizer', 'Balanced, Diplomatic, Aesthetic', 'Harmonic Balance', 'sine', 'strings', 'Air'),
    ('P8_SCORPIO', 'Scorpio Pentatonic', 'Scorpio', '0-1-5-7-8', 'The Transformer', 'Intense, Transformative, Deep', 'Tension Builder', 'sawtooth', 'synth', 'Water'),
    ('P9_SAGITTARIUS', 'Sagittarius Pentatonic', 'Sagittarius', '0-2-4-7-11', 'The Explorer', 'Expansive, Optimistic, Philosophical', 'Melodic Expansor', 'triangle', 'brass', 'Fire'),
    ('P10_CAPRICORN', 'Capricorn Pentatonic', 'Capricorn', '0-2-5-7-9', 'The Architect', 'Disciplined, Ambitious, Structured', 'Structural Foundation', 'square', 'organ', 'Earth'),
    ('P11_AQUARIUS', 'Aquarius Pentatonic', 'Aquarius', '0-2-4-8-10', 'The Visionary', 'Innovative, Humanitarian, Eccentric', 'Harmonic Innovator', 'square', 'synth', 'Air'),
    ('P12_PISCES', 'Pisces Pentatonic', 'Pisces', '0-3-5-8-10', 'The Dreamer', 'Mystical, Compassionate, Transcendent', 'Ethereal Ambiance', 'sine', 'pad', 'Water')
ON CONFLICT (mode_id) DO NOTHING;

-- =============================================================================
-- Reference Tables: Quadratonic Modes
-- =============================================================================

CREATE TABLE IF NOT EXISTS quadratonic_modes (
    id SERIAL PRIMARY KEY,
    mode_id TEXT UNIQUE NOT NULL,
    mode_name TEXT NOT NULL,
    modality TEXT NOT NULL,
    element TEXT NOT NULL,
    semitone_pattern TEXT NOT NULL,
    archetype TEXT NOT NULL,
    rhythmic_emphasis TEXT,
    dynamic_character TEXT
);

-- Insert default quadratonic modes
INSERT INTO quadratonic_modes (mode_id, mode_name, modality, element, semitone_pattern, archetype, rhythmic_emphasis, dynamic_character)
VALUES
    ('Q1_CARDINAL_FIRE', 'Cardinal Fire', 'Cardinal', 'Fire', '0-4-7-11', 'The Initiator', 'downbeat', 'explosive'),
    ('Q2_CARDINAL_EARTH', 'Cardinal Earth', 'Cardinal', 'Earth', '0-3-7-10', 'The Achiever', 'steady', 'determined'),
    ('Q3_CARDINAL_AIR', 'Cardinal Air', 'Cardinal', 'Air', '0-4-7-9', 'The Negotiator', 'syncopated', 'balanced'),
    ('Q4_CARDINAL_WATER', 'Cardinal Water', 'Cardinal', 'Water', '0-3-5-10', 'The Protector', 'flowing', 'nurturing'),
    ('Q5_FIXED_FIRE', 'Fixed Fire', 'Fixed', 'Fire', '0-4-7-11', 'The Performer', 'strong', 'dramatic'),
    ('Q6_FIXED_EARTH', 'Fixed Earth', 'Fixed', 'Earth', '0-3-7-9', 'The Sustainer', 'grounded', 'persistent'),
    ('Q7_FIXED_AIR', 'Fixed Air', 'Fixed', 'Air', '0-4-8-10', 'The Rebel', 'irregular', 'electric'),
    ('Q8_FIXED_WATER', 'Fixed Water', 'Fixed', 'Water', '0-1-5-8', 'The Alchemist', 'intense', 'transformative'),
    ('Q9_MUTABLE_FIRE', 'Mutable Fire', 'Mutable', 'Fire', '0-4-7-11', 'The Adventurer', 'free', 'expansive'),
    ('Q10_MUTABLE_EARTH', 'Mutable Earth', 'Mutable', 'Earth', '0-2-5-10', 'The Healer', 'precise', 'analytical'),
    ('Q11_MUTABLE_AIR', 'Mutable Air', 'Mutable', 'Air', '0-2-4-11', 'The Communicator', 'quick', 'mercurial'),
    ('Q12_MUTABLE_WATER', 'Mutable Water', 'Mutable', 'Water', '0-3-5-10', 'The Mystic', 'fluid', 'dreamy')
ON CONFLICT (mode_id) DO NOTHING;

-- =============================================================================
-- Reference Tables: Element Timbres
-- =============================================================================

CREATE TABLE IF NOT EXISTS element_timbres (
    id SERIAL PRIMARY KEY,
    element TEXT UNIQUE NOT NULL,
    primary_waveform TEXT NOT NULL,
    primary_instruments TEXT[] NOT NULL,
    secondary_instruments TEXT[],
    sonic_character TEXT,
    dynamic_range TEXT,
    reverb_character TEXT
);

-- Insert default element timbres
INSERT INTO element_timbres (element, primary_waveform, primary_instruments, secondary_instruments, sonic_character, dynamic_range, reverb_character)
VALUES
    ('Fire', 'sawtooth', ARRAY['brass', 'electric guitar', 'synth lead'], ARRAY['drums', 'percussion'], 'bright, aggressive, cutting', 'wide, dynamic', 'short, bright'),
    ('Earth', 'triangle', ARRAY['acoustic guitar', 'piano', 'strings'], ARRAY['cello', 'bass', 'marimba'], 'warm, rich, grounded', 'moderate, consistent', 'medium, natural'),
    ('Air', 'square', ARRAY['flute', 'wind instruments', 'chimes'], ARRAY['harp', 'vibraphone', 'bells'], 'light, airy, crystalline', 'soft to moderate', 'long, spacious'),
    ('Water', 'sine', ARRAY['pads', 'cello', 'ambient synths'], ARRAY['ocean sounds', 'glass', 'voice'], 'deep, flowing, ethereal', 'soft, evolving', 'long, dreamy')
ON CONFLICT (element) DO NOTHING;

-- =============================================================================
-- Functions & Triggers
-- =============================================================================

-- Update timestamp trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to tables with updated_at
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_natal_charts_updated_at
    BEFORE UPDATE ON natal_charts
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- Views
-- =============================================================================

-- View for chart summaries with latest interpretation
CREATE VIEW chart_summaries AS
SELECT
    nc.id,
    nc.user_id,
    nc.chart_name,
    nc.birth_datetime,
    nc.location_name,
    nc.sun_sign,
    nc.moon_sign,
    nc.rising_sign,
    nc.dominant_element,
    nc.is_public,
    nc.created_at,
    mi.primary_mode_archetype,
    mi.tension_index,
    mi.tempo_bpm,
    mi.key_signature
FROM natal_charts nc
LEFT JOIN LATERAL (
    SELECT *
    FROM musical_interpretations
    WHERE chart_id = nc.id
    ORDER BY created_at DESC
    LIMIT 1
) mi ON true;

-- =============================================================================
-- Sample Data (for development/testing)
-- =============================================================================

-- Uncomment to add sample data for testing
/*
INSERT INTO users (id, email, display_name)
VALUES ('00000000-0000-0000-0000-000000000001', 'test@example.com', 'Test User');

INSERT INTO natal_charts (user_id, chart_name, birth_datetime, latitude, longitude, timezone, location_name, chart_data, sun_sign, moon_sign, rising_sign, dominant_element, dominant_modality)
VALUES (
    '00000000-0000-0000-0000-000000000001',
    'Barack Obama',
    '1961-08-04 19:24:00-10',
    21.3099,
    -157.8581,
    'Pacific/Honolulu',
    'Honolulu, Hawaii',
    '{"planets": [], "houses": [], "aspects": []}',
    'Leo',
    'Gemini',
    'Aquarius',
    'Air',
    'Fixed'
);
*/
