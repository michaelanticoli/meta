import { Link } from 'react-router-dom';
import { motion } from 'motion/react';
import { Music, Star, Sparkles, ArrowRight, Waves } from 'lucide-react';

export default function Home() {
  return (
    <div className="min-h-screen bg-black text-white overflow-hidden">
      {/* Hero Section */}
      <section className="relative min-h-screen flex items-center justify-center">
        {/* Animated background */}
        <div className="absolute inset-0 overflow-hidden">
          <div className="absolute inset-0 bg-gradient-radial from-purple-900/20 via-black to-black" />
          <motion.div
            className="absolute w-96 h-96 rounded-full bg-neon-gold/10 blur-3xl"
            animate={{
              x: [0, 100, 0],
              y: [0, -50, 0],
            }}
            transition={{
              duration: 10,
              repeat: Infinity,
              ease: "easeInOut",
            }}
            style={{ top: '10%', left: '10%' }}
          />
          <motion.div
            className="absolute w-64 h-64 rounded-full bg-purple-600/20 blur-3xl"
            animate={{
              x: [0, -80, 0],
              y: [0, 60, 0],
            }}
            transition={{
              duration: 8,
              repeat: Infinity,
              ease: "easeInOut",
            }}
            style={{ bottom: '20%', right: '15%' }}
          />
        </div>

        <div className="relative z-10 text-center px-8 max-w-5xl mx-auto">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <h1 className="text-7xl md:text-9xl font-bold mb-6 bg-gradient-to-r from-neon-gold via-yellow-400 to-neon-gold bg-clip-text text-transparent">
              Quantumelodics
            </h1>
            <p className="text-2xl md:text-3xl text-gray-300 mb-8">
              Transform Your Stars Into Sound
            </p>
            <p className="text-lg text-gray-400 mb-12 max-w-2xl mx-auto">
              Your natal chart holds a unique musical signature. We decode the cosmic frequencies
              of your birth moment into personalized melodies, modes, and soundscapes.
            </p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8, delay: 0.3 }}
          >
            <Link
              to="/create"
              className="inline-flex items-center gap-3 bg-neon-gold text-black px-10 py-5 rounded-full font-bold text-xl hover:bg-yellow-300 transition-all transform hover:scale-105"
            >
              Create Your Melody
              <ArrowRight className="w-6 h-6" />
            </Link>
          </motion.div>
        </div>

        {/* Scroll indicator */}
        <motion.div
          className="absolute bottom-10 left-1/2 transform -translate-x-1/2"
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
        >
          <Waves className="w-8 h-8 text-gray-500" />
        </motion.div>
      </section>

      {/* Features Section */}
      <section className="py-32 px-8">
        <div className="max-w-6xl mx-auto">
          <motion.h2
            className="text-5xl font-bold text-center mb-20"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            The 24-Mode System
          </motion.h2>

          <div className="grid md:grid-cols-3 gap-8">
            <FeatureCard
              icon={<Star className="w-12 h-12" />}
              title="12 Pentatonic Modes"
              description="Each zodiac sign maps to a unique pentatonic scale, capturing the soul's musical expression."
              delay={0}
            />
            <FeatureCard
              icon={<Music className="w-12 h-12" />}
              title="12 Quadratonic Modes"
              description="Behavioral patterns encoded in four-note modes, revealing your rhythmic signature."
              delay={0.2}
            />
            <FeatureCard
              icon={<Sparkles className="w-12 h-12" />}
              title="Elemental Timbres"
              description="Fire, Earth, Air, Water - each element shapes the sonic texture of your personal composition."
              delay={0.4}
            />
          </div>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="py-32 px-8 bg-gradient-to-b from-black via-gray-900/50 to-black">
        <div className="max-w-4xl mx-auto">
          <motion.h2
            className="text-5xl font-bold text-center mb-20"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            viewport={{ once: true }}
          >
            How It Works
          </motion.h2>

          <div className="space-y-16">
            <Step
              number={1}
              title="Enter Your Birth Data"
              description="Provide your birth date, time, and location. Precision matters - accurate birth time yields more resonant results."
            />
            <Step
              number={2}
              title="Chart Calculation"
              description="We calculate your natal chart using Swiss Ephemeris, mapping planetary positions to their musical counterparts."
            />
            <Step
              number={3}
              title="Harmonic Analysis"
              description="Your chart is analyzed through our 24-mode system, determining your primary scales, tempos, and timbres."
            />
            <Step
              number={4}
              title="Receive Your Melody"
              description="Download your personalized MIDI file, hear your cosmic chord, and get AI prompts to generate full compositions."
            />
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-32 px-8 text-center">
        <motion.div
          className="max-w-3xl mx-auto"
          initial={{ opacity: 0, y: 30 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
        >
          <h2 className="text-5xl font-bold mb-8">
            Ready to Hear Your Stars?
          </h2>
          <p className="text-xl text-gray-400 mb-12">
            Your unique cosmic melody awaits. Transform the moment of your birth
            into a sound you can feel.
          </p>
          <Link
            to="/create"
            className="inline-flex items-center gap-3 bg-neon-gold text-black px-10 py-5 rounded-full font-bold text-xl hover:bg-yellow-300 transition-all transform hover:scale-105"
          >
            Begin Your Journey
            <ArrowRight className="w-6 h-6" />
          </Link>
        </motion.div>
      </section>

      {/* Footer */}
      <footer className="py-12 px-8 border-t border-gray-800">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row justify-between items-center">
          <p className="text-gray-500">&copy; 2025 Quantumelodics. All rights reserved.</p>
          <div className="flex gap-6 mt-4 md:mt-0">
            <a href="#" className="text-gray-500 hover:text-neon-gold transition">About</a>
            <a href="#" className="text-gray-500 hover:text-neon-gold transition">Contact</a>
            <a href="#" className="text-gray-500 hover:text-neon-gold transition">Privacy</a>
          </div>
        </div>
      </footer>
    </div>
  );
}

interface FeatureCardProps {
  icon: React.ReactNode;
  title: string;
  description: string;
  delay: number;
}

function FeatureCard({ icon, title, description, delay }: FeatureCardProps) {
  return (
    <motion.div
      className="glass-card p-8 text-center"
      initial={{ opacity: 0, y: 30 }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true }}
      transition={{ duration: 0.6, delay }}
    >
      <div className="text-neon-gold mb-6 flex justify-center">{icon}</div>
      <h3 className="text-2xl font-bold mb-4">{title}</h3>
      <p className="text-gray-400">{description}</p>
    </motion.div>
  );
}

interface StepProps {
  number: number;
  title: string;
  description: string;
}

function Step({ number, title, description }: StepProps) {
  return (
    <motion.div
      className="flex gap-8 items-start"
      initial={{ opacity: 0, x: -30 }}
      whileInView={{ opacity: 1, x: 0 }}
      viewport={{ once: true }}
    >
      <div className="flex-shrink-0 w-16 h-16 rounded-full bg-neon-gold/20 border-2 border-neon-gold flex items-center justify-center">
        <span className="text-2xl font-bold text-neon-gold">{number}</span>
      </div>
      <div>
        <h3 className="text-2xl font-bold mb-2">{title}</h3>
        <p className="text-gray-400 text-lg">{description}</p>
      </div>
    </motion.div>
  );
}
