"""
Quantumelodic API - Flask Backend
Transforms astrological natal charts into musical compositions using
the 24-mode pentatonic/quadratonic harmonic system.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os
import sys
import base64
from datetime import datetime

load_dotenv()

# Add backend directory to path for imports
backend_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

# Import engines with graceful fallback for missing dependencies
ENGINES_AVAILABLE = {
    'ephemeris': False,
    'harmonic': False,
    'midi': False,
    'ai_music': False
}

try:
    from engines.ephemeris.chart_builder import ChartBuilder
    ENGINES_AVAILABLE['ephemeris'] = True
except ImportError as e:
    ChartBuilder = None
    print(f"Warning: Ephemeris engine not available: {e}")

try:
    from engines.harmonic.engine import HarmonicEngine
    ENGINES_AVAILABLE['harmonic'] = True
except ImportError as e:
    HarmonicEngine = None
    print(f"Warning: Harmonic engine not available: {e}")

try:
    from engines.midi.exporter import MIDIExporter
    ENGINES_AVAILABLE['midi'] = True
except ImportError as e:
    MIDIExporter = None
    print(f"Warning: MIDI engine not available: {e}")

try:
    from engines.ai_music.prompt_builder import PromptBuilder
    ENGINES_AVAILABLE['ai_music'] = True
except ImportError as e:
    PromptBuilder = None
    print(f"Warning: AI Music engine not available: {e}")

app = Flask(__name__)
CORS(app, resources={
    r"/api/*": {
        "origins": os.getenv("ALLOWED_ORIGINS", "*").split(","),
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key-change-in-production')

# =============================================================================
# Health Check Endpoints
# =============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Basic health check endpoint."""
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "service": "quantumelodic-api",
        "timestamp": datetime.utcnow().isoformat()
    })


@app.route('/api/status', methods=['GET'])
def detailed_status():
    """Detailed status check with engine availability."""
    return jsonify({
        "status": "healthy",
        "version": "1.0.0",
        "engines": ENGINES_AVAILABLE,
        "database": os.getenv('SUPABASE_URL') is not None
    })


# =============================================================================
# Natal Chart Endpoints
# =============================================================================

@app.route('/api/natal-chart', methods=['POST'])
def calculate_natal_chart():
    """
    Calculate natal chart from birth data.

    Request body:
    {
        "date": "1961-08-04",
        "time": "19:24:00",
        "latitude": 21.3099,
        "longitude": -157.8581,
        "timezone": "Pacific/Honolulu",
        "name": "Optional chart name"
    }
    """
    data = request.json

    # Validate required fields
    required_fields = ['date', 'time', 'latitude', 'longitude', 'timezone']
    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing_fields
        }), 400

    if not ENGINES_AVAILABLE['ephemeris'] or ChartBuilder is None:
        return jsonify({"error": "Ephemeris engine not available. Please install pyswisseph."}), 503

    try:
        # Use ChartBuilder to calculate natal chart
        chart_builder = ChartBuilder()
        chart = chart_builder.build_chart(
            date=data['date'],
            time=data['time'],
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            timezone=data['timezone']
        )

        response = chart.to_dict()
        response['chart_name'] = data.get('name', 'Natal Chart')

        return jsonify(response)

    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Chart calculation failed: {str(e)}"}), 500


# =============================================================================
# Harmonic Analysis Endpoints
# =============================================================================

