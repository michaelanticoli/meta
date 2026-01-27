import { useState, useEffect } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { motion } from 'motion/react';
import { ArrowLeft, Search, Loader2, MapPin, Clock, Calendar } from 'lucide-react';
import { api, searchLocation, getTimezone } from '../lib/api-client';
import type { BirthData, LocationSearchResult, FullWorkflowResult } from '../types';

export default function CreateChart() {
  const navigate = useNavigate();
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Form state
  const [formData, setFormData] = useState<BirthData>({
    date: '',
    time: '',
    latitude: 0,
    longitude: 0,
    timezone: '',
    locationName: '',
    chartName: '',
  });

  // Location search state
  const [locationQuery, setLocationQuery] = useState('');
  const [locationResults, setLocationResults] = useState<LocationSearchResult[]>([]);
  const [isSearching, setIsSearching] = useState(false);
  const [showResults, setShowResults] = useState(false);

  // Debounced location search
  useEffect(() => {
    const timer = setTimeout(async () => {
      if (locationQuery.length >= 3) {
        setIsSearching(true);
        const results = await searchLocation(locationQuery);
        setLocationResults(results);
        setShowResults(true);
        setIsSearching(false);
      } else {
        setLocationResults([]);
        setShowResults(false);
      }
    }, 500);

    return () => clearTimeout(timer);
  }, [locationQuery]);

  const handleLocationSelect = async (location: LocationSearchResult) => {
    const lat = parseFloat(location.lat);
    const lon = parseFloat(location.lon);
    const tz = await getTimezone(lat, lon);

    setFormData({
      ...formData,
      latitude: lat,
      longitude: lon,
      timezone: tz,
      locationName: location.display_name,
    });
    setLocationQuery(location.display_name);
    setShowResults(false);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      // Validate form
      if (!formData.date || !formData.time || !formData.latitude || !formData.longitude) {
        throw new Error('Please fill in all required fields');
      }

      // Call the full workflow API
      const result = await api.fullWorkflow({
        date: formData.date,
        time: formData.time + ':00', // Add seconds
        latitude: formData.latitude,
        longitude: formData.longitude,
        timezone: formData.timezone || 'UTC',
        chartName: formData.chartName || 'My Chart',
      });

      // Navigate to results with the data
      navigate('/results', { state: { result, birthData: formData } });
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-black text-white p-8">
      {/* Header */}
      <div className="max-w-2xl mx-auto mb-12">
        <Link
          to="/"
          className="inline-flex items-center gap-2 text-gray-400 hover:text-neon-gold transition mb-8"
        >
          <ArrowLeft className="w-5 h-5" />
          Back to Home
        </Link>

        <motion.h1
          className="text-5xl md:text-6xl font-bold mb-4 bg-gradient-to-r from-neon-gold to-yellow-400 bg-clip-text text-transparent"
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
        >
          Create Your Cosmic Melody
        </motion.h1>
        <motion.p
          className="text-xl text-gray-400"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
        >
          Enter your birth details to generate your unique musical signature
        </motion.p>
      </div>

      {/* Form */}
      <motion.form
        onSubmit={handleSubmit}
        className="max-w-2xl mx-auto space-y-8"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.3 }}
      >
        {/* Chart Name (Optional) */}
        <div>
          <label className="block text-gray-400 mb-2 text-sm uppercase tracking-wider">
            Chart Name (Optional)
          </label>
          <input
            type="text"
            value={formData.chartName}
            onChange={(e) => setFormData({ ...formData, chartName: e.target.value })}
            placeholder="e.g., My Birth Chart"
            className="w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-4 text-lg focus:border-neon-gold focus:outline-none transition"
          />
        </div>

        {/* Birth Date */}
        <div>
          <label className="flex items-center gap-2 text-gray-400 mb-2 text-sm uppercase tracking-wider">
            <Calendar className="w-4 h-4" />
            Birth Date *
          </label>
          <input
            type="date"
            value={formData.date}
            onChange={(e) => setFormData({ ...formData, date: e.target.value })}
            className="w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-4 text-lg focus:border-neon-gold focus:outline-none transition"
            required
          />
        </div>

        {/* Birth Time */}
        <div>
          <label className="flex items-center gap-2 text-gray-400 mb-2 text-sm uppercase tracking-wider">
            <Clock className="w-4 h-4" />
            Birth Time *
          </label>
          <input
            type="time"
            value={formData.time}
            onChange={(e) => setFormData({ ...formData, time: e.target.value })}
            className="w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-4 text-lg focus:border-neon-gold focus:outline-none transition"
            required
          />
          <p className="text-gray-500 text-sm mt-2">
            Accurate birth time is essential for precise calculations
          </p>
        </div>

        {/* Location Search */}
        <div className="relative">
          <label className="flex items-center gap-2 text-gray-400 mb-2 text-sm uppercase tracking-wider">
            <MapPin className="w-4 h-4" />
            Birth Location *
          </label>
          <div className="relative">
            <input
              type="text"
              value={locationQuery}
              onChange={(e) => setLocationQuery(e.target.value)}
              placeholder="Search for a city..."
              className="w-full bg-gray-900/50 border border-gray-700 rounded-lg px-4 py-4 pr-12 text-lg focus:border-neon-gold focus:outline-none transition"
              required={!formData.latitude}
            />
            <div className="absolute right-4 top-1/2 transform -translate-y-1/2">
              {isSearching ? (
                <Loader2 className="w-5 h-5 text-gray-500 animate-spin" />
              ) : (
                <Search className="w-5 h-5 text-gray-500" />
              )}
            </div>
          </div>

          {/* Location Results Dropdown */}
          {showResults && locationResults.length > 0 && (
            <div className="absolute z-10 w-full mt-2 bg-gray-900 border border-gray-700 rounded-lg overflow-hidden shadow-xl">
              {locationResults.map((location, index) => (
                <button
                  key={index}
                  type="button"
                  onClick={() => handleLocationSelect(location)}
                  className="w-full px-4 py-3 text-left hover:bg-gray-800 transition flex items-start gap-3"
                >
                  <MapPin className="w-5 h-5 text-neon-gold flex-shrink-0 mt-0.5" />
                  <span className="text-gray-300">{location.display_name}</span>
                </button>
              ))}
            </div>
          )}

          {/* Selected coordinates display */}
          {formData.latitude !== 0 && formData.longitude !== 0 && (
            <p className="text-neon-gold text-sm mt-2">
              Coordinates: {formData.latitude.toFixed(4)}, {formData.longitude.toFixed(4)}
              {formData.timezone && ` | Timezone: ${formData.timezone}`}
            </p>
          )}
        </div>

        {/* Error Display */}
        {error && (
          <div className="bg-red-900/20 border border-red-500 rounded-lg px-4 py-3 text-red-400">
            {error}
          </div>
        )}

        {/* Submit Button */}
        <button
          type="submit"
          disabled={isLoading}
          className="w-full bg-neon-gold text-black py-5 rounded-full font-bold text-xl hover:bg-yellow-300 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center gap-3"
        >
          {isLoading ? (
            <>
              <Loader2 className="w-6 h-6 animate-spin" />
              Generating Your Melody...
            </>
          ) : (
            'Generate My Melody'
          )}
        </button>
      </motion.form>

      {/* Info Box */}
      <motion.div
        className="max-w-2xl mx-auto mt-12 glass-card p-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.5 }}
      >
        <h3 className="text-lg font-bold mb-3 text-neon-gold">Why Birth Time Matters</h3>
        <p className="text-gray-400">
          Your birth time determines your Ascendant (rising sign) and house placements,
          which significantly influence your musical mode. If you don't know your exact
          birth time, use 12:00 noon for a general reading, but results will be less personalized.
        </p>
      </motion.div>
    </div>
  );
}
