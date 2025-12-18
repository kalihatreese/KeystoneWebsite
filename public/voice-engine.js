const VeritasIntelligence = (function() {
  const synth = window.speechSynthesis;
  
  // The Reese Effect: Tuned for 1.0 rate and 0.85 pitch for resonance
  const CADENCE = {
    rate: 0.9,      // Slightly slower for authoritative calm
    pitch: 0.85,    // Deep resonance for psychological alignment
    volume: 1.0
  };

  function speak(text) {
    if (synth.speaking) synth.cancel();
    
    const utterance = new SpeechSynthesisUtterance(text);
    utterance.rate = CADENCE.rate;
    utterance.pitch = CADENCE.pitch;
    utterance.volume = CADENCE.volume;

    // Pulse the 3D environment in sync with the speech cadence
    utterance.onboundary = (event) => {
      if (event.name === 'word') {
        window.triggerVeritasPulse(); 
      }
    };

    synth.speak(utterance);
  }

  function init() {
    window.addEventListener('click', () => {
      speak("The Trinity is now aligned. Welcome to the Reese Era.");
    }, { once: true });
  }

  return { init, speak };
})();
