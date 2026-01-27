# Quantumelodic Backend API

Transform natal charts into musical compositions using the 24-mode pentatonic/quadratonic system.

## Quick Start

### 1. Setup Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
cp .env.example .env
# Edit .env with your configuration
```

### 3. Run Development Server

```bash
python api/main.py
```

The API will be available at `http://localhost:5000`

### 4. Test Health Check

```bash
curl http://localhost:5000/api/health
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/health` | GET | Health check |
| `/api/status` | GET | Detailed status with engine availability |
| `/api/natal-chart` | POST | Calculate natal chart from birth data |
| `/api/harmonic-analysis` | POST | Analyze chart using 24-mode system |
| `/api/generate-midi` | POST | Generate MIDI file from harmonic analysis |
| `/api/ai-prompt` | POST | Generate AI music prompts |
| `/api/generate-composition` | POST | Full pipeline: birth data to MIDI |

## Example Usage

### Calculate Natal Chart

```bash
curl -X POST http://localhost:5000/api/natal-chart \
  -H "Content-Type: application/json" \
  -d '{
    "date": "1961-08-04",
    "time": "19:24:00",
    "latitude": 21.3099,
    "longitude": -157.8581,
    "timezone": "Pacific/Honolulu",
    "name": "Example Chart"
  }'
```

### Full Composition Pipeline

```bash
curl -X POST http://localhost:5000/api/generate-composition \
  -H "Content-Type: application/json" \
  -d '{
    "date": "1961-08-04",
    "time": "19:24:00",
    "latitude": 21.3099,
    "longitude": -157.8581,
    "timezone": "Pacific/Honolulu",
    "name": "My Cosmic Melody"
  }'
```

## Project Structure

```
backend/
├── api/
│   └── main.py              # Flask API routes
├── engines/
│   ├── ephemeris/           # Natal chart calculations
│   │   ├── chart_builder.py
│   │   └── models.py
│   ├── harmonic/            # 24-mode analysis system
│   │   ├── engine.py
│   │   └── models.py
│   ├── midi/                # MIDI generation
│   │   └── exporter.py
│   └── ai_music/            # AI prompt generation
│       └── prompt_builder.py
├── data/
│   ├── schema.sql           # Database schema
│   └── mappings/            # CSV mapping files
├── models/                  # Database models
├── utils/                   # Utility functions
├── requirements.txt         # Python dependencies
├── .env.example            # Environment template
├── Procfile                # Deployment config
└── runtime.txt             # Python version
```

## The 24-Mode System

### Pentatonic Modes (12)
Each zodiac sign maps to a unique 5-note pentatonic scale with specific musical characteristics:
- **Semitone patterns**: Unique intervals for each sign
- **Archetypes**: Psychological/mythological themes
- **Timbres**: Suggested instruments and waveforms
- **Elements**: Fire, Earth, Air, Water associations

### Quadratonic Modes (12)
Behavioral/rhythmic modes based on modality × element combinations:
- **Cardinal**: Initiating energy
- **Fixed**: Sustaining energy
- **Mutable**: Adaptive energy

See `data/mappings/` for complete mode definitions.

## Database Setup (Supabase)

1. Create a new Supabase project
2. Run the schema from `data/schema.sql`
3. Add your Supabase credentials to `.env`

## Deployment

### Render.com

1. Connect your repository to Render
2. The `render.yaml` will auto-configure the service
3. Set environment variables in the Render dashboard

### Manual Deployment

```bash
gunicorn api.main:app --bind 0.0.0.0:$PORT --workers 2
```

## Development

### Running Tests

```bash
pytest tests/
```

### Code Formatting

```bash
black .
flake8 .
```

## License

Proprietary - Quantumelodic
