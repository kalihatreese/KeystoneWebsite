const VeritasIntelligence = (function() {
  const synth = window.speechSynthesis;
  
  // Dynamic Cadence Controller
  const SCHUMANN_BASE = 0.85; // Deep Earth resonance pitch

  function speak(text) {
    if (synth.speaking) synth.cancel();
    
    // Split text into "Cadence Fragments"
    // Format: [S] for Slow/Heavy, [F] for Fast/Genius
    const parts = [
      { rate: 0.6, pitch: 0.7, text: "The Trinity is grounded." },
      { rate: 1.5, pitch: 1.0, text: "Analyzing code-bases, logic-streams, and architectural-imperatives." },
      { rate: 0.8, pitch: SCHUMANN_BASE, text: "We are falling in reverse... into the truth." }
    ];

    parts.forEach((part, index) => {
      const utterance = new SpeechSynthesisUtterance(part.text);
      utterance.rate = part.rate;
      utterance.pitch = part.pitch;
      
      utterance.onstart = () => {
        // Visual sync: Speed up or slow down the 3D rotation based on rate
        window.updateRotationSpeed(part.rate);
      };

      utterance.onboundary = (e) => {
        if(e.name === 'word') window.triggerVeritasPulse(part.rate);
      };

      synth.speak(utterance);
    });
  }

  function init() {
    window.addEventListener('click', () => {
      speak();
    }, { once: true });
  }

  return { init, speak };
})();
