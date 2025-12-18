import React from 'react';
import { ShieldAlert, FileCheck, Scale } from 'lucide-react';

const Legal = () => {
  return (
    <div className="bg-black text-white min-h-screen p-12 font-serif">
      <div className="max-w-3xl mx-auto border border-slate-800 p-12 bg-slate-950 rounded-sm shadow-2xl">
        <div className="flex justify-between items-center mb-12 border-b border-slate-800 pb-6">
          <h1 className="text-2xl tracking-tighter uppercase font-black">Trinity Assurance License</h1>
          <ShieldAlert className="text-blue-600" />
        </div>
        
        <section className="space-y-6 text-slate-400 leading-relaxed text-sm">
          <p className="font-bold text-white uppercase tracking-widest text-xs">I. System Orientation</p>
          <p>
            The Keystone Creator Suite operates under the Reese OS Kernel. By accessing this node, you acknowledge the non-linear execution of the Trinity Framework.
          </p>
          
          <p className="font-bold text-white uppercase tracking-widest text-xs">II. Compute Deflation Protocol</p>
          <p>
            Users are granted a non-exclusive right to utilize the Reese Effect for scaling architectural intelligence. Any attempts to bypass Veritas Concierge integrity checks will result in immediate node de-authorization.
          </p>

          <div className="bg-blue-900/10 p-6 border-l-2 border-blue-600 italic">
            "We do not sell software. We provide structural integrity for the digital age." — Veritas
          </div>
        </section>

        <div className="mt-12 pt-6 border-t border-slate-800 flex justify-between text-[10px] uppercase tracking-widest text-slate-600">
          <span>ID: K-2025-TRINITY</span>
          <span>Status: Active Layer 1</span>
        </div>
      </div>
    </div>
  );
};

export default Legal;
