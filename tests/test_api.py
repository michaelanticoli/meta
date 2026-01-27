"""
Basic API tests for Quantumelodic backend.
"""

import pytest
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from api.main import app


@pytest.fixture
def client():
    """Create a test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


def test_health_check(client):
    """Test the health check endpoint."""
    response = client.get('/api/health')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'version' in data


def test_status_check(client):
    """Test the detailed status endpoint."""
    response = client.get('/api/status')
    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'engines' in data


def test_natal_chart_missing_fields(client):
    """Test natal chart endpoint with missing fields."""
    response = client.post('/api/natal-chart',
                          json={'date': '1961-08-04'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'missing' in data


def test_harmonic_analysis_missing_chart(client):
    """Test harmonic analysis endpoint with missing chart."""
    response = client.post('/api/harmonic-analysis',
                          json={})
    assert response.status_code == 400


def test_generate_midi_missing_analysis(client):
    """Test MIDI generation endpoint with missing analysis."""
    response = client.post('/api/generate-midi',
                          json={})
    assert response.status_code == 400


def test_ai_prompt_missing_analysis(client):
    """Test AI prompt endpoint with missing analysis."""
    response = client.post('/api/ai-prompt',
                          json={})
    assert response.status_code == 400


def test_generate_composition_missing_fields(client):
    """Test full composition endpoint with missing fields."""
    response = client.post('/api/generate-composition',
                          json={'date': '1961-08-04'})
    assert response.status_code == 400


def test_404_handler(client):
    """Test 404 error handler."""
    response = client.get('/api/nonexistent')
    assert response.status_code == 404
    data = response.get_json()
    assert 'error' in data
