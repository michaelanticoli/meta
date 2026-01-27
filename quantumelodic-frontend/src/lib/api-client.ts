import axios, { AxiosInstance, AxiosResponse } from 'axios';
import type {
  BirthData,
  NatalChart,
  HarmonicAnalysis,
  MidiResult,
  AIPrompts,
  FullWorkflowResult,
  LocationSearchResult
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5000';

class ApiClient {
  private client: AxiosInstance;

  constructor() {
    this.client = axios.create({
      baseURL: API_BASE_URL,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  }

  // Health check
  async healthCheck(): Promise<{ status: string; version: string }> {
    const response = await this.client.get('/api/health');
    return response.data;
  }

  // Calculate natal chart
  async calculateNatalChart(birthData: BirthData): Promise<NatalChart> {
    const response = await this.client.post<NatalChart>('/api/natal-chart', birthData);
    return response.data;
  }

  // Get harmonic analysis
  async getHarmonicAnalysis(chart: NatalChart): Promise<HarmonicAnalysis> {
    const response = await this.client.post<HarmonicAnalysis>('/api/harmonic-analysis', { chart });
    return response.data;
  }

  // Generate MIDI
  async generateMidi(
    harmonicAnalysis: HarmonicAnalysis,
    chartName?: string
  ): Promise<MidiResult> {
    const response = await this.client.post<MidiResult>('/api/generate-midi', {
      harmonic_analysis: harmonicAnalysis,
      chart_name: chartName,
    });
    return response.data;
  }

  // Generate AI prompts
  async generateAIPrompts(harmonicAnalysis: HarmonicAnalysis): Promise<AIPrompts> {
    const response = await this.client.post<AIPrompts>('/api/ai-prompt', {
      harmonic_analysis: harmonicAnalysis,
    });
    return response.data;
  }

  // Full workflow - all steps in one call
  async fullWorkflow(birthData: BirthData): Promise<FullWorkflowResult> {
    const response = await this.client.post<FullWorkflowResult>('/api/full-workflow', birthData);
    return response.data;
  }
}

// Location search using Nominatim (OpenStreetMap)
export async function searchLocation(query: string): Promise<LocationSearchResult[]> {
  if (!query || query.length < 3) return [];

  try {
    const response = await axios.get<LocationSearchResult[]>(
      'https://nominatim.openstreetmap.org/search',
      {
        params: {
          q: query,
          format: 'json',
          addressdetails: 1,
          limit: 5,
        },
        headers: {
          'User-Agent': 'Quantumelodic/1.0',
        },
      }
    );
    return response.data;
  } catch (error) {
    console.error('Location search error:', error);
    return [];
  }
}

// Get timezone from coordinates using timezone API
export async function getTimezone(lat: number, lon: number): Promise<string> {
  // For now, return a default timezone
  // In production, use a timezone API like timezonedb or Google Time Zone API
  // or calculate based on longitude
  const offset = Math.round(lon / 15);
  return `Etc/GMT${offset >= 0 ? '-' : '+'}${Math.abs(offset)}`;
}

// Helper function to convert base64 MIDI to Blob for download
export function midiBase64ToBlob(base64: string): Blob {
  const binaryString = atob(base64);
  const bytes = new Uint8Array(binaryString.length);
  for (let i = 0; i < binaryString.length; i++) {
    bytes[i] = binaryString.charCodeAt(i);
  }
  return new Blob([bytes], { type: 'audio/midi' });
}

// Helper function to download MIDI file
export function downloadMidi(base64: string, filename: string): void {
  const blob = midiBase64ToBlob(base64);
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
}

export const api = new ApiClient();
export default api;
