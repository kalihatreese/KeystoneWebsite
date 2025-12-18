const VeritasIntelligence = (function() {
  let recognition;
  
  function init() {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      console.error("Browser does not support Speech Recognition.");
      return;
    }
    recognition = new SpeechRecognition();
    recognition.continuous = true;
    recognition.interimResults = true;

    recognition.onresult = (event) => {
      const transcript = Array.from(event.results)
        .map(result => result[0])
        .map(result => result.transcript)
        .join('');
      
      const box = document.getElementById('veritas-voice-box');
      box.style.opacity = '1';
      box.innerHTML = \`Listening: "\${transcript}"\`;
    };

    recognition.start();
  }

  return { init };
})();
