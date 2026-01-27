from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import base64

# Import engines
from engines.ephemeris.chart_builder import ChartBuilder
from engines.harmonic.engine import HarmonicEngine
from engines.midi.exporter import MIDIExporter
from engines.ai_music.prompt_builder import PromptBuilder

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "service": "quantumelodic-api"
    })


@app.route('/api/natal-chart', methods=['POST'])
def calculate_natal_chart():
    """Calculate natal chart from birth data."""
    data = request.json

    # Validate required fields
    required_fields = ['date', 'time', 'latitude', 'longitude', 'timezone']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        chart_builder = ChartBuilder()
        chart = chart_builder.build_chart(
            date=data['date'],
            time=data['time'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            timezone=data['timezone']
        )
        return jsonify(chart.to_dict())
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/harmonic-analysis', methods=['POST'])
def harmonic_analysis():
    """Analyze chart data using the 24-mode harmonic system."""
    data = request.json

    if 'chart' not in data:
        return jsonify({"error": "Missing chart data"}), 400

    try:
        chart_data = data['chart']
        harmonic_engine = HarmonicEngine()
        result = harmonic_engine.analyze(chart_data)

        return jsonify({
            "primary_mode": result.primary_pentatonic_mode,
            "behavioral_mode": result.primary_quadratonic_mode,
            "tension_index": result.harmonic_tension_index,
            "dominant_element": result.dominant_element,
            "recommended_tempo": result.tempo_bpm,
            "key_signature": result.key_signature,
            "mode_details": {
                "mode_name": result.mode_name,
                "archetype": result.archetype,
                "emotional_color": result.emotional_color,
                "sonic_role": result.sonic_role,
                "waveform": result.waveform,
                "timbre": result.timbre
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/generate-midi', methods=['POST'])
def generate_midi():
    """Generate MIDI file from harmonic analysis."""
    data = request.json

    if 'harmonic_analysis' not in data:
        return jsonify({"error": "Missing harmonic_analysis data"}), 400

    try:
        harmonic_result = data['harmonic_analysis']
        midi_exporter = MIDIExporter()
        midi_bytes = midi_exporter.generate(harmonic_result)

        midi_base64 = base64.b64encode(midi_bytes).decode('utf-8')
        chart_name = data.get('chart_name', 'composition')

        return jsonify({
            "midi_data": midi_base64,
            "filename": f"natal_chart_{chart_name}.mid"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/ai-prompt', methods=['POST'])
def generate_ai_prompt():
    """Generate AI music prompts for Suno and Stable Audio."""
    data = request.json

    if 'harmonic_analysis' not in data:
        return jsonify({"error": "Missing harmonic_analysis data"}), 400

    try:
        harmonic_result = data['harmonic_analysis']
        prompt_builder = PromptBuilder()

        return jsonify({
            "suno_prompt": prompt_builder.build_suno_prompt(harmonic_result),
            "stable_audio_prompt": prompt_builder.build_stable_audio_prompt(harmonic_result)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/full-workflow', methods=['POST'])
def full_workflow():
    """Complete workflow: natal chart -> harmonic analysis -> MIDI + prompts."""
    data = request.json

    required_fields = ['date', 'time', 'latitude', 'longitude', 'timezone']
    for field in required_fields:
        if field not in data:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        # Step 1: Build natal chart
        chart_builder = ChartBuilder()
        chart = chart_builder.build_chart(
            date=data['date'],
            time=data['time'],
            latitude=data['latitude'],
            longitude=data['longitude'],
            timezone=data['timezone']
        )
        chart_dict = chart.to_dict()

        # Step 2: Harmonic analysis
        harmonic_engine = HarmonicEngine()
        harmonic_result = harmonic_engine.analyze(chart_dict)

        # Step 3: Generate MIDI
        midi_exporter = MIDIExporter()
        midi_bytes = midi_exporter.generate(harmonic_result)
        midi_base64 = base64.b64encode(midi_bytes).decode('utf-8')

        # Step 4: Generate AI prompts
        prompt_builder = PromptBuilder()
        suno_prompt = prompt_builder.build_suno_prompt(harmonic_result)
        stable_audio_prompt = prompt_builder.build_stable_audio_prompt(harmonic_result)

        chart_name = data.get('chart_name', 'composition')

        return jsonify({
            "chart": chart_dict,
            "harmonic_analysis": {
                "primary_mode": harmonic_result.primary_pentatonic_mode,
                "behavioral_mode": harmonic_result.primary_quadratonic_mode,
                "tension_index": harmonic_result.harmonic_tension_index,
                "dominant_element": harmonic_result.dominant_element,
                "recommended_tempo": harmonic_result.tempo_bpm,
                "key_signature": harmonic_result.key_signature,
                "mode_details": {
                    "mode_name": harmonic_result.mode_name,
                    "archetype": harmonic_result.archetype,
                    "emotional_color": harmonic_result.emotional_color,
                    "sonic_role": harmonic_result.sonic_role,
                    "waveform": harmonic_result.waveform,
                    "timbre": harmonic_result.timbre
                }
            },
            "midi": {
                "midi_data": midi_base64,
                "filename": f"natal_chart_{chart_name}.mid"
            },
            "ai_prompts": {
                "suno_prompt": suno_prompt,
                "stable_audio_prompt": stable_audio_prompt
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)
