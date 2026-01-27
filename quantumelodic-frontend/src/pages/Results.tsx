import { useLocation, Link, Navigate } from 'react-router-dom';
import { useState, useRef, useCallback, useEffect } from 'react';
import { motion } from 'motion/react';
import {
  ArrowLeft,
  Play,
  Pause,
  Download,
  Copy,
  Check,
  Music,
  Flame,
  Mountain,
  Wind,
  Droplets
} from 'lucide-react';
import { downloadMidi } from '../lib/api-client';
import type { FullWorkflowResult, BirthData } from '../types';

export default function Results() {
  const location = useLocation();
  const state = location.state as { result: FullWorkflowResult; birthData: BirthData } | null;

  // Redirect if no data
  if (!state?.result) {
    return <Navigate to="/create" replace />;
  }

  const { result, birthData } = state;
  const { chart, harmonic_analysis, midi, ai_prompts } = result;

  // Audio state
  const [isPlaying, setIsPlaying] = useState(false);
  const audioCtxRef = useRef<AudioContext | null>(null);
  const oscillatorsRef = useRef<OscillatorNode[]>([]);
  const gainNodeRef = useRef<GainNode | null>(null);

  // Copy state
  const [copiedPrompt, setCopiedPrompt] = useState<'suno' | 'stable' | null>(null);

  // Get element icon
  const ElementIcon = {
    Fire: Flame,
    Earth: Mountain,
    Air: Wind,
    Water: Droplets,
  }[harmonic_analysis.dominant_element] || Flame;

  // Web Audio API - Play cosmic chord based on harmonic analysis
  const playCosmicChord = useCallback(() => {
    if (isPlaying) {
      // Stop playing
      oscillatorsRef.current.forEach(osc => {
        osc.stop();
        osc.disconnect();
      });
      oscillatorsRef.current = [];
      if (gainNodeRef.current) {
        gainNodeRef.current.disconnect();
      }
      setIsPlaying(false);
      return;
    }

    // Create audio context
    if (!audioCtxRef.current) {
      audioCtxRef.current = new AudioContext();
    }
    const audioCtx = audioCtxRef.current;

    // Create gain node for volume
    const gainNode = audioCtx.createGain();
    gainNode.gain.value = 0.3;
    gainNode.connect(audioCtx.destination);
    gainNodeRef.current = gainNode;

    // Get waveform type
    const waveformMap: Record<string, OscillatorType> = {
      'Sawtooth': 'sawtooth',
      'Sine': 'sine',
      'Triangle': 'triangle',
      'Square': 'square',
      'Noise/FM': 'sawtooth',
    };
    const waveform = waveformMap[harmonic_analysis.mode_details.waveform] || 'sine';

    // Base frequency from key signature
    const keyFrequencies: Record<string, number> = {
      'C major': 261.63, 'C minor': 261.63,
      'D major': 293.66, 'D minor': 293.66,
      'E major': 329.63, 'E minor': 329.63,
      'F major': 349.23, 'F minor': 349.23,
      'F# major': 369.99, 'F# minor': 369.99,
      'G major': 392.00, 'G minor': 392.00,
      'A major': 440.00, 'A minor': 440.00,
      'Bb major': 466.16, 'Bb minor': 466.16,
      'B major': 493.88, 'B minor': 493.88,
    };
    const baseFreq = keyFrequencies[harmonic_analysis.key_signature] || 440;

    // Create chord based on mode (pentatonic scale intervals)
    const intervals = [0, 2, 4, 7, 9]; // Pentatonic scale degrees
    const oscillators: OscillatorNode[] = [];

    intervals.slice(0, 3).forEach((semitones, index) => {
      const osc = audioCtx.createOscillator();
      osc.type = waveform;
      osc.frequency.value = baseFreq * Math.pow(2, semitones / 12);

      // Slight detune for richness
      osc.detune.value = (index - 1) * 5;

      osc.connect(gainNode);
      osc.start();
      oscillators.push(osc);
    });

    // Add a low drone
    const drone = audioCtx.createOscillator();
    drone.type = 'sine';
    drone.frequency.value = baseFreq / 2;
    drone.connect(gainNode);
    drone.start();
    oscillators.push(drone);

    oscillatorsRef.current = oscillators;
    setIsPlaying(true);
  }, [isPlaying, harmonic_analysis]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      oscillatorsRef.current.forEach(osc => {
        try {
          osc.stop();
          osc.disconnect();
        } catch {
          // Ignore errors
        }
      });
    };
  }, []);

  const handleDownloadMidi = () => {
    downloadMidi(midi.midi_data, midi.filename);
  };

  const copyPrompt = async (type: 'suno' | 'stable') => {
    const text = type === 'suno' ? ai_prompts.suno_prompt : ai_prompts.stable_audio_prompt;
    await navigator.clipboard.writeText(text);
    setCopiedPrompt(type);
    setTimeout(() => setCopiedPrompt(null), 2000);
  };

  return (
    <div className="min-h-screen bg-black text-white p-8">
      {/* Header */}
      <div className="max-w-6xl mx-auto mb-12">
        <Link
          to="/create"
          className="inline-flex items-center gap-2 text-gray-400 hover:text-neon-gold transition mb-8"
        >
          <ArrowLeft className="w-5 h-5" />
          Create Another Chart
        </Link>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          <h1 className="text-5xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-neon-gold to-yellow-400 bg-clip-text text-transparent">
            Your Cosmic Melody
          </h1>
          {birthData.chartName && (
            <p className="text-xl text-gray-400">{birthData.chartName}</p>
          )}
        </motion.div>
      </div>

      {/* Main Content */}
      <div className="max-w-6xl mx-auto grid lg:grid-cols-2 gap-12">
        {/* Left Column - Musical Analysis */}
        <motion.div
          className="space-y-6"
          initial={{ opacity: 0, x: -30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
        >
          {/* Primary Mode Card */}
          <div className="glass-card p-8">
            <h2 className="text-3xl font-bold mb-2 text-neon-gold">
              {harmonic_analysis.mode_details.archetype}
            </h2>
            <p className="text-xl text-gray-300 mb-6">
              {harmonic_analysis.mode_details.emotional_color}
            </p>

            <div className="grid grid-cols-2 gap-4">
              <div className="bg-gray-800/50 rounded-lg p-4">
                <p className="text-gray-400 text-sm mb-1">Musical Mode</p>
                <p className="font-bold">{harmonic_analysis.mode_details.mode_name}</p>
              </div>
              <div className="bg-gray-800/50 rounded-lg p-4">
                <p className="text-gray-400 text-sm mb-1">Key Signature</p>
                <p className="font-bold">{harmonic_analysis.key_signature}</p>
              </div>
              <div className="bg-gray-800/50 rounded-lg p-4">
                <p className="text-gray-400 text-sm mb-1">Waveform</p>
                <p className="font-bold">{harmonic_analysis.mode_details.waveform}</p>
              </div>
              <div className="bg-gray-800/50 rounded-lg p-4">
                <p className="text-gray-400 text-sm mb-1">Sonic Role</p>
                <p className="font-bold">{harmonic_analysis.mode_details.sonic_role}</p>
              </div>
            </div>
          </div>

          {/* Tension Index */}
          <div className="glass-card p-6">
            <div className="flex justify-between items-center mb-3">
              <h3 className="font-bold text-lg">Harmonic Tension</h3>
              <span className="text-neon-gold font-bold text-2xl">
                {harmonic_analysis.tension_index}%
              </span>
            </div>
            <div className="w-full bg-gray-800 h-4 rounded-full overflow-hidden">
              <motion.div
                className="h-full bg-gradient-to-r from-green-500 via-yellow-500 to-red-500"
                initial={{ width: 0 }}
                animate={{ width: `${harmonic_analysis.tension_index}%` }}
                transition={{ duration: 1, delay: 0.5 }}
              />
            </div>
            <p className="text-gray-400 text-sm mt-2">
              {harmonic_analysis.tension_index < 40
                ? 'Harmonious and flowing'
                : harmonic_analysis.tension_index < 70
                ? 'Dynamic with creative tension'
                : 'Intense and transformative'}
            </p>
          </div>

          {/* Element & Tempo */}
          <div className="grid grid-cols-2 gap-4">
            <div className="glass-card p-6 text-center">
              <ElementIcon className="w-12 h-12 mx-auto mb-3 text-neon-gold" />
              <p className="text-gray-400 text-sm mb-1">Dominant Element</p>
              <p className="text-xl font-bold">{harmonic_analysis.dominant_element}</p>
            </div>
            <div className="glass-card p-6 text-center">
              <Music className="w-12 h-12 mx-auto mb-3 text-neon-gold" />
              <p className="text-gray-400 text-sm mb-1">Recommended Tempo</p>
              <p className="text-xl font-bold">{harmonic_analysis.recommended_tempo} BPM</p>
            </div>
          </div>

          {/* Chart Summary */}
          <div className="glass-card p-6">
            <h3 className="font-bold text-lg mb-4">Your Natal Chart</h3>
            <div className="grid grid-cols-3 gap-4 text-center">
              <div>
                <p className="text-gray-400 text-sm">Sun</p>
                <p className="font-bold text-neon-gold">{chart.sun_sign}</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Moon</p>
                <p className="font-bold text-neon-gold">{chart.moon_sign}</p>
              </div>
              <div>
                <p className="text-gray-400 text-sm">Rising</p>
                <p className="font-bold text-neon-gold">{chart.rising_sign}</p>
              </div>
            </div>
          </div>
        </motion.div>

        {/* Right Column - Audio & Actions */}
        <motion.div
          className="space-y-6"
          initial={{ opacity: 0, x: 30 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
        >
          {/* Play Section */}
          <div className="glass-card p-8 text-center">
            <h3 className="text-2xl font-bold mb-6">Listen to Your Cosmic Chord</h3>

            <button
              onClick={playCosmicChord}
              className="w-full bg-neon-gold text-black py-6 rounded-full font-bold text-xl mb-6 hover:bg-yellow-300 transition flex items-center justify-center gap-3"
            >
              {isPlaying ? (
                <>
                  <Pause className="w-8 h-8" />
                  Stop Playing
                </>
              ) : (
                <>
                  <Play className="w-8 h-8" />
                  Play Cosmic Chord
                </>
              )}
            </button>

            <button
              onClick={handleDownloadMidi}
              className="w-full bg-gray-800 text-white py-4 rounded-full font-bold hover:bg-gray-700 transition flex items-center justify-center gap-3"
            >
              <Download className="w-5 h-5" />
              Download MIDI File
            </button>
          </div>

          {/* AI Prompts */}
          <div className="glass-card p-6">
            <h3 className="font-bold text-lg mb-4">AI Music Prompts</h3>

            {/* Suno Prompt */}
            <div className="mb-6">
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-400 text-sm">Suno AI Prompt</span>
                <button
                  onClick={() => copyPrompt('suno')}
                  className="text-neon-gold hover:text-yellow-300 transition flex items-center gap-1 text-sm"
                >
                  {copiedPrompt === 'suno' ? (
                    <>
                      <Check className="w-4 h-4" />
                      Copied!
                    </>
                  ) : (
                    <>
                      <Copy className="w-4 h-4" />
                      Copy
                    </>
                  )}
                </button>
              </div>
              <div className="bg-gray-900 rounded-lg p-4 text-sm text-gray-300 max-h-40 overflow-y-auto">
                {ai_prompts.suno_prompt}
              </div>
            </div>

            {/* Stable Audio Prompt */}
            <div>
              <div className="flex justify-between items-center mb-2">
                <span className="text-gray-400 text-sm">Stable Audio Prompt</span>
                <button
                  onClick={() => copyPrompt('stable')}
                  className="text-neon-gold hover:text-yellow-300 transition flex items-center gap-1 text-sm"
                >
                  {copiedPrompt === 'stable' ? (
                    <>
                      <Check className="w-4 h-4" />
                      Copied!
                    </>
                  ) : (
                    <>
                      <Copy className="w-4 h-4" />
                      Copy
                    </>
                  )}
                </button>
              </div>
              <div className="bg-gray-900 rounded-lg p-4 text-sm text-gray-300">
                {ai_prompts.stable_audio_prompt}
              </div>
            </div>
          </div>

          {/* Timbre Description */}
          <div className="glass-card p-6">
            <h3 className="font-bold text-lg mb-3">Your Sonic Signature</h3>
            <p className="text-gray-300">
              {harmonic_analysis.mode_details.timbre}
            </p>
          </div>

          {/* Share Section */}
          <div className="glass-card p-6 text-center">
            <h3 className="font-bold text-lg mb-4">Share Your Results</h3>
            <div className="flex justify-center gap-4">
              <button className="px-6 py-2 bg-gray-800 rounded-lg hover:bg-gray-700 transition">
                Twitter
              </button>
              <button className="px-6 py-2 bg-gray-800 rounded-lg hover:bg-gray-700 transition">
                Facebook
              </button>
              <button className="px-6 py-2 bg-gray-800 rounded-lg hover:bg-gray-700 transition">
                Copy Link
              </button>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
}
