import React, { useState, useEffect } from 'react';
import { Sparkles, ArrowRight, ShieldCheck, Zap } from 'lucide-react';
import { motion } from 'framer-motion';

const VeritasConcierge = () => {
  const [featuredItem, setFeaturedItem] = useState(null);

  useEffect(() => {
    // Fetching from the Pulse (D1 Database via Worker)
    fetch('/api/daily_deals')
      .then(res => res.json())
      .then(data => {
        // Veritas highlights the highest trend score
        const top = data.sort((a, b) => b.trend_score - a.trend_score)[0];
        setFeaturedItem(top);
      });
  }, []);

  return (
    <motion.div 
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      className="max-w-4xl mx-auto p-8 bg-slate-900 border border-blue-500/30 rounded-2xl shadow-2xl"
    >
      <div className="flex items-start gap-6">
        <div className="w-16 h-16 rounded-full bg-gradient-to-tr from-blue-600 to-cyan-400 flex items-center justify-center shadow-lg shadow-blue-500/20">
          <ShieldCheck className="text-white w-8 h-8" />
        </div>
        
        <div className="flex-1">
          <h2 className="text-2xl font-bold text-white mb-2 font-mono uppercase tracking-widest">
            Concierge Veritas: <span className="text-blue-400">System Orientation</span>
          </h2>
          <p className="text-slate-300 leading-relaxed mb-6 italic">
            "Welcome to the KeystoneCreatorSuite. I am Veritas. I have mapped the current flow of the Reese OS Kernel. Notice the structural integrity of the Trinity Framework as we move through the Toolbox."
          </p>

          {featuredItem && (
            <div className="bg-slate-800/50 p-6 rounded-xl border border-slate-700">
              <div className="flex justify-between items-center mb-4">
                <span className="flex items-center gap-2 text-xs font-bold text-cyan-400 uppercase tracking-tighter">
                  <Zap size={14} /> Reese Effect Calibration: {featuredItem.trend_score}%
                </span>
                <span className="text-slate-500 text-xs">Live Pulse Analysis</span>
              </div>
              
              <div className="flex gap-4">
                <img src={featuredItem.image} alt="Market Pulse" className="w-24 h-24 rounded-lg object-cover border border-slate-600" />
                <div>
                  <h3 className="text-lg font-semibold text-white">{featuredItem.title}</h3>
                  <p className="text-sm text-slate-400 mt-1">Identified by Trinity as a high-velocity market asset.</p>
                  <button className="mt-4 flex items-center gap-2 text-blue-400 hover:text-blue-300 transition-colors font-bold text-sm">
                    Acquire Asset via Stripe <ArrowRight size={16} />
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </motion.div>
  );
};

export default VeritasConcierge;