@app.route('/api/harmonic-analysis', methods=['POST'])
def harmonic_analysis():
    """
    Analyze natal chart using the 24-mode harmonic system.

    Request body:
    {
        "chart": { ... natal chart data ... }
    }
    """
    data = request.json

    if 'chart' not in data:
        return jsonify({"error": "Missing 'chart' in request body"}), 400

    if not ENGINES_AVAILABLE['harmonic'] or HarmonicEngine is None:
        return jsonify({"error": "Harmonic engine not available."}), 503

    try:
        chart_data = data['chart']

        # Use HarmonicEngine to analyze chart
        harmonic_engine = HarmonicEngine()
        result = harmonic_engine.analyze(chart_data)

        return jsonify({
            "primary_mode": {
                "mode_id": result.primary_pentatonic_mode.mode_id,
                "mode_name": result.primary_pentatonic_mode.mode_name,
                "archetype": result.primary_pentatonic_mode.archetype,
                "emotional_color": result.primary_pentatonic_mode.emotional_color,
                "semitone_pattern": result.primary_pentatonic_mode.semitone_pattern,
                "zodiac_sign": result.primary_pentatonic_mode.zodiac_sign
            },
            "behavioral_mode": {
                "mode_id": result.primary_quadratonic_mode.mode_id,
                "mode_name": result.primary_quadratonic_mode.mode_name,
                "archetype": result.primary_quadratonic_mode.archetype
            },
            "tension_index": result.harmonic_tension_index,
            "dominant_element": result.dominant_element,
            "recommended_tempo": result.tempo_bpm,
            "key_signature": result.key_signature,
            "time_signature": result.time_signature,
            "dynamics": result.dynamics,
            "waveform": result.waveform,
            "timbre": result.timbre
        })

    except KeyError as e:
        return jsonify({"error": f"Invalid chart data: missing {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Harmonic analysis failed: {str(e)}"}), 500


# =============================================================================
# MIDI Generation Endpoints
# =============================================================================

