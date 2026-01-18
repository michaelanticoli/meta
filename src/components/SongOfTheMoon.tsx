"use client";

import React, { useEffect, useRef, useState } from "react";
import { Button, Column, Flex, Heading, Row, Text } from "@once-ui-system/core";
import styles from "./SongOfTheMoon.module.scss";

// Moon frequency constants
const MOON_BASE_FREQUENCY = 210.42; // Hz - The "OM" frequency associated with lunar cycles
const LUNAR_SYNODIC_PERIOD = 29.53; // days - Average time between new moons

interface SongOfTheMoonProps {
  autoPlay?: boolean;
  showVisualization?: boolean;
}

export const SongOfTheMoon: React.FC<SongOfTheMoonProps> = ({
  autoPlay = false,
  showVisualization = true,
}) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [volume, setVolume] = useState(0.5);
  const [currentTime, setCurrentTime] = useState(0);
  const [isInitialized, setIsInitialized] = useState(false);

  const audioContextRef = useRef<AudioContext | null>(null);
  const oscillatorsRef = useRef<OscillatorNode[]>([]);
  const gainNodeRef = useRef<GainNode | null>(null);
  const analyserRef = useRef<AnalyserNode | null>(null);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const animationFrameRef = useRef<number | null>(null);

  // Initialize Web Audio API
  const initializeAudio = () => {
    if (audioContextRef.current) return;

    const AudioContextClass =
      window.AudioContext || (window as typeof window & { webkitAudioContext: typeof AudioContext }).webkitAudioContext;
    audioContextRef.current = new AudioContextClass();

    // Create gain node for volume control
    gainNodeRef.current = audioContextRef.current.createGain();
    gainNodeRef.current.gain.value = volume;
    gainNodeRef.current.connect(audioContextRef.current.destination);

    // Create analyser for visualization
    analyserRef.current = audioContextRef.current.createAnalyser();
    analyserRef.current.fftSize = 2048;
    analyserRef.current.connect(gainNodeRef.current);

    setIsInitialized(true);
  };

  // Generate moon frequency tones with harmonics
  const createMoonTones = () => {
    if (!audioContextRef.current || !gainNodeRef.current || !analyserRef.current) return;

    // Stop any existing oscillators
    stopMoonTones();

    const context = audioContextRef.current;
    const harmonics = [1, 2, 3, 4, 5, 8]; // Harmonic series
    const newOscillators: OscillatorNode[] = [];

    harmonics.forEach((harmonic, index) => {
      const oscillator = context.createOscillator();
      const harmonicGain = context.createGain();

      // Calculate frequency for this harmonic
      const frequency = MOON_BASE_FREQUENCY * harmonic;
      oscillator.frequency.value = frequency;

      // Use different waveforms for variety
      const waveforms: OscillatorType[] = ["sine", "triangle", "sawtooth"];
      oscillator.type = waveforms[index % waveforms.length];

      // Set gain based on harmonic (higher harmonics are quieter)
      const gainValue = 1 / (harmonic * 2);
      harmonicGain.gain.value = gainValue;

      // Connect: oscillator -> harmonicGain -> analyser -> main gain -> destination
      oscillator.connect(harmonicGain);
      harmonicGain.connect(analyserRef.current!);

      oscillator.start();
      newOscillators.push(oscillator);
    });

    oscillatorsRef.current = newOscillators;
  };

  // Stop all oscillators
  const stopMoonTones = () => {
    oscillatorsRef.current.forEach((osc) => {
      try {
        osc.stop();
        osc.disconnect();
      } catch (e) {
        // Oscillator might already be stopped
      }
    });
    oscillatorsRef.current = [];
  };

  // Toggle play/pause
  const togglePlay = () => {
    if (!isInitialized) {
      initializeAudio();
    }

    if (isPlaying) {
      stopMoonTones();
      setIsPlaying(false);
    } else {
      createMoonTones();
      setIsPlaying(true);
      if (showVisualization) {
        startVisualization();
      }
    }
  };

  // Update volume
  const handleVolumeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newVolume = parseFloat(e.target.value);
    setVolume(newVolume);
    if (gainNodeRef.current) {
      gainNodeRef.current.gain.value = newVolume;
    }
  };

  // Visualization
  const startVisualization = () => {
    if (!analyserRef.current || !canvasRef.current) return;

    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");
    if (!ctx) return;

    const analyser = analyserRef.current;
    const bufferLength = analyser.frequencyBinCount;
    const dataArray = new Uint8Array(bufferLength);

    const draw = () => {
      if (!isPlaying) return;

      animationFrameRef.current = requestAnimationFrame(draw);

      analyser.getByteTimeDomainData(dataArray);

      // Clear canvas with semi-transparent black for trail effect
      ctx.fillStyle = "rgba(10, 10, 20, 0.15)";
      ctx.fillRect(0, 0, canvas.width, canvas.height);

      // Draw waveform
      ctx.lineWidth = 2;
      ctx.strokeStyle = "rgba(138, 99, 210, 0.8)"; // Indigo/violet color
      ctx.beginPath();

      const sliceWidth = (canvas.width * 1.0) / bufferLength;
      let x = 0;

      for (let i = 0; i < bufferLength; i++) {
        const v = dataArray[i] / 128.0;
        const y = (v * canvas.height) / 2;

        if (i === 0) {
          ctx.moveTo(x, y);
        } else {
          ctx.lineTo(x, y);
        }

        x += sliceWidth;
      }

      ctx.lineTo(canvas.width, canvas.height / 2);
      ctx.stroke();

      // Draw frequency bars
      analyser.getByteFrequencyData(dataArray);
      const barWidth = (canvas.width / bufferLength) * 2.5;
      let barX = 0;

      for (let i = 0; i < bufferLength; i += 2) {
        const barHeight = (dataArray[i] / 255) * (canvas.height / 3);

        const hue = (i / bufferLength) * 360;
        ctx.fillStyle = `hsla(${hue}, 70%, 60%, 0.6)`;
        ctx.fillRect(barX, canvas.height - barHeight, barWidth, barHeight);

        barX += barWidth + 1;
      }
    };

    draw();
  };

  // Update current time for display
  useEffect(() => {
    let interval: NodeJS.Timeout;
    if (isPlaying) {
      interval = setInterval(() => {
        setCurrentTime((prev) => prev + 1);
      }, 1000);
    }
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [isPlaying]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      stopMoonTones();
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
      if (audioContextRef.current) {
        audioContextRef.current.close();
      }
    };
  }, []);

  // Auto-play if specified
  useEffect(() => {
    if (autoPlay && !isInitialized) {
      // Note: Browsers may block autoplay. User interaction might be required.
      initializeAudio();
    }
  }, [autoPlay, isInitialized]);

  // Format time display
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  // Get moon phase emoji based on current date
  const getMoonPhase = () => {
    const date = new Date();
    const dayOfMonth = date.getDate();
    const phases = ["🌑", "🌒", "🌓", "🌔", "🌕", "🌖", "🌗", "🌘"];
    // Using integer arithmetic for more predictable phase calculation
    const approximatePhase = Math.floor(((dayOfMonth % 30) / 30) * 8) % 8;
    return phases[approximatePhase];
  };

  return (
    <Column fillWidth gap="24" className={styles.container}>
      {/* Header */}
      <Column fillWidth gap="12" horizontal="center">
        <Text size="xl" onBackground="neutral-weak">
          {getMoonPhase()}
        </Text>
        <Heading variant="display-strong-l" align="center">
          Song of the Moon
        </Heading>
        <Text variant="body-default-m" align="center" onBackground="neutral-weak">
          An immersive sonic journey through lunar frequencies at {MOON_BASE_FREQUENCY} Hz
        </Text>
      </Column>

      {/* Visualizer */}
      {showVisualization && (
        <Column fillWidth horizontal="center">
          <canvas
            ref={canvasRef}
            width={800}
            height={400}
            className={styles.visualizer}
            style={{
              width: "100%",
              maxWidth: "800px",
              height: "auto",
              aspectRatio: "2/1",
              borderRadius: "var(--radius-m-4)",
              background: "rgba(10, 10, 20, 0.5)",
              border: "1px solid var(--neutral-alpha-weak)",
            }}
          />
        </Column>
      )}

      {/* Controls */}
      <Column fillWidth gap="16" maxWidth={600} horizontal="center" style={{ margin: "0 auto" }}>
        {/* Play/Pause and Time */}
        <Row fillWidth gap="16" vertical="center">
          <Button
            onClick={togglePlay}
            variant={isPlaying ? "secondary" : "primary"}
            size="l"
            prefixIcon={isPlaying ? "pause" : "play"}
          >
            {isPlaying ? "Pause" : "Play"}
          </Button>
          <Text variant="body-default-m" onBackground="neutral-weak">
            {formatTime(currentTime)}
          </Text>
        </Row>

        {/* Volume Control */}
        <Column fillWidth gap="8">
          <Row fillWidth horizontal="between">
            <Text variant="body-default-s" onBackground="neutral-weak">
              Volume
            </Text>
            <Text variant="body-default-s" onBackground="neutral-weak">
              {Math.round(volume * 100)}%
            </Text>
          </Row>
          <input
            type="range"
            min="0"
            max="1"
            step="0.01"
            value={volume}
            onChange={handleVolumeChange}
            className={styles.volumeSlider}
            style={{
              width: "100%",
              accentColor: "var(--brand-medium)",
            }}
          />
        </Column>

        {/* Information */}
        <Column fillWidth gap="8" padding="16" background="neutral-alpha-weak" radius="m">
          <Text variant="body-default-s" weight="strong">
            About the Moon Frequency
          </Text>
          <Text variant="body-default-s" onBackground="neutral-weak">
            This sonic experience is tuned to {MOON_BASE_FREQUENCY} Hz, known as the "OM" frequency,
            which resonates with lunar cycles. The lunar synodic period (time between new moons) is
            approximately {LUNAR_SYNODIC_PERIOD} days. The composition includes harmonics and
            overtones that create an evolving soundscape, designed to facilitate reflection,
            creativity, and connection with natural cycles.
          </Text>
        </Column>
      </Column>
    </Column>
  );
};