@app.route('/api/generate-midi', methods=['POST'])
def generate_midi():
    """
    Generate MIDI file from harmonic analysis.

    Request body:
    {
        "harmonic_analysis": { ... analysis result ... },
        "chart_name": "optional name for file"
    }
    """
    data = request.json

    if 'harmonic_analysis' not in data:
        return jsonify({"error": "Missing 'harmonic_analysis' in request body"}), 400

    if not ENGINES_AVAILABLE['midi'] or MIDIExporter is None:
        return jsonify({"error": "MIDI engine not available. Please install midiutil."}), 503

    try:
        harmonic_result = data['harmonic_analysis']
        chart_name = data.get('chart_name', 'composition')

        # Generate MIDI using MIDIExporter
        midi_exporter = MIDIExporter()
        midi_bytes = midi_exporter.generate(harmonic_result)

        # Encode as base64 for transmission
        midi_base64 = base64.b64encode(midi_bytes).decode('utf-8')

        # Generate filename (sanitize chart_name)
        safe_name = "".join(c for c in chart_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')[:50]
        filename = f"natal_chart_{safe_name}.mid"

        return jsonify({
            "midi_data": midi_base64,
            "filename": filename,
            "format": "base64",
            "content_type": "audio/midi"
        })

    except Exception as e:
        return jsonify({"error": f"MIDI generation failed: {str(e)}"}), 500


# =============================================================================
# AI Prompt Generation Endpoints
# =============================================================================

@app.route('/api/ai-prompt', methods=['POST'])
def generate_ai_prompt():
    """
    Generate AI music generation prompts for Suno AI and Stable Audio.

    Request body:
    {
        "harmonic_analysis": { ... analysis result ... }
    }
    """
    data = request.json

    if 'harmonic_analysis' not in data:
        return jsonify({"error": "Missing 'harmonic_analysis' in request body"}), 400

    if not ENGINES_AVAILABLE['ai_music'] or PromptBuilder is None:
        return jsonify({"error": "AI Music engine not available."}), 503

    try:
        harmonic_result = data['harmonic_analysis']

        # Generate prompts using PromptBuilder
        prompt_builder = PromptBuilder()

        return jsonify({
            "suno_prompt": prompt_builder.build_suno_prompt(harmonic_result),
            "stable_audio_prompt": prompt_builder.build_stable_audio_prompt(harmonic_result),
            "udio_prompt": prompt_builder.build_udio_prompt(harmonic_result),
            "generic_prompt": prompt_builder.build_generic_prompt(harmonic_result)
        })

    except Exception as e:
        return jsonify({"error": f"AI prompt generation failed: {str(e)}"}), 500


# =============================================================================
# Combined Workflow Endpoints
# =============================================================================

@app.route('/api/generate-composition', methods=['POST'])
def generate_composition():
    """
    Full pipeline: birth data -> natal chart -> harmonic analysis -> MIDI + prompts.

    This is a convenience endpoint that combines all steps.

    Request body:
    {
        "date": "1961-08-04",
        "time": "19:24:00",
        "latitude": 21.3099,
        "longitude": -157.8581,
        "timezone": "Pacific/Honolulu",
        "name": "Optional chart name"
    }
    """
    data = request.json

    # Validate required fields
    required_fields = ['date', 'time', 'latitude', 'longitude', 'timezone']
    missing_fields = [f for f in required_fields if f not in data]
    if missing_fields:
        return jsonify({
            "error": "Missing required fields",
            "missing": missing_fields
        }), 400

    # Check all required engines are available
    missing_engines = [eng for eng, avail in ENGINES_AVAILABLE.items() if not avail]
    if missing_engines:
        return jsonify({
            "error": "Required engines not available",
            "missing_engines": missing_engines
        }), 503

    try:
        chart_name = data.get('name', 'Natal Chart')

        # Step 1: Calculate natal chart
        chart_builder = ChartBuilder()
        chart = chart_builder.build_chart(
            date=data['date'],
            time=data['time'],
            latitude=float(data['latitude']),
            longitude=float(data['longitude']),
            timezone=data['timezone']
        )
        chart_dict = chart.to_dict()

        # Step 2: Harmonic analysis
        harmonic_engine = HarmonicEngine()
        harmonic_result = harmonic_engine.analyze(chart_dict)

        # Step 3: Generate MIDI
        midi_exporter = MIDIExporter()
        midi_bytes = midi_exporter.generate(harmonic_result.to_dict())
        midi_base64 = base64.b64encode(midi_bytes).decode('utf-8')

        # Step 4: Generate AI prompts
        prompt_builder = PromptBuilder()

        # Construct response
        return jsonify({
            "chart": {
                "name": chart_name,
                "birth_data": {
                    "date": data['date'],
                    "time": data['time'],
                    "latitude": data['latitude'],
                    "longitude": data['longitude'],
                    "timezone": data['timezone']
                },
                "positions": chart_dict
            },
            "harmonic_analysis": {
                "primary_mode": {
                    "mode_id": harmonic_result.primary_pentatonic_mode.mode_id,
                    "mode_name": harmonic_result.primary_pentatonic_mode.mode_name,
                    "archetype": harmonic_result.primary_pentatonic_mode.archetype,
                    "emotional_color": harmonic_result.primary_pentatonic_mode.emotional_color
                },
                "behavioral_mode": {
                    "mode_id": harmonic_result.primary_quadratonic_mode.mode_id,
                    "archetype": harmonic_result.primary_quadratonic_mode.archetype
                },
                "tension_index": harmonic_result.harmonic_tension_index,
                "dominant_element": harmonic_result.dominant_element,
                "recommended_tempo": harmonic_result.tempo_bpm,
                "key_signature": harmonic_result.key_signature
            },
            "midi": {
                "data": midi_base64,
                "filename": f"natal_chart_{chart_name.replace(' ', '_')}.mid",
                "format": "base64"
            },
            "ai_prompts": {
                "suno": prompt_builder.build_suno_prompt(harmonic_result.to_dict()),
                "stable_audio": prompt_builder.build_stable_audio_prompt(harmonic_result.to_dict())
            }
        })

    except ValueError as e:
        return jsonify({"error": f"Invalid input: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"Composition generation failed: {str(e)}"}), 500


# =============================================================================
# Error Handlers
# =============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404


@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({"error": "Method not allowed"}), 405


# =============================================================================
# Application Entry Point
# =============================================================================

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_ENV', 'development') == 'development'

    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║                  QUANTUMELODIC API v1.0.0                  ║
    ║         Transforming Stars into Sound Since 2024          ║
    ╚═══════════════════════════════════════════════════════════╝

    Running on: http://localhost:{port}
    Debug mode: {debug}

    Endpoints:
      GET  /api/health              - Health check
      GET  /api/status              - Detailed status
      POST /api/natal-chart         - Calculate natal chart
      POST /api/harmonic-analysis   - Analyze chart harmonically
      POST /api/generate-midi       - Generate MIDI file
      POST /api/ai-prompt           - Generate AI music prompts
      POST /api/generate-composition - Full pipeline
    """)

    app.run(debug=debug, host='0.0.0.0', port=port)
